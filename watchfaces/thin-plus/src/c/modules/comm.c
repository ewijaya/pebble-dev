#include "comm.h"

// Clay sends select values as strings
static SlotType get_slot(DictionaryIterator *iter, uint32_t key) {
  Tuple *t = dict_find(iter, key);
  if (!t) return SlotTypeNone;

  return (t->type == TUPLE_CSTRING) ? atoi(t->value->cstring) : (int)t->value->int32;
}

static void in_recv_handler(DictionaryIterator *iter, void *context) {
  (void)context;
  APP_LOG(APP_LOG_LEVEL_INFO, "Config message received");

  // Capability-filtered Clay pages and older pages may send only some keys.
  // Missing means "leave the saved value alone", including false/zero values.
  const uint32_t toggles[] = {
    MESSAGE_KEY_EnableDate, MESSAGE_KEY_EnableBT, MESSAGE_KEY_EnableBattery,
    MESSAGE_KEY_EnableSecondHand, MESSAGE_KEY_EnableSteps,
    MESSAGE_KEY_EnableThickHands, MESSAGE_KEY_BatteryOnlyWhenLow,
    MESSAGE_KEY_VibrateOnDisconnect, MESSAGE_KEY_EnableEnhancedBT, MESSAGE_KEY_TapForSeconds,
    MESSAGE_KEY_EnableChargingColor, MESSAGE_KEY_EnableStartupAnim
  };
  const uint32_t slots[] = {
    MESSAGE_KEY_SlotTop, MESSAGE_KEY_SlotLeft, MESSAGE_KEY_SlotBottom
  };
  const uint32_t colors[] = {
    MESSAGE_KEY_ColorBackground, MESSAGE_KEY_ColorHourMinutes,
    MESSAGE_KEY_ColorSeconds, MESSAGE_KEY_ColorNotches, MESSAGE_KEY_ColorHandTips,
    MESSAGE_KEY_ColorCenterDot, MESSAGE_KEY_ColorSecondTip,
    MESSAGE_KEY_ColorBatteryEmpty, MESSAGE_KEY_ColorMonthDay, MESSAGE_KEY_ColorDate,
    MESSAGE_KEY_ColorDisconnected, MESSAGE_KEY_ColorCharging
  };
  for (size_t i = 0; i < ARRAY_LENGTH(toggles); i++) {
    if (dict_find(iter, toggles[i])) {
      data_set_enable(toggles[i], packet_get_boolean(iter, toggles[i]));
    }
  }
  for (size_t i = 0; i < ARRAY_LENGTH(slots); i++) {
    if (dict_find(iter, slots[i])) data_set_slot(slots[i], get_slot(iter, slots[i]));
  }
  for (size_t i = 0; i < ARRAY_LENGTH(colors); i++) {
    if (dict_find(iter, colors[i])) {
      data_set_color(colors[i], GColorFromHEX(packet_get_integer(iter, colors[i])));
    }
  }

  main_window_reload_config();
}

void comm_init() {
  packet_init();

  app_message_register_inbox_received(in_recv_handler);
  // Room for a complete settings dictionary; partial updates are also accepted
  app_message_open(512, 64);
}
