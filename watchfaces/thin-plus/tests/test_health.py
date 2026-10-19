#!/usr/bin/env python3
"""Health aggregation, distance units, daily goal fallback and midnight reset."""
from test_low_battery import run_harness
HEADER=r'''
#define PBL_HEALTH 1
#define SECONDS_PER_DAY 86400
typedef int HealthEventType;
typedef int HealthMetric;
enum {HealthEventSleepUpdate,HealthEventHeartRateUpdate,HealthEventMovementUpdate};
enum {HealthMetricStepCount,HealthMetricWalkedDistanceMeters,HealthMetricActiveKCalories,HealthMetricHeartRateBPM};
enum {MeasurementSystemImperial,MeasurementSystemMetric,HealthServiceTimeScopeDaily,HealthServiceAccessibilityMaskAvailable=8};
int health_service_sum_today(HealthMetric metric);
int health_service_get_measurement_system_for_display(HealthMetric metric);
int health_service_metric_averaged_accessible(HealthMetric metric,time_t start,time_t end,int scope);
int health_service_sum_averaged(HealthMetric metric,time_t start,time_t end,int scope);
int health_service_metric_accessible(HealthMetric metric,time_t start,time_t end);
int health_service_peek_current_value(HealthMetric metric);
bool health_service_events_subscribe(void (*handler)(HealthEventType,void *),void *context);
time_t time_start_of_today(void);
'''
TEST=r'''
#include <assert.h>
#include "src/c/modules/health.c"
static int sums[]={3750,10500,1234,72}, goal=7500,units=MeasurementSystemMetric,updates;
static int custom_goal=10000,mode=StepGoalAutomatic;
int data_get_step_goal_mode(void) {return mode;}
int data_get_custom_step_goal(void) {return custom_goal;}
static bool available=true,averaged=true;
static time_t day=1800000000;
static void updated(void) {updates++;}
time_t time_start_of_today(void) {return day;}
int health_service_sum_today(HealthMetric metric) {return sums[metric];}
int health_service_get_measurement_system_for_display(HealthMetric metric) {(void)metric;return units;}
int health_service_metric_averaged_accessible(HealthMetric metric,time_t start,time_t end,int scope) {
 assert(metric==HealthMetricStepCount && start==day && end==day+86400 && scope==HealthServiceTimeScopeDaily);return averaged?8:0;
}
int health_service_sum_averaged(HealthMetric metric,time_t start,time_t end,int scope) {(void)metric;(void)start;(void)end;(void)scope;return goal;}
int health_service_metric_accessible(HealthMetric metric,time_t start,time_t end) {(void)metric;(void)start;(void)end;return available?8:0;}
int health_service_peek_current_value(HealthMetric metric) {return sums[metric];}
bool health_service_events_subscribe(void (*handler)(HealthEventType,void *),void *context) {(void)handler;(void)context;return available;}
int main(void) {
 health_set_update_handler(updated);health_init();assert(health_is_health_available());
 assert(health_get_distance_tenths()==105 && health_get_active_calories()==1234 && health_get_step_count()==3750);
 assert(health_get_step_goal()==7500);goal=10000;health_handler(HealthEventMovementUpdate,NULL);assert(health_get_step_goal()==10000 && updates==1);
 units=MeasurementSystemImperial;sums[1]=1609;health_handler(HealthEventMovementUpdate,NULL);assert(health_get_distance_tenths()==10);
 goal=0;health_handler(HealthEventMovementUpdate,NULL);assert(health_get_step_goal()==7500);
 averaged=false;goal=12345;health_handler(HealthEventMovementUpdate,NULL);assert(health_get_step_goal()==7500);
 mode=StepGoalCustom;assert(health_get_step_goal()==10000);
 mode=StepGoalAutomatic;assert(health_get_step_goal()==7500);
 mode=StepGoalCustom;assert(health_get_step_goal()==10000);
 averaged=true;goal=20000;health_handler(HealthEventMovementUpdate,NULL);assert(health_get_step_goal()==10000);
 mode=StepGoalAutomatic;assert(health_get_step_goal()==20000);
 day+=86400;sums[0]=0;sums[1]=0;sums[2]=0;assert(health_get_step_count()==0 && health_get_distance_tenths()==0 && health_get_active_calories()==0);
 puts("PASS: activity metrics, km/mi rounding, averaged goal and 7500 fallback, event redraw callback, midnight reset.");
}
'''
run_harness(TEST,HEADER)
