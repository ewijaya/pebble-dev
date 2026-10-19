#include "health.h"

static bool s_health_available;
static int s_step_count = 0;
static int s_heart_rate = 0;

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
  if(event != HealthEventSleepUpdate) {
    s_step_count = (int)health_service_sum_today(HealthMetricStepCount);
  }
  if (event == HealthEventHeartRateUpdate) {
    update_heart_rate();
  }
}

void health_init() {
  if (s_health_available) return;

  s_health_available = health_service_events_subscribe(health_handler, NULL);

  if (s_health_available) {
    s_step_count = (int)health_service_sum_today(HealthMetricStepCount);
    update_heart_rate();
  }
}

bool health_is_health_available() {
  return s_health_available;
}

int health_get_step_count() {
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
