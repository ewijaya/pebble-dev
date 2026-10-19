#!/usr/bin/env python3
"""Production formatting, weather persistence/expiry and request scheduling."""
from test_low_battery import run_harness
HEADER = r'''
#define APP_MSG_OK 0
typedef struct {int unused;} DictionaryIterator;
int persist_get_size(int key);
int app_message_outbox_begin(DictionaryIterator **iter);
int app_message_outbox_send(void);
int dict_write_int32(DictionaryIterator *iter, uint32_t key, int32_t value);
'''
TEST = r'''
#include <assert.h>
#include <pebble.h>
static time_t now=1800000000;
static time_t fake_time(time_t *out) {if(out)*out=now;return now;}
#define time fake_time
#include "src/c/modules/data.c"
#include "src/c/modules/weather.c"
#include "src/c/modules/format.c"
#include "src/c/modules/refresh.c"
static uint8_t saved[256];static size_t size;
static DictionaryIterator dictionary;
static int sends,writes;static bool busy;
bool persist_exists(int key) {(void)key;return false;}
int persist_delete(int key) {(void)key;return 0;}
int persist_write_int(int key,int value) {(void)key;(void)value;return 0;}
int persist_write_data(int key,const void *data,size_t n) {if(key==51){memcpy(saved,data,n);size=n;}return (int)n;}
int persist_read_data(int key,void *data,size_t n) {(void)key;if(n>size)n=size;memcpy(data,saved,n);return (int)n;}
int persist_get_size(int key) {(void)key;return (int)size;}
bool slots_uses(SlotType type) {return data_get_slot(MESSAGE_KEY_SlotTop)==type || data_get_slot(MESSAGE_KEY_SlotLeft)==type;}
int app_message_outbox_begin(DictionaryIterator **iter) {*iter=&dictionary;writes=0;return busy?1:APP_MSG_OK;}
int app_message_outbox_send(void) {sends++;return APP_MSG_OK;}
int dict_write_int32(DictionaryIterator *iter,uint32_t key,int32_t value) {
 (void)iter;(void)value;assert(key==MESSAGE_KEY_WeatherRequest || key==MESSAGE_KEY_WeatherUnits || key==MESSAGE_KEY_TimezoneRequest);writes++;return 0;
}
int main(void) {
 data_init();weather_init();int temperature=0;
 assert(!weather_get_temperature(&temperature));
 weather_store(18,3,0);assert(weather_get_temperature(&temperature) && temperature==18);
 now+=1799;assert(!weather_needs_update(now));now++;assert(weather_needs_update(now));
 memset(&s_weather,0,sizeof(s_weather));weather_init();assert(weather_get_temperature(&temperature) && temperature==18);
 now+=9000;assert(weather_get_temperature(&temperature));now++;assert(!weather_get_temperature(&temperature));
 now=1800000000;weather_store(-12,71,0);assert(weather_get_temperature(&temperature) && temperature==-12);
 weather_store(999,3,0);assert(weather_get_temperature(&temperature) && temperature==-12);
 data_set_weather_units(1);assert(!weather_get_temperature(&temperature));weather_store(22,3,0);assert(!weather_get_temperature(&temperature));
 weather_store(72,0,1);assert(weather_get_temperature(&temperature) && temperature==72);
 now--;assert(!weather_get_temperature(&temperature));now++;
 refresh_poll();assert(sends==0); // No selected weather/timezone, no phone traffic.
 data_set_slot(MESSAGE_KEY_SlotTop,SlotTypeWeather);refresh_poll();assert(sends==0); // Fresh cache.
 now+=1800;refresh_poll();assert(sends==1 && writes==2);
 now+=60;refresh_poll();assert(sends==1);now+=1740;refresh_poll();assert(sends==2);
 data_set_slot(MESSAGE_KEY_SlotLeft,SlotTypeSecondTime);refresh_phone_ready();assert(sends==3 && writes==3);
 data_set_slot(MESSAGE_KEY_SlotTop,SlotTypeNone);now+=1800;refresh_poll();assert(sends==4 && writes==1);
 busy=true;now+=1800;refresh_poll();assert(sends==4);busy=false;refresh_poll();assert(sends==5);
 data_set_slot(MESSAGE_KEY_SlotLeft,SlotTypeNone);now+=1800;refresh_poll();assert(sends==5);
 int offset;data_set_timezone(0);assert(data_get_timezone(&offset)&&offset==0);
 data_set_timezone(-720);assert(data_get_timezone(&offset)&&offset==-720);
 data_set_timezone(840);assert(data_get_timezone(&offset)&&offset==840);
 data_set_timezone(10000);assert(!data_get_timezone(&offset));
 struct tm date={.tm_year=121,.tm_mon=0,.tm_mday=1,.tm_yday=0,.tm_wday=5};assert(format_iso_week(&date)==53);
 date.tm_mday=4;date.tm_yday=3;date.tm_wday=1;assert(format_iso_week(&date)==1);
 date=(struct tm){.tm_year=118,.tm_mon=11,.tm_mday=31,.tm_yday=364,.tm_wday=1};assert(format_iso_week(&date)==1);
 date=(struct tm){.tm_year=120,.tm_mon=11,.tm_mday=31,.tm_yday=365,.tm_wday=4};assert(format_iso_week(&date)==53);
 char text[16];date.tm_hour=0;date.tm_min=5;format_clock(text,sizeof(text),&date,true);assert(!strcmp(text,"00:05"));
 format_clock(text,sizeof(text),&date,false);assert(!strcmp(text,"12:05"));date.tm_hour=23;format_clock(text,sizeof(text),&date,false);assert(!strcmp(text,"11:05"));
 puts("PASS: ISO year boundaries, 12/24h time, timezone bounds, cache persistence/units/expiry, 30-minute requests, no traffic with unused slots, outbox busy recovery.");
}
'''
run_harness(TEST, HEADER)
