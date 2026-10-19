#pragma once
#include <pebble.h>

void weather_init(void);
void weather_store(int temperature, int code, int units);
bool weather_get_temperature(int *temperature);
bool weather_needs_update(time_t now);
