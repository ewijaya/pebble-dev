#pragma once

#include <pebble.h>

#include "data.h"

void health_init();

bool health_is_health_available();

int health_get_step_count();

int health_get_heart_rate();

bool health_is_heart_rate_available();

bool health_step_data_is_available();

int health_get_distance_tenths(void);
int health_get_active_calories(void);
int health_get_step_goal(void);

void health_set_update_handler(void (*handler)(void));
