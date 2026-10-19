// TEMP_TEST: design-gate alternative, applied in a scratch build only.
const int x = center.x;
const int y = scl_y(90);
graphics_context_set_stroke_color(ctx, data_get_color(MESSAGE_KEY_ColorDisconnected));
graphics_context_set_stroke_width(ctx, 2);
graphics_draw_line(ctx, GPoint(x, y - 6), GPoint(x, y + 6));
graphics_draw_line(ctx, GPoint(x, y - 6), GPoint(x + 4, y - 3));
graphics_draw_line(ctx, GPoint(x + 4, y - 3), GPoint(x - 4, y + 3));
graphics_draw_line(ctx, GPoint(x - 4, y - 3), GPoint(x + 4, y + 3));
graphics_draw_line(ctx, GPoint(x + 4, y + 3), GPoint(x, y + 6));
graphics_context_set_stroke_width(ctx, 1);
graphics_draw_line(ctx, GPoint(x - 7, y + 7), GPoint(x + 7, y - 7));
