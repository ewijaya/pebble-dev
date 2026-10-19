#!/usr/bin/env python3
"""Check the production progress geometry and hidden/empty/full boundaries."""
from test_low_battery import run_harness
HEADER=r'''
#include <stdlib.h>
typedef struct {int16_t x,y;} GPoint;
typedef struct {GPoint origin;struct {int16_t w,h;} size;} RingRect;
#undef GRect
#define GRect RingRect
#define RingRect(a,b,c,d) ((RingRect){.origin={a,b},.size={c,d}})
#define TRIG_MAX_ANGLE 65536
#define GOvalScaleModeFitCircle 0
void graphics_context_set_stroke_color(GContext *ctx,GColor color);
void graphics_context_set_stroke_width(GContext *ctx,int width);
void graphics_draw_line(GContext *ctx,GPoint a,GPoint b);
void graphics_draw_arc(GContext *ctx,GRect bounds,int mode,int start,int end);
'''
TEST=r'''
#include <assert.h>
#include "src/c/modules/step_ring.c"
static bool enabled=true,available=true;
static int steps=0,goal=7500,length,angle;
bool data_get_enable(uint32_t key) {assert(key==MESSAGE_KEY_EnableStepRing);return enabled;}
GColor data_get_color(uint32_t key) {assert(key==MESSAGE_KEY_ColorStepRing);return 2;}
bool health_is_health_available(void) {return available;}
int health_get_step_count(void) {return steps;}
int health_get_step_goal(void) {return goal;}
void graphics_context_set_stroke_color(GContext *ctx,GColor color) {(void)ctx;(void)color;}
void graphics_context_set_stroke_width(GContext *ctx,int width) {(void)ctx;assert(width==2);}
void graphics_draw_line(GContext *ctx,GPoint a,GPoint b) {(void)ctx;assert(a.x>=11&&a.x<=188&&b.x>=11&&b.x<=188);assert(a.y>=11&&a.y<=216&&b.y>=11&&b.y<=216);length+=abs(b.x-a.x)+abs(b.y-a.y);}
void graphics_draw_arc(GContext *ctx,GRect bounds,int mode,int start,int end) {(void)ctx;(void)bounds;(void)mode;assert(start==0);angle=end;}
int main(void) {
 GRect bounds=GRect(0,0,200,228);
 step_ring_draw(NULL,bounds,7);assert(length==0&&angle==0);
 goal=10000;steps=5000;step_ring_draw(NULL,bounds,7);
#ifdef PBL_ROUND
 assert(angle==32768);
#else
 assert(length==382);
#endif
 length=angle=0;steps=10000;step_ring_draw(NULL,bounds,7);
#ifdef PBL_ROUND
 assert(angle==65536);
#else
 assert(length==764);
#endif
 int full_length=length,full_angle=angle;
 length=angle=0;steps=15000;step_ring_draw(NULL,bounds,7);
 assert(length==full_length && angle==full_angle);
 length=angle=0;enabled=false;step_ring_draw(NULL,bounds,7);assert(!length&&!angle);
 enabled=true;available=false;step_ring_draw(NULL,bounds,7);assert(!length&&!angle);
 available=true;goal=0;step_ring_draw(NULL,bounds,7);assert(!length&&!angle);
 puts("PASS: ring off/no health/zero goal/zero steps, half progress, capped full progress and inset geometry.");
}
'''
run_harness(TEST,HEADER)
run_harness(TEST,HEADER+'\n#define PBL_ROUND 1\n')
