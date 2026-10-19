#!/usr/bin/env python3
"""Compile the production event functions with observable host service stubs."""
from pathlib import Path
import json, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT/'src/c/windows/main_window.c').read_text()

def function(name):
    # Extract a complete C function, without rewriting its implementation.
    import re
    match = re.search(r'^(?:static )?void '+name+r'\([^\n]*\) \{', source, re.M)
    assert match, name
    depth = 1
    end = source.index('{', match.start()) + 1
    while depth:
        if source[end] == '{': depth += 1
        if source[end] == '}': depth -= 1
        end += 1
    return source[match.start():end]

keys = json.loads((ROOT/'package.json').read_text())['pebble']['messageKeys']
prefix = r'''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stddef.h>
#define APP_LOG(...) ((void)0)
#define PBL_TOUCH 1
#define SECONDS_DURATION 15000
#define ANIMATION_DURATION 1000
#define ANIMATION_DELAY 300
typedef int Window;
typedef int Layer;
typedef int GColor;
typedef int Animation;
typedef int AppTimer;
typedef int AnimationProgress;
typedef struct { void (*load)(Window *); void (*unload)(Window *); } WindowHandlers;
typedef struct { void (*update)(Animation *, AnimationProgress); } AnimationImplementation;
typedef enum {TouchEvent_Touchdown, TouchEvent_Liftoff, TouchEvent_PositionUpdate} TouchEventType;
typedef struct {TouchEventType type;} TouchEvent;
static Window window;
static Window *s_main_window;
static Layer *s_canvas_layer;
static bool flags[128], s_animating, s_is_connected, s_show_seconds;
static AppTimer timer, *s_seconds_timer;
static int buzzes, touches, unsubscribes, registers, reschedules, reloads, animations, tick_changes;
static bool data_get_enable(uint32_t key) {return flags[key];}
static GColor data_get_color(uint32_t key) {(void)key;return 0;}
static void vibes_long_pulse(void) {buzzes++;}
static void layer_mark_dirty(Layer *layer) {(void)layer;}
static void subscribe_tick(void) {tick_changes++;}
static void update_time(void) {}
static void seconds_timer_handler(void *context);
static AppTimer *app_timer_register(int ms, void (*cb)(void *), void *context) {
 assert(ms==15000 && cb==seconds_timer_handler && context==NULL);registers++;return &timer;
}
static void app_timer_reschedule(AppTimer *t, int ms) {assert(t==&timer && ms==15000);reschedules++;}
static void touch_handler(const TouchEvent *event, void *context);
static void touch_service_subscribe(void (*cb)(const TouchEvent *,void *), void *ctx) {
 assert(cb==touch_handler && ctx==NULL);touches++;
}
static void touch_service_unsubscribe(void) {unsubscribes++;}
static Window *window_create(void) {return &window;}
static void window_set_background_color(Window *w,GColor c) {(void)w;(void)c;}
static void window_set_window_handlers(Window *w,WindowHandlers handlers) {(void)w;(void)handlers;}
static void window_stack_push(Window *w,bool animated) {(void)w;(void)animated;}
static void window_load(Window *w) {(void)w;}
static void window_unload(Window *w) {(void)w;}
static void hands_update(Animation *a,AnimationProgress p) {(void)a;(void)p;}
static void animate(int duration,int delay,AnimationImplementation *impl,bool handlers) {
 assert(duration==1000 && delay==300 && impl->update==hands_update && handlers);animations++;
}
void main_window_reload_config(void) {reloads++;}
'''
main = r'''
int main(void) {
 // Buzz only on a connected->disconnected edge when enabled.
 flags[MESSAGE_KEY_VibrateOnDisconnect]=false;
 bt_handler(true);bt_handler(false);assert(buzzes==0);
 flags[MESSAGE_KEY_VibrateOnDisconnect]=true;
 bt_handler(true);bt_handler(false);bt_handler(false);assert(buzzes==1);
 bt_handler(true);assert(buzzes==1);
 // Touch sensor subscribed only when both settings are enabled.
 for(int tap=0;tap<2;tap++)for(int seconds=0;seconds<2;seconds++) {
  flags[MESSAGE_KEY_TapForSeconds]=tap;flags[MESSAGE_KEY_EnableSecondHand]=seconds;
  touches=unsubscribes=0;update_touch_subscription();
  assert(unsubscribes==1 && touches==(tap && seconds));
 }
 TouchEvent event={TouchEvent_Touchdown};touch_handler(&event,NULL);assert(registers==0);
 event.type=TouchEvent_PositionUpdate;touch_handler(&event,NULL);assert(registers==0);
 event.type=TouchEvent_Liftoff;touch_handler(&event,NULL);assert(registers==1 && s_show_seconds);
 touch_handler(&event,NULL);assert(registers==1 && reschedules==1);
 seconds_timer_handler(NULL);assert(!s_show_seconds && s_seconds_timer==NULL);
 flags[MESSAGE_KEY_EnableSecondHand]=false;
 touch_handler(&event,NULL);assert(registers==1 && !s_show_seconds);
 // Animation-off initializes immediately and reloads config exactly once.
 flags[MESSAGE_KEY_EnableStartupAnim]=false;s_animating=true;
 main_window_push();assert(!s_animating && animations==0 && reloads==1);
 reloads=0;flags[MESSAGE_KEY_EnableStartupAnim]=true;
 main_window_push();assert(animations==1 && reloads==1);
 puts("PASS: disconnect vibration edges/toggle, touch subscription and liftoff, 15s timer/reschedule, immediate startup without animation.");
}
'''
with tempfile.TemporaryDirectory(prefix='thin-interactions-') as directory:
    tmp = Path(directory)
    definitions = '\n'.join('#define MESSAGE_KEY_'+key+' '+str(i) for i,key in enumerate(keys))
    body = '\n'.join(function(n) for n in ['seconds_timer_handler','show_seconds','touch_handler',
                                          'update_touch_subscription','bt_handler','main_window_push'])
    (tmp/'test.c').write_text(prefix+'\n'+definitions+'\n'+body+'\n'+main)
    subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-Wno-unused-parameter',
                    '-fsanitize=address,undefined',str(tmp/'test.c'),'-o',str(tmp/'test')],check=True)
    subprocess.run([str(tmp/'test')],check=True)
