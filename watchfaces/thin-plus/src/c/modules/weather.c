#include "weather.h"
#include "data.h"

#define SK_WEATHER 51
#define WEATHER_REFRESH_SECONDS (30 * 60)
#define WEATHER_MAX_AGE_SECONDS (3 * 60 * 60)

typedef struct {
  int32_t temperature, code, timestamp;
  int32_t units;
} WeatherCache;
static WeatherCache s_weather;

static bool valid_at(time_t now, int max_age) {
  return s_weather.timestamp > 0 && now >= s_weather.timestamp &&
    now - s_weather.timestamp <= max_age && s_weather.units == data_get_weather_units();
}

void weather_init(void) {
  memset(&s_weather, 0, sizeof(s_weather));
  if (persist_get_size(SK_WEATHER) == sizeof(s_weather)) {
    if (persist_read_data(SK_WEATHER, &s_weather, sizeof(s_weather)) != sizeof(s_weather)) {
      memset(&s_weather, 0, sizeof(s_weather));
    }
  }
}

void weather_store(int temperature, int code, int units) {
  // A delayed response to a previous units setting must not relabel old data.
  if (units != data_get_weather_units() || temperature < -150 || temperature > 180 || code < 0 || code > 99) return;
  s_weather = (WeatherCache){temperature, code, (int32_t)time(NULL), units};
  APP_LOG(APP_LOG_LEVEL_INFO, "Weather update: %d, units=%d", temperature, units);
  if (persist_write_data(SK_WEATHER, &s_weather, sizeof(s_weather)) < 0) {
    APP_LOG(APP_LOG_LEVEL_ERROR, "Weather cache save failed");
  }
}

bool weather_get_temperature(int *temperature) {
  if (!valid_at(time(NULL), WEATHER_MAX_AGE_SECONDS)) return false;
  *temperature = s_weather.temperature;
  return true;
}

bool weather_needs_update(time_t now) {
  return !valid_at(now, WEATHER_REFRESH_SECONDS - 1);
}
