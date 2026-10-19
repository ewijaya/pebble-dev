#include "slots.h"

#define VALUE_HEIGHT scl_y_pp({.o = 170, .c = 160, .e = 145, .g = 140})
#define UNIT_HEIGHT  scl_y_pp({.o = 120, .c = 110, .e = 110, .g = 110})

static void get_slot_text(SlotType type, char *value, size_t size, const char **unit) {
  switch (type) {
    case SlotTypeSteps:
      snprintf(value, size, "%d", health_get_step_count());
      *unit = "steps";
      break;
    case SlotTypeHeartRate: {
      const int bpm = health_get_heart_rate();
      if (bpm > 0) {
        snprintf(value, size, "%d", bpm);
      } else {
        snprintf(value, size, "--");
      }
      *unit = "bpm";
      break;
    }
    case SlotTypeBattery: {
      BatteryChargeState state = battery_state_service_peek();
      snprintf(value, size, "%d%%", state.charge_percent);
      *unit = state.is_charging ? "charging" : "";
      break;
    }
    case SlotTypeTime: {
      time_t t = time(NULL);
      struct tm *now = localtime(&t);
      if (clock_is_24h_style()) {
        strftime(value, size, "%H:%M", now);
        *unit = "";
      } else {
        const int hour = (now->tm_hour % 12 == 0) ? 12 : (now->tm_hour % 12);
        snprintf(value, size, "%d:%02d", hour, now->tm_min);
        *unit = (now->tm_hour < 12) ? "am" : "pm";
      }
      break;
    }
    default:
      value[0] = '\0';
      *unit = "";
      break;
  }
}

static void draw_slot(GContext *ctx, uint32_t key, GRect value_rect) {
  const SlotType type = data_get_slot(key);
  if (type == SlotTypeNone) return;
  if ((type == SlotTypeSteps || type == SlotTypeHeartRate) && !health_is_health_available()) return;

  static char s_value[16];
  const char *unit;
  get_slot_text(type, s_value, sizeof(s_value), &unit);

  GRect unit_rect = GRect(
    value_rect.origin.x, value_rect.origin.y + value_rect.size.h, value_rect.size.w, UNIT_HEIGHT
  );

  graphics_draw_text(ctx, s_value, scl_get_font(SFI_MediumBold), value_rect,
    GTextOverflowModeFill, GTextAlignmentCenter, NULL);
  graphics_draw_text(ctx, unit, scl_get_font(SFI_SmallBold), unit_rect,
    GTextOverflowModeFill, GTextAlignmentCenter, NULL);
}

/************************************ API *************************************/

bool slots_uses(SlotType type) {
  return data_get_slot(MESSAGE_KEY_SlotTop) == type ||
    data_get_slot(MESSAGE_KEY_SlotLeft) == type ||
    data_get_slot(MESSAGE_KEY_SlotBottom) == type;
}

void slots_draw(GContext *ctx) {
  graphics_context_set_text_color(ctx, data_get_color(MESSAGE_KEY_ColorDate));

  // Top, left mirrors the date column on the right, bottom
  draw_slot(ctx, MESSAGE_KEY_SlotTop, GRect(0, scl_y(130), PS_DISP_W, VALUE_HEIGHT));
  draw_slot(ctx, MESSAGE_KEY_SlotLeft, GRect(0, scl_y(420), scl_x(430), VALUE_HEIGHT));
  draw_slot(ctx, MESSAGE_KEY_SlotBottom, GRect(0, scl_y(690), PS_DISP_W, VALUE_HEIGHT));
}
