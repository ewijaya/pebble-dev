#pragma once
#include <pebble.h>

int format_iso_week(const struct tm *date);
void format_clock(char *text, size_t size, const struct tm *date, bool twenty_four_hour);
