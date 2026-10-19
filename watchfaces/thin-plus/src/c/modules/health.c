#include "health.h"
#include "data.h"

static bool s_health_available;
static int s_step_count = 0;
static int s_heart_rate = 0;
static int s_distance_tenths, s_active_calories;
static int s_step_goal = 7500;
static time_t s_activity_day;
static void (*s_update_handler)(void);

static void update_activity(void) {
#if defined(PBL_HEALTH)
  s_step_count = (int)health_service_sum_today(HealthMetricStepCount);
  const int meters = (int)health_service_sum_today(HealthMetricWalkedDistanceMeters);
  const bool imperial = health_service_get_measurement_system_for_display(
    HealthMetricWalkedDistanceMeters) == MeasurementSystemImperial;
  // Integer arithmetic avoids unsupported floating-point printf on the watch.
  s_distance_tenths = imperial ? (int)(((int64_t)meters * 10000 + 804672) / 1609344) : (meters + 50) / 100;
  s_active_calories = (int)health_service_sum_today(HealthMetricActiveKCalories);
  const time_t start = time_start_of_today();
  s_activity_day = start;
  int goal = 0;
  if (health_service_metric_averaged_accessible(HealthMetricStepCount, start,
      start + SECONDS_PER_DAY, HealthServiceTimeScopeDaily) & HealthServiceAccessibilityMaskAvailable) {
    goal = (int)health_service_sum_averaged(HealthMetricStepCount, start,
      start + SECONDS_PER_DAY, HealthServiceTimeScopeDaily);
  }
  s_step_goal = goal > 0 ? goal : 7500;
#endif
}

static void ensure_activity_day(void) {
  if (s_health_available && s_activity_day != time_start_of_today()) update_activity();
}

void health_set_update_handler(void (*handler)(void)) { s_update_handler = handler; }

static void update_heart_rate() {
#if defined(PBL_HEALTH)
  const time_t now = time(NULL);
  if (health_service_metric_accessible(HealthMetricHeartRateBPM, now, now) &
      HealthServiceAccessibilityMaskAvailable) {
    s_heart_rate = (int)health_service_peek_current_value(HealthMetricHeartRateBPM);
  }
#endif
}

static void health_handler(HealthEventType event, void *context) {
  (void)context;
  if(event != HealthEventSleepUpdate) {
    update_activity();
  }
  if (event == HealthEventHeartRateUpdate) {
    update_heart_rate();
  }
  if (s_update_handler) s_update_handler();
}

void health_init() {
  if (s_health_available) return;

  s_health_available = health_service_events_subscribe(health_handler, NULL);

  if (s_health_available) {
    update_activity();
    update_heart_rate();
  }
}

bool health_is_health_available() {
  return s_health_available;
}

int health_get_step_count() {
  ensure_activity_day();
  return s_step_count;
}

int health_get_heart_rate() {
  return s_heart_rate;
}

bool health_step_data_is_available() {
  return health_is_health_available() && (HealthServiceAccessibilityMaskAvailable &
    health_service_metric_accessible(HealthMetricStepCount, time_start_of_today(), time(NULL)));
}

bool health_is_heart_rate_available() {
  // These models never shipped with a heart-rate sensor. Their emulator can
  // report an accessible metric despite having no sensor, so exclude them too.
#if defined(PBL_PLATFORM_BASALT) || defined(PBL_PLATFORM_CHALK)
  return false;
#elif defined(PBL_HEALTH)
  const time_t now = time(NULL);
  return s_health_available &&
    (health_service_metric_accessible(HealthMetricHeartRateBPM, now, now) &
      HealthServiceAccessibilityMaskAvailable);
#else
  return false;
#endif
}

int health_get_distance_tenths(void) { ensure_activity_day(); return s_distance_tenths; }
int health_get_active_calories(void) { ensure_activity_day(); return s_active_calories; }
int health_get_step_goal(void) {
  if (data_get_step_goal_mode() == StepGoalCustom) return data_get_custom_step_goal();
  ensure_activity_day();
  return s_step_goal;
}
