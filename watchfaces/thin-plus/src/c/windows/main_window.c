#include "main_window.h"
#include "../modules/refresh.h"
#include "../modules/step_ring.h"

#define MARGIN             scl_x(35)
#define THICKNESS          scl_x(20)
// Stroke widths must be odd, even values get rounded down when drawing
#define STROKE_WIDTH       (THICKNESS | 1)
#define STROKE_WIDTH_THICK (STROKE_WIDTH + 2)
#define STROKE_WIDTH_SEC   (STROKE_WIDTH - 2)
#define SECONDS_DURATION   15000
#define TIP_LENGTH         (MARGIN + 2)
#define ANIMATION_DELAY    300
#define ANIMATION_DURATION 1000
#define HAND_LENGTH_SEC    scl_x(440)
#define HAND_LENGTH_MIN    HAND_LENGTH_SEC
#define HAND_LENGTH_HOUR   (HAND_LENGTH_SEC - scl_x(130))

typedef struct {
  int days;
  int hours;
  int minutes;
  int seconds;
} SimpleTime;

static Window *s_main_window;
static TextLayer *s_weekday_layer, *s_day_in_month_layer, *s_month_layer;
static Layer *s_canvas_layer, *s_bg_layer, *s_slots_layer;

// One each of these to represent the current time and an animated pseudo-time
static SimpleTime s_current_time, s_anim_time;

static char s_weekday_buffer[8], s_month_buffer[8], s_day_buffer[3];
static GRect s_full_day_frame;
static bool s_animating, s_is_connected, s_show_seconds;
static AppTimer *s_seconds_timer;

/******************************* Event Services *******************************/

static void tick_handler(struct tm *tick_time, TimeUnits changed) {
  s_current_time.days = tick_time->tm_mday;
  s_current_time.hours = tick_time->tm_hour;
  s_current_time.minutes = tick_time->tm_min;
  s_current_time.seconds = tick_time->tm_sec;

  s_current_time.hours -= (s_current_time.hours > 12) ? 12 : 0;

  snprintf(s_day_buffer, sizeof(s_day_buffer), "%d", s_current_time.days);
  strftime(s_weekday_buffer, sizeof(s_weekday_buffer), "%a", tick_time);
  strftime(s_month_buffer, sizeof(s_month_buffer), "%b", tick_time);

  text_layer_set_text(s_weekday_layer, s_weekday_buffer);
  text_layer_set_text(s_day_in_month_layer, s_day_buffer);
  text_layer_set_text(s_month_layer, s_month_buffer);

  if (changed & MINUTE_UNIT) {
    main_window_refresh_data();
    refresh_poll();
  }
  // Finally
  layer_mark_dirty(s_canvas_layer);
}

static void update_time() {
  time_t t = time(NULL);
  tick_handler(localtime(&t), SECOND_UNIT);
}

static void subscribe_tick() {
  tick_timer_service_unsubscribe();
  tick_timer_service_subscribe(s_show_seconds ? SECOND_UNIT : MINUTE_UNIT, tick_handler);
}

static void seconds_timer_handler(void *context) {
  s_seconds_timer = NULL;
  s_show_seconds = false;
  subscribe_tick();
  layer_mark_dirty(s_canvas_layer);
}

// Second hand only runs for a while after a wrist flick to save battery
static void show_seconds() {
  if (!data_get_enable(MESSAGE_KEY_EnableSecondHand)) return;

  if (s_seconds_timer) {
    app_timer_reschedule(s_seconds_timer, SECONDS_DURATION);
  } else {
    s_seconds_timer = app_timer_register(SECONDS_DURATION, seconds_timer_handler, NULL);
  }

  if (!s_show_seconds) {
    s_show_seconds = true;
    subscribe_tick();
    update_time();
  }
}

static void accel_tap_handler(AccelAxisType axis, int32_t direction) {
  show_seconds();
}

#if defined(PBL_TOUCH)
static void touch_handler(const TouchEvent *event, void *context) {
  if (event->type == TouchEvent_Liftoff) show_seconds();
}

static void update_touch_subscription() {
  touch_service_unsubscribe();
  if (data_get_enable(MESSAGE_KEY_TapForSeconds) &&
      data_get_enable(MESSAGE_KEY_EnableSecondHand)) {
    touch_service_subscribe(touch_handler, NULL);
  }
}
#endif

static void bt_handler(bool connected) {
  APP_LOG(APP_LOG_LEVEL_DEBUG, "Phone connected=%d, enhanced=%d, vibrate=%d", connected,
    data_get_enable(MESSAGE_KEY_EnableEnhancedBT), data_get_enable(MESSAGE_KEY_VibrateOnDisconnect));
  // Notify disconnection
  if (!connected && s_is_connected && data_get_enable(MESSAGE_KEY_VibrateOnDisconnect)) {
    vibes_long_pulse();
  }

  s_is_connected = connected;
  layer_mark_dirty(s_canvas_layer);
}

static void batt_handler(BatteryChargeState state) {
  layer_mark_dirty(s_bg_layer);
  layer_mark_dirty(s_canvas_layer);
  layer_mark_dirty(s_slots_layer);
}

/************************** AnimationImplementation ***************************/

static void animation_started(Animation *anim, void *context) {
  s_animating = true;
}

static void animation_stopped(Animation *anim, bool stopped, void *context) {
  s_animating = false;

  main_window_reload_config();
}

static void animate(int duration, int delay, AnimationImplementation *implementation, bool handlers) {
  Animation *anim = animation_create();
  if (anim) {
    animation_set_duration(anim, duration);
    animation_set_delay(anim, delay);
    animation_set_curve(anim, AnimationCurveEaseInOut);
    animation_set_implementation(anim, implementation);
    if (handlers) {
      animation_set_handlers(anim, (AnimationHandlers) {
        .started = animation_started,
        .stopped = animation_stopped
      }, NULL);
    }
    animation_schedule(anim);
  }
}

/****************************** Drawing Functions *****************************/

static void bg_update_proc(Layer *layer, GContext *ctx) {
  GRect bounds = layer_get_bounds(layer);
  GPoint center = grect_center_point(&bounds);

  BatteryChargeState state = battery_state_service_peek();
  const int perc = state.charge_percent;
  const int batt_hours = (int)(12.0F * ((float)perc / 100.0F)) + 1;

  GColor bg_color = data_get_color(MESSAGE_KEY_ColorBackground);
  GColor notch_color = data_get_color(MESSAGE_KEY_ColorNotches);

  graphics_context_set_stroke_width(ctx, STROKE_WIDTH);
  for (int h = 0; h < 12; h++) {
    const int angle = (TRIG_MAX_ANGLE * h) / 12;
    const int nom = (int32_t)(3 * HAND_LENGTH_SEC);
    GPoint point = (GPoint) {
      .x = (int16_t)(sin_lookup(angle) * nom / TRIG_MAX_RATIO) + center.x,
      .y = (int16_t)(-cos_lookup(angle) * nom / TRIG_MAX_RATIO) + center.y,
    };

    if (data_get_enable(MESSAGE_KEY_EnableBattery)) {
      if (h < batt_hours) {
        const bool highlight = state.is_charging && data_get_enable(MESSAGE_KEY_EnableChargingColor);
        graphics_context_set_stroke_color(ctx,
          highlight ? data_get_color(MESSAGE_KEY_ColorCharging) : notch_color);
      } else {
        // Empty segment
        graphics_context_set_stroke_color(ctx, data_get_color(MESSAGE_KEY_ColorBatteryEmpty));
      }
    } else {
      // No battery indicator, show all
      graphics_context_set_stroke_color(ctx, notch_color);
    }
    graphics_draw_line(ctx, center, point);
  }

  // Make markers by cutting out the middle
  graphics_context_set_fill_color(ctx, bg_color);
#ifdef PBL_ROUND
  graphics_fill_circle(ctx, center, (bounds.size.w / 2) - (2 * MARGIN));
#else
  graphics_fill_rect(
    ctx,
    GRect(MARGIN, MARGIN, bounds.size.w - (2 * MARGIN), bounds.size.h - (2 * MARGIN)),
    0,
    GCornerNone
  );
#endif
  step_ring_draw(ctx, bounds, MARGIN);
}

#if defined(PBL_RECT) && !defined(PBL_PLATFORM_APLITE)
static void unobstructed_did_change(void *context) {
  layer_mark_dirty(s_slots_layer);
}
#endif

static void slots_update_proc(Layer *layer, GContext *ctx) {
  bool bottom_visible = true;
#if defined(PBL_RECT) && !defined(PBL_PLATFORM_APLITE)
  Layer *root = window_get_root_layer(s_main_window);
  bottom_visible = layer_get_unobstructed_bounds(root).size.h >= layer_get_bounds(root).size.h;
#endif
  // Keep the analog geometry, date and other slots fixed while a peek is open.
  slots_draw(ctx, bottom_visible);
}

static GPoint make_hand_point(int quantity, int intervals, int len, GPoint center) {
  const int angle = (TRIG_MAX_ANGLE * quantity) / intervals;
  return (GPoint) {
    .x = (int16_t)(sin_lookup(angle) * (int32_t)len / TRIG_MAX_RATIO) + center.x,
    .y = (int16_t)(-cos_lookup(angle) * (int32_t)len / TRIG_MAX_RATIO) + center.y,
  };
}

// Point part way along a line, rounded, so it stays on the line actually drawn
static GPoint point_along(GPoint from, GPoint to, int num, int den) {
  const int dx = (to.x - from.x) * num;
  const int dy = (to.y - from.y) * num;
  return GPoint(
    from.x + (dx + ((dx < 0) ? -den : den) / 2) / den,
    from.y + (dy + ((dy < 0) ? -den : den) / 2) / den
  );
}

// Draw the full hand, then the tip over its end sharing the same end point and line
static void draw_hand(GContext *ctx, GPoint center, GPoint end, int len, GColor shaft_color,
                      GColor tip_color) {
  graphics_context_set_stroke_color(ctx, shaft_color);
  graphics_draw_line(ctx, center, end);

  graphics_context_set_stroke_color(ctx, tip_color);
  graphics_draw_line(ctx, point_along(center, end, len - TIP_LENGTH, len), end);
}

static int hours_to_minutes(int hours_out_of_12) {
  return (hours_out_of_12 * 60) / 12;
}

static void draw_proc(Layer *layer, GContext *ctx) {
  GRect bounds = layer_get_bounds(layer);
  GPoint center = grect_center_point(&bounds);

  SimpleTime mode_time = (s_animating) ? s_anim_time : s_current_time;

  // Plot hand ends
  GPoint second_hand_end = make_hand_point(mode_time.seconds, 60, HAND_LENGTH_SEC, center);
  GPoint minute_hand_end = make_hand_point(mode_time.minutes, 60, HAND_LENGTH_MIN, center);

  float minute_angle = TRIG_MAX_ANGLE * mode_time.minutes / 60;
  float hour_angle;
  if (s_animating) {
    // Hours out of 60 for smoothness
    hour_angle = TRIG_MAX_ANGLE * mode_time.hours / 60;
  } else {
    hour_angle = TRIG_MAX_ANGLE * mode_time.hours / 12;
  }
  hour_angle += (minute_angle / TRIG_MAX_ANGLE) * (TRIG_MAX_ANGLE / 12);

  // Hour is more accurate
  GPoint hour_hand_end = (GPoint) {
    .x = (int16_t)(sin_lookup(hour_angle) * (int32_t)HAND_LENGTH_HOUR / TRIG_MAX_RATIO) + center.x,
    .y = (int16_t)(-cos_lookup(hour_angle) * (int32_t)HAND_LENGTH_HOUR / TRIG_MAX_RATIO) + center.y,
  };

  GColor bg_color = data_get_color(MESSAGE_KEY_ColorBackground);
  GColor hour_min_color = data_get_color(MESSAGE_KEY_ColorHourMinutes);
  GColor second_color = data_get_color(MESSAGE_KEY_ColorSeconds);
  GColor tip_color = data_get_color(MESSAGE_KEY_ColorHandTips);
  GColor second_tip_color = data_get_color(MESSAGE_KEY_ColorSecondTip);

  // Draw hands
  graphics_context_set_antialiased(ctx, true);
  const bool thick = data_get_enable(MESSAGE_KEY_EnableThickHands);
  graphics_context_set_stroke_width(ctx, thick ? STROKE_WIDTH_THICK : STROKE_WIDTH);
  draw_hand(ctx, center, minute_hand_end, HAND_LENGTH_MIN, hour_min_color, tip_color);
  draw_hand(ctx, center, hour_hand_end, HAND_LENGTH_HOUR, hour_min_color, tip_color);

  // Draw second hand
  if (s_show_seconds) {
    graphics_context_set_stroke_width(ctx, STROKE_WIDTH_SEC);
    draw_hand(ctx, center, second_hand_end, HAND_LENGTH_SEC, second_color, second_tip_color);
  }

  // Center
  graphics_context_set_fill_color(ctx, data_get_color(MESSAGE_KEY_ColorCenterDot));
  const int center_radius = thick ? 5 : 4;
  graphics_fill_circle(ctx, center, center_radius);

  // Draw black if disconnected
  if (data_get_enable(MESSAGE_KEY_EnableBT) && !s_is_connected) {
    if (data_get_enable(MESSAGE_KEY_EnableEnhancedBT)) {
      graphics_context_set_fill_color(ctx, data_get_color(MESSAGE_KEY_ColorDisconnected));
      graphics_fill_circle(ctx, center, center_radius + 3);
      graphics_context_set_fill_color(ctx, bg_color);
      graphics_fill_circle(ctx, center, center_radius);
    } else {
      graphics_context_set_fill_color(ctx, bg_color);
      graphics_fill_circle(ctx, center, center_radius - 1);
    }
  }
}

/*********************************** Window ***********************************/

static void window_load(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
  GRect bounds = layer_get_bounds(window_layer);

  s_bg_layer = layer_create(bounds);
  layer_set_update_proc(s_bg_layer, bg_update_proc);
  layer_add_child(window_layer, s_bg_layer);

  const int x_offset = scl_x(710);
  const int y_offset = scl_y(305);
  const int text_s = 100;

  GColor month_day_color = data_get_color(MESSAGE_KEY_ColorMonthDay);
  GColor date_color = data_get_color(MESSAGE_KEY_ColorDate);

  s_weekday_layer = text_layer_create(
    GRect(x_offset, y_offset + scl_y_pp({.o = 35, .g = 30}), text_s, text_s)
  );
  text_layer_set_font(s_weekday_layer, scl_get_font(SFI_SmallBold));
  text_layer_set_text_color(s_weekday_layer, date_color);
  text_layer_set_background_color(s_weekday_layer, GColorClear);

  s_day_in_month_layer = text_layer_create(
    GRect(
      x_offset - scl_x_pp({.o = 60, .e = 35, .g = 15}),
      y_offset + scl_y_pp({.o = 105, .e = 120, .g = 130}),
      40,
      text_s
    )
  );
  text_layer_set_font(s_day_in_month_layer, scl_get_font(SFI_MediumBold));
  text_layer_set_text_color(s_day_in_month_layer, month_day_color);
  text_layer_set_text_alignment(s_day_in_month_layer, GTextAlignmentCenter);
  text_layer_set_background_color(s_day_in_month_layer, GColorClear);
  s_full_day_frame = layer_get_frame(text_layer_get_layer(s_day_in_month_layer));

  s_month_layer = text_layer_create(
    GRect(x_offset, y_offset + scl_y_pp({.o = 260, .e = 250, .g = 250}), text_s, text_s)
  );
  text_layer_set_font(s_month_layer, scl_get_font(SFI_SmallBold));
  text_layer_set_text_color(s_month_layer, date_color);
  text_layer_set_background_color(s_month_layer, GColorClear);

  s_slots_layer = layer_create(bounds);
  layer_set_update_proc(s_slots_layer, slots_update_proc);

  s_canvas_layer = layer_create(bounds);
  layer_set_update_proc(s_canvas_layer, draw_proc);
}

static void window_unload(Window *window) {
  health_set_update_handler(NULL);
#if defined(PBL_TOUCH)
  touch_service_unsubscribe();
#endif
#if defined(PBL_RECT) && !defined(PBL_PLATFORM_APLITE)
  unobstructed_area_service_unsubscribe();
#endif
  layer_destroy(s_canvas_layer);
  layer_destroy(s_bg_layer);
  layer_destroy(s_slots_layer);

  text_layer_destroy(s_weekday_layer);
  text_layer_destroy(s_day_in_month_layer);
  text_layer_destroy(s_month_layer);

  window_destroy(s_main_window);
}

static int anim_percentage(AnimationProgress dist_normalized, int max) {
  return (max * dist_normalized) / ANIMATION_NORMALIZED_MAX;
}

static void hands_update(Animation *anim, AnimationProgress dist_normalized) {
  s_current_time.hours -= (s_current_time.hours > 12) ? 12 : 0;

  s_anim_time.hours = anim_percentage(dist_normalized, hours_to_minutes(s_current_time.hours));
  s_anim_time.minutes = anim_percentage(dist_normalized, s_current_time.minutes);
  s_anim_time.seconds = anim_percentage(dist_normalized, s_current_time.seconds);

  layer_mark_dirty(s_canvas_layer);
}

/************************************ API *************************************/

void main_window_push() {
  GColor bg_color = data_get_color(MESSAGE_KEY_ColorBackground);

  s_main_window = window_create();
  window_set_background_color(s_main_window, bg_color);
  window_set_window_handlers(s_main_window, (WindowHandlers) {
    .load = window_load,
    .unload = window_unload,
  });
  window_stack_push(s_main_window, true);
#if defined(PBL_RECT) && !defined(PBL_PLATFORM_APLITE)
  unobstructed_area_service_subscribe((UnobstructedAreaHandlers) {
    .did_change = unobstructed_did_change
  }, NULL);
#endif

  // Begin smooth animation
  static AnimationImplementation hands_impl = {
    .update = hands_update
  };
  s_animating = false;
  if (data_get_enable(MESSAGE_KEY_EnableStartupAnim)) {
    animate(ANIMATION_DURATION, ANIMATION_DELAY, &hands_impl, true);
  }

  main_window_reload_config();
  show_seconds();
}

void main_window_reload_config() {
  health_set_update_handler(main_window_refresh_data);
  // Health may have been enabled after launch
  if (slots_uses(SlotTypeSteps) || slots_uses(SlotTypeHeartRate) ||
      slots_uses(SlotTypeDistance) || slots_uses(SlotTypeActiveCalories) ||
      data_get_enable(MESSAGE_KEY_EnableStepRing)) {
    health_init();
  }

  update_time();

  accel_tap_service_unsubscribe();
  if (data_get_enable(MESSAGE_KEY_EnableSecondHand)) {
    accel_tap_service_subscribe(accel_tap_handler);
  } else {
    s_show_seconds = false;
    if (s_seconds_timer) {
      app_timer_cancel(s_seconds_timer);
      s_seconds_timer = NULL;
    }
  }
  subscribe_tick();

#if defined(PBL_TOUCH)
  update_touch_subscription();
#endif

  connection_service_unsubscribe();
  if (data_get_enable(MESSAGE_KEY_EnableBT)) {
    connection_service_subscribe((ConnectionHandlers) {
      .pebble_app_connection_handler = bt_handler
    });
    bt_handler(connection_service_peek_pebble_app_connection());
  }

  battery_state_service_unsubscribe();
  if (data_get_enable(MESSAGE_KEY_EnableBattery) || slots_uses(SlotTypeBattery)) {
    battery_state_service_subscribe(batt_handler);
  }

  GColor bg_color = data_get_color(MESSAGE_KEY_ColorBackground);
  GColor date_color = data_get_color(MESSAGE_KEY_ColorDate);
  GColor month_day_color = data_get_color(MESSAGE_KEY_ColorMonthDay);

  window_set_background_color(s_main_window, bg_color);
  if (s_bg_layer) layer_mark_dirty(s_bg_layer);
  text_layer_set_text_color(s_weekday_layer, date_color);
  text_layer_set_text_color(s_day_in_month_layer, month_day_color);
  text_layer_set_text_color(s_month_layer, date_color);

  Layer *window_layer = window_get_root_layer(s_main_window);
  layer_remove_from_parent(text_layer_get_layer(s_day_in_month_layer));
  layer_remove_from_parent(text_layer_get_layer(s_weekday_layer));
  layer_remove_from_parent(text_layer_get_layer(s_month_layer));
  layer_remove_from_parent(s_slots_layer);
  const DateStyle date_style = data_get_date_style();
  GRect day_frame = s_full_day_frame;
  if (date_style == DateStyleDayOnly) {
    // Center the visible numeral, accounting for each font's top bearing.
#if defined(PBL_PLATFORM_EMERY) || defined(PBL_PLATFORM_GABBRO)
    const int numeral_center = 19;
#else
    const int numeral_center = 15;
#endif
    day_frame.origin.y = layer_get_bounds(window_layer).size.h / 2 - numeral_center;
  }
  layer_set_frame(text_layer_get_layer(s_day_in_month_layer), day_frame);
  if (data_get_enable(MESSAGE_KEY_EnableDate)) {
    layer_add_child(window_layer, text_layer_get_layer(s_day_in_month_layer));
    if (date_style != DateStyleDayOnly) layer_add_child(window_layer, text_layer_get_layer(s_weekday_layer));
    if (date_style == DateStyleFull) layer_add_child(window_layer, text_layer_get_layer(s_month_layer));
  }
  layer_add_child(window_layer, s_slots_layer);

  layer_add_child(window_layer, s_canvas_layer);
  refresh_poll();
}


void main_window_refresh_data(void) {
  if (s_slots_layer) layer_mark_dirty(s_slots_layer);
  if (s_bg_layer && data_get_enable(MESSAGE_KEY_EnableStepRing)) layer_mark_dirty(s_bg_layer);
}
