#include "data.h"

#define SK_AppConfig 0

#define SK_MIGRATION_1 50

typedef struct {
  bool enable_date;
  bool enable_bt;
  bool enable_battery;
  bool enable_second_hand;
  bool enable_steps; // Unused, replaced by slots

  GColor color_background;
  GColor color_hour_minutes;
  GColor color_seconds;
  GColor color_notches;
  GColor color_month_day;
  GColor color_date;

  // Append only, older saved configs are a prefix of this struct
  uint8_t slot_top;
  uint8_t slot_left;
  uint8_t slot_bottom;
  bool enable_thick_hands;
  GColor color_hand_tips;
  GColor color_center_dot;
} AppConfig;

// Cache for speed
static AppConfig s_app_config;

static void save_all() {
  status_t result = persist_write_data(SK_AppConfig, &s_app_config, sizeof(AppConfig));
  if (result < 0) {
    APP_LOG(APP_LOG_LEVEL_ERROR, "Error writing app config: %d", (int)result);
  } else {
    APP_LOG(APP_LOG_LEVEL_INFO, "App config saved");
  }
}

void data_init() {
  // When color options were added we needed to start again
  if (!persist_exists(SK_MIGRATION_1)) {
    persist_delete(SK_AppConfig);
    persist_write_int(SK_MIGRATION_1, 1);
  }

  // Set before reading so configs saved before slots existed keep these
  s_app_config.slot_top = SlotTypeNone;
  s_app_config.slot_left = SlotTypeNone;
  s_app_config.slot_bottom = SlotTypeSteps;
  s_app_config.enable_thick_hands = false;
  s_app_config.color_hand_tips = GColorClear;
  s_app_config.color_center_dot = GColorClear;

  if(!persist_exists(SK_AppConfig)) {
    // Set defaults
    s_app_config.enable_date = true;
    s_app_config.enable_bt = true;
    s_app_config.enable_battery = true;
    s_app_config.enable_second_hand = true;
    s_app_config.enable_steps = true;

    s_app_config.color_background = GColorBlack;
    s_app_config.color_hour_minutes = PBL_IF_COLOR_ELSE(GColorLightGray, GColorWhite);
    s_app_config.color_seconds = PBL_IF_COLOR_ELSE(GColorDarkCandyAppleRed, GColorWhite);
    s_app_config.color_notches = GColorWhite;
    s_app_config.color_month_day = PBL_IF_COLOR_ELSE(GColorChromeYellow, GColorWhite);
    s_app_config.color_date = GColorWhite;

    save_all();
  } else {
    status_t result = persist_read_data(SK_AppConfig, &s_app_config, sizeof(AppConfig));
    if (result < 0) {
      APP_LOG(APP_LOG_LEVEL_ERROR, "Error reading app config: %d", (int)result);
    } else {
      APP_LOG(APP_LOG_LEVEL_INFO, "App config loaded");
    }
  }

  // Hand tips used to share the notches color, and the center dot the hand tips
  if (gcolor_equal(s_app_config.color_hand_tips, GColorClear)) {
    s_app_config.color_hand_tips = s_app_config.color_notches;
  }
  if (gcolor_equal(s_app_config.color_center_dot, GColorClear)) {
    s_app_config.color_center_dot = s_app_config.color_hand_tips;
  }
}

void data_deinit() {
  save_all();
}

void data_set_enable(uint32_t key, bool b) {
  // Can't use switch with MESSAGE_KEY_ constants directly
  if (key == MESSAGE_KEY_EnableDate) {
    s_app_config.enable_date = b;
  } else if (key == MESSAGE_KEY_EnableBT) {
    s_app_config.enable_bt = b;
  } else if (key == MESSAGE_KEY_EnableBattery) {
    s_app_config.enable_battery = b;
  } else if (key == MESSAGE_KEY_EnableSecondHand) {
    s_app_config.enable_second_hand = b;
  } else if (key == MESSAGE_KEY_EnableSteps) {
    s_app_config.enable_steps = b;
  } else if (key == MESSAGE_KEY_EnableThickHands) {
    s_app_config.enable_thick_hands = b;
  }
}

bool data_get_enable(uint32_t key) {
  if (key == MESSAGE_KEY_EnableDate) {
    return s_app_config.enable_date;
  } else if (key == MESSAGE_KEY_EnableBT) {
    return s_app_config.enable_bt;
  } else if (key == MESSAGE_KEY_EnableBattery) {
    return s_app_config.enable_battery;
  } else if (key == MESSAGE_KEY_EnableSecondHand) {
    return s_app_config.enable_second_hand;
  } else if (key == MESSAGE_KEY_EnableSteps) {
    return s_app_config.enable_steps;
  } else if (key == MESSAGE_KEY_EnableThickHands) {
    return s_app_config.enable_thick_hands;
  }

  return false;
}

void data_set_color(uint32_t key, GColor color) {
  if (key == MESSAGE_KEY_ColorBackground) {
    s_app_config.color_background = color;
  } else if (key == MESSAGE_KEY_ColorHourMinutes) {
    s_app_config.color_hour_minutes = color;
  } else if (key == MESSAGE_KEY_ColorSeconds) {
    s_app_config.color_seconds = color;
  } else if (key == MESSAGE_KEY_ColorNotches) {
    s_app_config.color_notches = color;
  } else if (key == MESSAGE_KEY_ColorMonthDay) {
    s_app_config.color_month_day = color;
  } else if (key == MESSAGE_KEY_ColorDate) {
    s_app_config.color_date = color;
  } else if (key == MESSAGE_KEY_ColorHandTips) {
    s_app_config.color_hand_tips = color;
  } else if (key == MESSAGE_KEY_ColorCenterDot) {
    s_app_config.color_center_dot = color;
  }
}

GColor data_get_color(uint32_t key) {
  if (key == MESSAGE_KEY_ColorBackground) {
    return s_app_config.color_background;
  } else if (key == MESSAGE_KEY_ColorHourMinutes) {
    return s_app_config.color_hour_minutes;
  } else if (key == MESSAGE_KEY_ColorSeconds) {
    return s_app_config.color_seconds;
  } else if (key == MESSAGE_KEY_ColorNotches) {
    return s_app_config.color_notches;
  } else if (key == MESSAGE_KEY_ColorMonthDay) {
    return s_app_config.color_month_day;
  } else if (key == MESSAGE_KEY_ColorDate) {
    return s_app_config.color_date;
  } else if (key == MESSAGE_KEY_ColorHandTips) {
    return s_app_config.color_hand_tips;
  } else if (key == MESSAGE_KEY_ColorCenterDot) {
    return s_app_config.color_center_dot;
  }

  return GColorBlack;
}

void data_set_slot(uint32_t key, SlotType type) {
  if (key == MESSAGE_KEY_SlotTop) {
    s_app_config.slot_top = type;
  } else if (key == MESSAGE_KEY_SlotLeft) {
    s_app_config.slot_left = type;
  } else if (key == MESSAGE_KEY_SlotBottom) {
    s_app_config.slot_bottom = type;
  }
}

SlotType data_get_slot(uint32_t key) {
  int type = SlotTypeNone;
  if (key == MESSAGE_KEY_SlotTop) {
    type = s_app_config.slot_top;
  } else if (key == MESSAGE_KEY_SlotLeft) {
    type = s_app_config.slot_left;
  } else if (key == MESSAGE_KEY_SlotBottom) {
    type = s_app_config.slot_bottom;
  }

  return (type < SlotTypeCount) ? type : SlotTypeNone;
}
