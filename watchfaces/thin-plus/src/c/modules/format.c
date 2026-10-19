#include "format.h"

static bool leap(int year) {
  return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
}

int format_iso_week(const struct tm *date) {
  // Find the Thursday in this ISO week, including the adjacent-year boundaries.
  const int weekday = date->tm_wday == 0 ? 7 : date->tm_wday;
  int thursday = date->tm_yday + 4 - weekday;
  const int year = date->tm_year + 1900;
  if (thursday < 0) thursday += leap(year - 1) ? 366 : 365;
  else if (thursday >= (leap(year) ? 366 : 365)) return 1;
  return thursday / 7 + 1;
}

void format_clock(char *text, size_t size, const struct tm *date, bool twenty_four_hour) {
  int hour = date->tm_hour;
  if (!twenty_four_hour) { hour %= 12; if (!hour) hour = 12; }
  snprintf(text, size, twenty_four_hour ? "%02d:%02d" : "%d:%02d", hour, date->tm_min);
}
