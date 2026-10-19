#include "step_ring.h"
#include "data.h"
#include "health.h"

void step_ring_draw(GContext *ctx, GRect bounds, int margin) {
  if (!data_get_enable(MESSAGE_KEY_EnableStepRing) || !health_is_health_available()) return;
  int steps = health_get_step_count(), goal = health_get_step_goal();
  if (steps <= 0 || goal <= 0) return;
  if (steps > goal) steps = goal;
  graphics_context_set_stroke_color(ctx, data_get_color(MESSAGE_KEY_ColorStepRing));
  graphics_context_set_stroke_width(ctx, 2);
#if defined(PBL_ROUND)
  const int inset = 2 * margin + 4;
  graphics_draw_arc(ctx, GRect(inset, inset, bounds.size.w - 2 * inset, bounds.size.h - 2 * inset),
    GOvalScaleModeFitCircle, 0, (int32_t)((int64_t)TRIG_MAX_ANGLE * steps / goal));
#else
  const int inset = margin + 4;
  const int x0 = inset, y0 = inset, x1 = bounds.size.w - inset - 1, y1 = bounds.size.h - inset - 1;
  const int middle = bounds.size.w / 2;
  const GPoint vertices[] = {{middle,y0},{x1,y0},{x1,y1},{x0,y1},{x0,y0},{middle,y0}};
  int remaining = (int)((int64_t)(2 * (x1 - x0 + y1 - y0)) * steps / goal);
  for (int i = 0; i < 5 && remaining > 0; i++) {
    GPoint a = vertices[i], b = vertices[i + 1];
    const int dx = b.x - a.x, dy = b.y - a.y;
    const int length = abs(dx) + abs(dy);
    const int draw = remaining < length ? remaining : length;
    b.x = a.x + dx * draw / length;
    b.y = a.y + dy * draw / length;
    graphics_draw_line(ctx, a, b);
    remaining -= draw;
  }
#endif
}
