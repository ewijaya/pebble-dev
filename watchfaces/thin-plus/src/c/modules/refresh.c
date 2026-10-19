#include "refresh.h"
#include "data.h"
#include "slots.h"
#include "weather.h"

#define REFRESH_INTERVAL (30 * 60)
static time_t s_weather_request, s_timezone_request;

static bool due(time_t now, time_t last) {
  return !last || now < last || now - last >= REFRESH_INTERVAL;
}

void refresh_poll(void) {
  const time_t now = time(NULL);
  const bool weather = slots_uses(SlotTypeWeather) && weather_needs_update(now) && due(now, s_weather_request);
  const bool timezone = slots_uses(SlotTypeSecondTime) && due(now, s_timezone_request);
  if (!weather && !timezone) return;
  DictionaryIterator *iter;
  if (app_message_outbox_begin(&iter) != APP_MSG_OK || !iter) return;
  // Maximum dictionary: 1 + 3 * (7 + 4) = 34 bytes; outbox remains 64.
  if (weather) {
    dict_write_int32(iter, MESSAGE_KEY_WeatherRequest, 1);
    dict_write_int32(iter, MESSAGE_KEY_WeatherUnits, data_get_weather_units());
  }
  if (timezone) dict_write_int32(iter, MESSAGE_KEY_TimezoneRequest, 1);
  if (app_message_outbox_send() == APP_MSG_OK) {
    APP_LOG(APP_LOG_LEVEL_INFO, "Phone request: weather=%d, timezone=%d", weather, timezone);
    if (weather) s_weather_request = now;
    if (timezone) s_timezone_request = now;
  }
}

void refresh_phone_ready(void) {
  // Also called after settings changes: request updated units/zone immediately.
  s_weather_request = s_timezone_request = 0;
  refresh_poll();
}
