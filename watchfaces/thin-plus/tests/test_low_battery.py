#!/usr/bin/env python3
"""Exercise production persistence and slot rendering with a small host SDK stub."""
from pathlib import Path
import json, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[1]
KEYS = json.loads((ROOT/'package.json').read_text())['pebble']['messageKeys']
HEADER = r'''
#pragma once
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
typedef uint8_t GColor;
typedef int status_t;
typedef struct { int unused; } GContext;
typedef struct { int x,y,w,h; } GRect;
#define GRect(x,y,w,h) ((GRect){x,y,w,h})
typedef struct { uint8_t charge_percent; bool is_charging, is_plugged; } BatteryChargeState;
#define GColorClear 0
#define GColorBlack 1
#define GColorWhite 2
#define GColorLightGray 3
#define GColorDarkCandyAppleRed 4
#define GColorChromeYellow 5
#define GColorDarkGray 6
#define PBL_IF_COLOR_ELSE(a,b) (a)
#define gcolor_equal(a,b) ((a)==(b))
#define APP_LOG(...) ((void)0)
#define APP_LOG_LEVEL_ERROR 1
#define APP_LOG_LEVEL_INFO 2
#define GTextOverflowModeFill 0
#define GTextAlignmentCenter 0
bool persist_exists(int key);
int persist_delete(int key);
int persist_write_int(int key, int value);
int persist_write_data(int key, const void *data, size_t size);
int persist_read_data(int key, void *data, size_t size);
BatteryChargeState battery_state_service_peek(void);
bool clock_is_24h_style(void);
void graphics_context_set_text_color(GContext *ctx, GColor color);
void graphics_draw_text(GContext *ctx, const char *text, void *font, GRect rect, int overflow, int align, void *attributes);
'''
HARNESS = r'''
#include <assert.h>
#include "src/c/modules/data.c"
#include "src/c/modules/slots.c"
static uint8_t stored[256];
static size_t stored_size;
static bool migration;
static uint8_t battery;
static int draws;
static char drawn[3][16];
bool persist_exists(int key) { return key==50 ? migration : stored_size>0; }
int persist_delete(int key) { (void)key; stored_size=0; return 0; }
int persist_write_int(int key,int value) { (void)key; migration=value; return 0; }
int persist_write_data(int key,const void *p,size_t n) { (void)key; memcpy(stored,p,n);stored_size=n;return n; }
int persist_read_data(int key,void *p,size_t n) { (void)key; if(n>stored_size)n=stored_size;memcpy(p,stored,n);return n; }
BatteryChargeState battery_state_service_peek(void) { return (BatteryChargeState){.charge_percent=battery}; }
bool clock_is_24h_style(void) { return true; }
bool health_is_health_available(void) { return true; }
int health_get_step_count(void) { return 6432; }
int health_get_heart_rate(void) { return 72; }
void graphics_context_set_text_color(GContext *ctx,GColor color) { (void)ctx;(void)color; }
void graphics_draw_text(GContext *ctx,const char *text,void *font,GRect rect,int overflow,int align,void *attributes) {
 (void)ctx;(void)font;(void)rect;(void)overflow;(void)align;(void)attributes;
 assert(draws<3);snprintf(drawn[draws++],16,"%s",text);
}
static void render(void) { draws=0;slots_draw(NULL); }
int main(void) {
 data_init();
 assert(!data_get_enable(MESSAGE_KEY_BatteryOnlyWhenLow));
 // A pre-option persisted record must retain its settings and default the new flag off.
 data_set_slot(MESSAGE_KEY_SlotTop,SlotTypeBattery);
 data_set_enable(MESSAGE_KEY_EnableBattery,false);
 data_set_color(MESSAGE_KEY_ColorBatteryEmpty,9);
 data_deinit();
 stored_size=offsetof(AppConfig,battery_only_when_low);
 data_set_enable(MESSAGE_KEY_BatteryOnlyWhenLow,true);
 data_init();
 assert(!data_get_enable(MESSAGE_KEY_BatteryOnlyWhenLow));
 assert(data_get_slot(MESSAGE_KEY_SlotTop)==SlotTypeBattery);
 assert(!data_get_enable(MESSAGE_KEY_EnableBattery));
 assert(data_get_color(MESSAGE_KEY_ColorBatteryEmpty)==9);
 // New saved values round-trip without affecting the independent marker switch.
 data_set_enable(MESSAGE_KEY_BatteryOnlyWhenLow,true);data_deinit();
 data_set_enable(MESSAGE_KEY_BatteryOnlyWhenLow,false);data_init();
 assert(data_get_enable(MESSAGE_KEY_BatteryOnlyWhenLow));
 assert(!data_get_enable(MESSAGE_KEY_EnableBattery));
 const uint32_t keys[]={MESSAGE_KEY_SlotTop,MESSAGE_KEY_SlotLeft,MESSAGE_KEY_SlotBottom};
 const int percentages[]={0,1,19,20,21,100};
 for(int position=0;position<3;position++) {
  for(int k=0;k<3;k++)data_set_slot(keys[k],SlotTypeNone);
  data_set_slot(keys[position],SlotTypeBattery);
  for(int enabled=0;enabled<2;enabled++) {
   data_set_enable(MESSAGE_KEY_BatteryOnlyWhenLow,enabled);
   for(int p=0;p<6;p++) {
    battery=percentages[p];render();
    bool shown=!enabled || battery<20;
    assert(draws==(shown?1:0));
    if(shown){char expected[16];snprintf(expected,16,"%d%%",battery);assert(!strcmp(drawn[0],expected));}
   }
  }
 }
 // All selected battery slots follow the same threshold, in both directions.
 for(int k=0;k<3;k++)data_set_slot(keys[k],SlotTypeBattery);
 data_set_enable(MESSAGE_KEY_BatteryOnlyWhenLow,true);
 battery=20;render();assert(draws==0);
 battery=19;render();assert(draws==3);
 battery=20;render();assert(draws==0);
 // Other complications still render above the threshold; no Battery selection means no warning.
 data_set_slot(keys[0],SlotTypeSteps);data_set_slot(keys[1],SlotTypeHeartRate);data_set_slot(keys[2],SlotTypeTime);
 battery=100;render();assert(draws==3);assert(!strcmp(drawn[0],"6432"));assert(!strcmp(drawn[1],"72"));
 battery=1;render();assert(draws==3);assert(!strcmp(drawn[0],"6432"));
 assert(!slots_uses(SlotTypeBattery));
 puts("PASS: legacy settings migration, persistence, all three slots, 0/1/19/20/21/100%, on/off, other complications, marker independence.");
}
'''
with tempfile.TemporaryDirectory(prefix='thin-low-battery-test-') as tmp:
    temp=Path(tmp)
    (temp/'pebble.h').write_text(HEADER+'\n'+ '\n'.join(f'#define MESSAGE_KEY_{key} {i+10000}' for i,key in enumerate(KEYS))+'\n')
    (temp/'pebble-scalable').mkdir()
    (temp/'pebble-scalable/pebble-scalable.h').write_text('#pragma once\n#define scl_y_pp(...) 25\n#define scl_x(x) (x)\n#define scl_y(y) (y)\n#define scl_get_font(x) NULL\n#define PS_DISP_W 200\n')
    (temp/'test.c').write_text(HARNESS)
    subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I',str(temp),'-I',str(ROOT),str(temp/'test.c'),'-o',str(temp/'test')],check=True)
    subprocess.run([str(temp/'test')],check=True)
