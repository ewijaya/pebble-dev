#pragma once

#include <pebble.h>

// Persisted and sent by config.js - only ever append new types
typedef enum {
  SlotTypeNone = 0,
  SlotTypeSteps,
  SlotTypeHeartRate,
  SlotTypeBattery,
  SlotTypeTime,

  SlotTypeDistance = 5,
  SlotTypeActiveCalories = 6,
  SlotTypeWeek = 7,
  SlotTypeSecondTime = 8,
  SlotTypeWeather = 9,

  SlotTypeCount
} SlotType;

typedef enum {
  DateStyleFull = 0,
  DateStyleDayOnly = 1,
  DateStyleWeekdayDay = 2
} DateStyle;

void data_init();

void data_deinit();

void data_set_enable(uint32_t key, bool b);

bool data_get_enable(uint32_t key);

void data_set_color(uint32_t key, GColor color);

GColor data_get_color(uint32_t key);

void data_set_slot(uint32_t key, SlotType type);

SlotType data_get_slot(uint32_t key);

void data_set_timezone(int offset_minutes);
bool data_get_timezone(int *offset_minutes);
void data_set_weather_units(int units);
int data_get_weather_units(void);
void data_set_date_style(int style);
DateStyle data_get_date_style(void);

enum { StepGoalAutomatic = 0, StepGoalCustom = 1 };
#define STEP_GOAL_DEFAULT 7500
#define STEP_GOAL_MIN 1000
#define STEP_GOAL_MAX 100000
void data_set_step_goal_mode(int mode);
int data_get_step_goal_mode(void);
void data_set_custom_step_goal(int goal);
int data_get_custom_step_goal(void);
