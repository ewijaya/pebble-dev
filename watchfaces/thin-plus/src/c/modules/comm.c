#include "comm.h"
#include "weather.h"
#include "refresh.h"

// Bounded decimal parsing: no fractions, signs, overflow or atoi truncation.
static bool goal_integer(Tuple *tuple, int min, int max, int *result) {
  if (tuple->type == TUPLE_CSTRING) {
    const char *text = tuple->value->cstring;
    if (!tuple->length || memchr(text, '\0', tuple->length) != text + tuple->length - 1) return false;
    int value = 0;
    if (!*text) return false;
    for (uint16_t i = 0; i < tuple->length - 1; i++) {
      if (text[i] < '0' || text[i] > '9') return false;
      int digit = text[i] - '0';
      if (value > (max - digit) / 10 || digit > max) return false;
      value = value * 10 + digit;
    }
    if (value < min || value > max) return false;
    *result = value;
    return true;
  }
  if ((tuple->type != TUPLE_INT && tuple->type != TUPLE_UINT) || tuple->length != 4) return false;
  if (tuple->type == TUPLE_UINT && tuple->value->uint32 > (uint32_t)max) return false;
  const int value = tuple->value->int32;
  if (value < min || value > max) return false;
  *result = value;
  return true;
}

// Clay sends select values as strings
static SlotType get_slot(DictionaryIterator *iter, uint32_t key) {
  Tuple *t = dict_find(iter, key);
  if (!t) return SlotTypeNone;

  return (t->type == TUPLE_CSTRING) ? atoi(t->value->cstring) : (int)t->value->int32;
}

static void in_recv_handler(DictionaryIterator *iter, void *context) {
  (void)context;
  APP_LOG(APP_LOG_LEVEL_INFO, "Config message received");

  // Live data does not reapply settings or restart watch services.
  if (dict_find(iter, MESSAGE_KEY_WeatherTemp) && dict_find(iter, MESSAGE_KEY_WeatherCode) &&
      dict_find(iter, MESSAGE_KEY_WeatherUnits)) {
    weather_store(packet_get_integer(iter, MESSAGE_KEY_WeatherTemp),
      packet_get_integer(iter, MESSAGE_KEY_WeatherCode), packet_get_integer(iter, MESSAGE_KEY_WeatherUnits));
    main_window_refresh_data();
    return;
  }
  if (dict_find(iter, MESSAGE_KEY_PhoneReady)) {
    refresh_phone_ready();
    return;
  }
  bool settings_changed = false;
  Tuple *goal_mode = dict_find(iter, MESSAGE_KEY_StepGoalMode);
  Tuple *custom_goal = dict_find(iter, MESSAGE_KEY_CustomStepGoal);
  int mode = data_get_step_goal_mode(), goal = data_get_custom_step_goal();
  // Reject a malformed goal packet before applying any settings in it.
  if ((goal_mode && !goal_integer(goal_mode, StepGoalAutomatic, StepGoalCustom, &mode)) ||
      (custom_goal && !goal_integer(custom_goal, STEP_GOAL_MIN, STEP_GOAL_MAX, &goal))) {
    APP_LOG(APP_LOG_LEVEL_ERROR, "Invalid step goal; settings unchanged");
    return;
  }
  if (goal_mode) { data_set_step_goal_mode(mode); settings_changed = true; }
  if (custom_goal) { data_set_custom_step_goal(goal); settings_changed = true; }
  if (dict_find(iter, MESSAGE_KEY_DateStyle)) {
    Tuple *style = dict_find(iter, MESSAGE_KEY_DateStyle);
    data_set_date_style(style->type == TUPLE_CSTRING ? atoi(style->value->cstring) : style->value->int32);
    settings_changed = true;
  }
  if (dict_find(iter, MESSAGE_KEY_TzOffsetMinutes)) {
    data_set_timezone(packet_get_integer(iter, MESSAGE_KEY_TzOffsetMinutes));
    main_window_refresh_data();
  }
  if (dict_find(iter, MESSAGE_KEY_WeatherUnits)) {
    Tuple *units = dict_find(iter, MESSAGE_KEY_WeatherUnits);
    data_set_weather_units(units->type == TUPLE_CSTRING ? atoi(units->value->cstring) : units->value->int32);
    settings_changed = true;
  }
  // Capability-filtered Clay pages and older pages may send only some keys.
  // Missing means "leave the saved value alone", including false/zero values.
  const uint32_t toggles[] = {
    MESSAGE_KEY_EnableDate, MESSAGE_KEY_EnableBT, MESSAGE_KEY_EnableBattery,
    MESSAGE_KEY_EnableSecondHand, MESSAGE_KEY_EnableSteps,
    MESSAGE_KEY_EnableThickHands, MESSAGE_KEY_BatteryOnlyWhenLow,
    MESSAGE_KEY_VibrateOnDisconnect, MESSAGE_KEY_EnableEnhancedBT, MESSAGE_KEY_TapForSeconds,
    MESSAGE_KEY_EnableChargingColor, MESSAGE_KEY_EnableStartupAnim, MESSAGE_KEY_EnableStepRing
  };
  const uint32_t slots[] = {
    MESSAGE_KEY_SlotTop, MESSAGE_KEY_SlotLeft, MESSAGE_KEY_SlotBottom
  };
  const uint32_t colors[] = {
    MESSAGE_KEY_ColorBackground, MESSAGE_KEY_ColorHourMinutes,
    MESSAGE_KEY_ColorSeconds, MESSAGE_KEY_ColorNotches, MESSAGE_KEY_ColorHandTips,
    MESSAGE_KEY_ColorCenterDot, MESSAGE_KEY_ColorSecondTip,
    MESSAGE_KEY_ColorBatteryEmpty, MESSAGE_KEY_ColorMonthDay, MESSAGE_KEY_ColorDate,
    MESSAGE_KEY_ColorDisconnected, MESSAGE_KEY_ColorCharging, MESSAGE_KEY_ColorStepRing
  };
  for (size_t i = 0; i < ARRAY_LENGTH(toggles); i++) {
    if (dict_find(iter, toggles[i])) {
      settings_changed = true;
      data_set_enable(toggles[i], packet_get_boolean(iter, toggles[i]));
    }
  }
  for (size_t i = 0; i < ARRAY_LENGTH(slots); i++) {
    if (dict_find(iter, slots[i])) {
      settings_changed = true;
      data_set_slot(slots[i], get_slot(iter, slots[i]));
    }
  }
  for (size_t i = 0; i < ARRAY_LENGTH(colors); i++) {
    if (dict_find(iter, colors[i])) {
      settings_changed = true;
      data_set_color(colors[i], GColorFromHEX(packet_get_integer(iter, colors[i])));
    }
  }

  if (settings_changed) {
    main_window_reload_config();
    refresh_phone_ready();
  }
}

void comm_init() {
  packet_init();

  app_message_register_inbox_received(in_recv_handler);
  // Room for a complete settings dictionary; partial updates are also accepted
  app_message_open(512, 64);
}
