#include "slots.h"
#include "format.h"
#include "weather.h"

#define VALUE_HEIGHT scl_y_pp({.o = 170, .c = 160, .e = 145, .g = 140})
#define LOW_BATTERY_PERCENT 20

static void get_slot_text(SlotType type, char *value, size_t size) {
  switch (type) {
    case SlotTypeSteps:
      snprintf(value, size, "%d", health_get_step_count());
      break;
    case SlotTypeHeartRate: {
      const int bpm = health_get_heart_rate();
      if (bpm > 0) {
        snprintf(value, size, "%d", bpm);
      } else {
        snprintf(value, size, "--");
      }
      break;
    }
    case SlotTypeBattery:
      snprintf(value, size, "%d%%", battery_state_service_peek().charge_percent);
      break;
    case SlotTypeDistance: {
      const int tenths = health_get_distance_tenths();
      snprintf(value, size, "%d.%d", tenths / 10, tenths % 10);
      break;
    }
    case SlotTypeActiveCalories:
      snprintf(value, size, "%d", health_get_active_calories());
      break;
    case SlotTypeWeek: {
      time_t now = time(NULL);
      snprintf(value, size, "W%02d", format_iso_week(localtime(&now)));
      break;
    }
    case SlotTypeTime:
    case SlotTypeSecondTime: {
      time_t now = time(NULL);
      if (type == SlotTypeSecondTime) {
        int offset;
        if (!data_get_timezone(&offset)) { value[0] = '\0'; break; }
        now += offset * 60;
        format_clock(value, size, gmtime(&now), clock_is_24h_style());
      } else {
        format_clock(value, size, localtime(&now), clock_is_24h_style());
      }
      break;
    }
    case SlotTypeWeather: {
      int temperature;
      if (weather_get_temperature(&temperature)) snprintf(value, size, "%d°", temperature);
      else value[0] = '\0'; // Approved design: stale/unavailable weather stays blank.
      break;
    }
    default:
      value[0] = '\0';
      break;
  }
}

static void draw_slot(GContext *ctx, uint32_t key, GRect value_rect) {
  const SlotType type = data_get_slot(key);
  if (type == SlotTypeNone) return;
  if (type == SlotTypeBattery && data_get_enable(MESSAGE_KEY_BatteryOnlyWhenLow) &&
      battery_state_service_peek().charge_percent >= LOW_BATTERY_PERCENT) return;
  if ((type == SlotTypeSteps || type == SlotTypeHeartRate ||
       type == SlotTypeDistance || type == SlotTypeActiveCalories) && !health_is_health_available()) return;

  if (type == SlotTypeHeartRate && !health_is_heart_rate_available()) return;

  static char s_value[16];
  get_slot_text(type, s_value, sizeof(s_value));

  if (!s_value[0]) return;
  graphics_draw_text(ctx, s_value, scl_get_font(SFI_MediumBold), value_rect,
    GTextOverflowModeFill, GTextAlignmentCenter, NULL);
}

/************************************ API *************************************/

bool slots_uses(SlotType type) {
  return data_get_slot(MESSAGE_KEY_SlotTop) == type ||
    data_get_slot(MESSAGE_KEY_SlotLeft) == type ||
    data_get_slot(MESSAGE_KEY_SlotBottom) == type;
}

void slots_draw(GContext *ctx, bool bottom_visible) {
  graphics_context_set_text_color(ctx, data_get_color(MESSAGE_KEY_ColorDate));

  // Top, left mirrors the date column on the right, bottom
  draw_slot(ctx, MESSAGE_KEY_SlotTop, GRect(0, scl_y(130), PS_DISP_W, VALUE_HEIGHT));
  draw_slot(ctx, MESSAGE_KEY_SlotLeft, GRect(0, scl_y(420), scl_x(430), VALUE_HEIGHT));
  if (bottom_visible) {
    draw_slot(ctx, MESSAGE_KEY_SlotBottom, GRect(0, scl_y(690), PS_DISP_W, VALUE_HEIGHT));
  }
}
