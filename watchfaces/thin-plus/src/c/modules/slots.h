#pragma once

#include <pebble.h>

#include "data.h"
#include "health.h"
#include "scalable.h"

bool slots_uses(SlotType type);

void slots_draw(GContext *ctx);
