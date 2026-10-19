#!/usr/bin/env python3
"""Exercise production AppMessage handling: omitted keys must not reset settings."""
from test_low_battery import HARNESS, run_harness

HEADER = r'''
#include <stdlib.h>
#define ARRAY_LENGTH(a) (sizeof(a) / sizeof((a)[0]))
#define GColorFromHEX(x) ((GColor)(x))
#define TUPLE_CSTRING 1
#define TUPLE_INT 0
#define TUPLE_UINT 2
typedef union { char *cstring; int32_t int32; uint32_t uint32; } TupleValue;
typedef struct { int type; uint16_t length; TupleValue *value; } Tuple;
typedef struct { uint32_t key; Tuple tuple; bool empty; uint32_t second_key; Tuple second_tuple; } DictionaryIterator;
Tuple *dict_find(DictionaryIterator *iter, uint32_t key);
void app_message_register_inbox_received(void (*handler)(DictionaryIterator *, void *));
void app_message_open(int inbox, int outbox);
'''
PACKET = '''#pragma once
void packet_init(void);
bool packet_get_boolean(DictionaryIterator *iter, uint32_t key);
int packet_get_integer(DictionaryIterator *iter, uint32_t key);
'''
TEST = HARNESS[:HARNESS.index('int main(void)')] + r'''
#include "src/c/modules/comm.c"
Tuple *dict_find(DictionaryIterator *iter, uint32_t key) {
 return !iter->empty && iter->key == key ? &iter->tuple :
   (!iter->empty && iter->second_key == key ? &iter->second_tuple : NULL);
}
int packet_get_integer(DictionaryIterator *iter, uint32_t key) {
 Tuple *t=dict_find(iter,key); assert(t); return t->value->int32;
}
bool packet_get_boolean(DictionaryIterator *iter, uint32_t key) {
 return packet_get_integer(iter,key)!=0;
}
void packet_init(void) {}
void app_message_register_inbox_received(void (*handler)(DictionaryIterator *, void *)) {(void)handler;}
void app_message_open(int inbox,int outbox) {assert(inbox>=480);assert(outbox>=64);}
void main_window_reload_config(void) {render();}
void main_window_refresh_data(void) {}
void refresh_phone_ready(void) {}
void weather_store(int t,int c,int u) {(void)t;(void)c;(void)u;}
int main(void) {
 data_init();
 // Seed every byte, then compare the whole config after empty/partial messages.
 data_set_enable(MESSAGE_KEY_EnableThickHands,true);
 data_set_enable(MESSAGE_KEY_BatteryOnlyWhenLow,true);
 data_set_slot(MESSAGE_KEY_SlotTop,SlotTypeTime);
 data_set_color(MESSAGE_KEY_ColorCenterDot,42);
 data_set_date_style(DateStyleDayOnly);
 AppConfig before=s_app_config;
 DictionaryIterator empty={.empty=true};
 in_recv_handler(&empty,NULL);
 assert(!memcmp(&before,&s_app_config,sizeof(before)));
 TupleValue value={.int32=0};
 DictionaryIterator message={.key=MESSAGE_KEY_EnableDate,.tuple={.value=&value}};
 in_recv_handler(&message,NULL);
 before.enable_date=false;
 assert(!memcmp(&before,&s_app_config,sizeof(before)));
 message.key=MESSAGE_KEY_ColorBackground;
 in_recv_handler(&message,NULL);
 before.color_background=0;
 assert(!memcmp(&before,&s_app_config,sizeof(before)));
 value.cstring="3"; message.key=MESSAGE_KEY_SlotLeft;message.tuple.type=TUPLE_CSTRING;
 in_recv_handler(&message,NULL);
 before.slot_left=SlotTypeBattery;
 assert(!memcmp(&before,&s_app_config,sizeof(before)));
 message.key=MESSAGE_KEY_Theme;
 in_recv_handler(&message,NULL);
 assert(!memcmp(&before,&s_app_config,sizeof(before)));
 message.key=MESSAGE_KEY_DateStyle;value.cstring="2";
 in_recv_handler(&message,NULL);before.date_style=DateStyleWeekdayDay;
 assert(!memcmp(&before,&s_app_config,sizeof(before)));
 message.tuple.type=0;value.int32=0;
 in_recv_handler(&message,NULL);before.date_style=DateStyleFull;
 assert(!memcmp(&before,&s_app_config,sizeof(before)));
 value.int32=99;in_recv_handler(&message,NULL);
 assert(!memcmp(&before,&s_app_config,sizeof(before)));
 message.key=MESSAGE_KEY_CustomStepGoal;message.tuple.type=TUPLE_INT;message.tuple.length=4;
 value.int32=10000;in_recv_handler(&message,NULL);assert(data_get_custom_step_goal()==10000);
 message.key=MESSAGE_KEY_StepGoalMode;value.int32=1;in_recv_handler(&message,NULL);
 assert(data_get_step_goal_mode()==StepGoalCustom);
 value.int32=0;in_recv_handler(&message,NULL);assert(data_get_custom_step_goal()==10000);
 value.int32=1;in_recv_handler(&message,NULL);
 before=s_app_config;
 message.key=MESSAGE_KEY_CustomStepGoal;
 const int bad[]={0,-1,999,100001,2147483647};
 for(size_t i=0;i<sizeof(bad)/sizeof(bad[0]);i++) {
   value.int32=bad[i];in_recv_handler(&message,NULL);assert(!memcmp(&before,&s_app_config,sizeof(before)));
 }
 message.tuple.type=TUPLE_CSTRING;
 const char *bad_text[]={"","999","100001","1000.5","1e4"," 1000","+1000","-1000","1000junk","999999999999999999999999"};
 TupleValue mode={.int32=0};message.second_key=MESSAGE_KEY_StepGoalMode;
 message.second_tuple=(Tuple){.type=TUPLE_INT,.length=4,.value=&mode};
 for(size_t i=0;i<sizeof(bad_text)/sizeof(bad_text[0]);i++) {
   value.cstring=(char *)bad_text[i];message.tuple.length=strlen(value.cstring)+1;
   in_recv_handler(&message,NULL);assert(!memcmp(&before,&s_app_config,sizeof(before)));
 }
 message.second_key=0;
 value.cstring="100000";message.tuple.length=7;in_recv_handler(&message,NULL);assert(data_get_custom_step_goal()==100000);
 value.cstring="1000";message.tuple.length=5;in_recv_handler(&message,NULL);assert(data_get_custom_step_goal()==1000);
 message.key=MESSAGE_KEY_StepGoalMode;value.cstring="1junk";message.tuple.length=6;
 before=s_app_config;in_recv_handler(&message,NULL);assert(!memcmp(&before,&s_app_config,sizeof(before)));
 message.key=MESSAGE_KEY_CustomStepGoal;message.tuple.type=TUPLE_UINT;message.tuple.length=4;
 value.uint32=UINT32_MAX;in_recv_handler(&message,NULL);assert(!memcmp(&before,&s_app_config,sizeof(before)));
 data_deinit();memset(&s_app_config,0,sizeof(s_app_config));data_init();assert(!memcmp(&before,&s_app_config,sizeof(before)));
 puts("PASS: goal validation, mode switching, invalid pair atomic rejection, persistence; empty, partial, zero/false, string slot and unknown/watch-ignored keys preserve all omitted settings.");
}
'''
run_harness(TEST, HEADER, PACKET)
