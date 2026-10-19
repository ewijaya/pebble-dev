# PRD: Thin+ improvements for 1.2.0 and 1.3.0

Status: approved to start (2026-10-19). Owner: Edward Wijaya.
Current live version: **1.1.0** (store app `b0a4b28dbe9440c3b19f68e3`,
https://apps.repebble.com/b0a4b28dbe9440c3b19f68e3), tags `thin-plus-v1.0.0`,
`thin-plus-v1.1.0` on `origin` (github.com/ewijaya/pebble-dev).

## 1. Goal and phasing

Ship eleven improvements in two store releases (including the owner-added R11).
Each release is developed,
verified in the emulator, sideloaded to the owner's **Pebble Time 2 (emery)**,
approved by the owner, then published with the existing release workflow.

| Release | Items | Theme |
| --- | --- | --- |
| **1.2.0** | R1 Quick View, R2 platform-aware settings, R3 disconnect alert, R4 README + CI, R5 tap for seconds, R9 charging indicator, R10 startup animation toggle | Correctness and polish, no network |
| **1.3.0** | R6 more complications, R7 weather, R8 step-goal arc, R11 date styles | New information, phone-side JS, date choices |

Do 1.2.0 completely (including publishing) before starting 1.3.0, unless the
owner says otherwise.

Out of scope: changing the UUID, upstream (`C-D-Lewis/pebble-dev`), the
original `watchfaces/thin`, store visibility of anything other than Thin+.

## 2. Ground rules (read first)

### 2.1 Environment

- Project: `~/projects/pebble-dev/watchfaces/thin-plus`, branch
  `watchface/thin-plus`, push to `origin` only. Shell is **zsh**: put loops in
  `bash` scripts (zsh does not word-split `$var`).
- Pebble Tool 5.0.40, SDK 4.33.1, headless Ubuntu. One emulator at a time
  (`pebble kill` between platforms). Screenshots:
  `pebble screenshot --emulator <p> --no-open file.png`. If SDL errors, prefix
  `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy SDL_RENDER_DRIVER=software`.
- Emulator controls available (use them for evidence): `emu-battery --percent N
  [--charging]`, `emu-bt-connection --connected no|yes`,
  `emu-set-timeline-quick-view on|off`, `emu-heart-rate`, `emu-steps`,
  `emu-distance`, `emu-calories`, `emu-set-time`, `emu-time-format`, `emu-tap`.
  Check each command's `--help` before use.
- The Clay settings page cannot run headless. To capture a specific state,
  temporarily hard-code return values at the top of the `data_get_*` getters
  in `src/c/modules/data.c`, marked `// TEMP_TEST`, ideally in a scratch copy
  (`rsync -a --exclude build`). Before any commit, `grep -rc TEMP_TEST src`
  must report 0.
- After changing `messageKeys` in `package.json`, run `pebble clean` before
  building, or `MESSAGE_KEY_*` values are stale.
- Physical install to the PT2: `pebble install --cloudpebble build/thin-plus.pbw`
  (check `pebble login --status`). If it hangs, ask the owner to reopen the
  Pebble app on his phone.
- Host tests: `python3 tests/test_low_battery.py` compiles production C with
  SDK stubs and sanitizers. Extend this pattern for new pure logic.
- Release/store work: use the existing `thin-plus-release` skill
  (`~/.codex/skills/thin-plus-release`) and its references. The store listing
  already exists; never create a second one. Never use `pebble publish`.

### 2.2 Compatibility rules (non-negotiable)

1. **Persisted config is append-only.** `AppConfig` in `src/c/modules/data.c`
   is written with `persist_write_data`; older saves are a prefix. Add new
   fields only at the end. Set every new field's default **before**
   `persist_read_data` (see existing slot/thick-hands defaults).
2. **New colors use the `GColorClear` sentinel** and fall back after reading
   (see `color_hand_tips`, `color_second_tip`, `color_battery_empty`).
3. **Message keys are appended** to the end of `pebble.messageKeys`.
4. **`SlotType` values are persisted and sent by `config.js`**: only append new
   types before `SlotTypeCount`, never renumber. Keep `slotOptions` in
   `config.js` in sync.
5. **Defaults preserve current behavior.** An existing user who updates must
   see an unchanged face until they change a setting. Exception: R1 (Quick
   View) is a fix and is always on.
6. **Settings message size.** Inbox is 512 bytes (`comm.c`). After adding keys,
   compute the worst-case Clay dictionary (7-byte tuple header + 4 bytes per
   int/bool + string length incl. NUL) and keep it under 480 bytes, or raise
   the inbox with a recorded reason.
7. **Theme logic** lives in `src/pkjs/custom-clay.js` (`COLOR_KEYS`, `THEMES`,
   `NEWER_KEYS`). Every new color key must be added to `COLOR_KEYS`, every
   theme array and `NEWER_KEYS`, with a value that keeps each theme's look.
   Re-run the mock Clay test (create `tests/test_custom_clay.js` if absent,
   mirroring Clay's `color` manipulator: `set()` accepts hex strings, `get()`
   returns an int, `set()` triggers `change` only on change).

### 2.3 Gates (owner approval required)

- **Design gate**: for every visual change (R3 indicator, R8 arc, R7 weather
  rendering, R9 charging look), show emery emulator screenshots (and one round
  screenshot) before finalizing.
- **PT2 gate**: sideload each release candidate to the PT2 and get the owner's
  confirmation of a short checklist (given per requirement below).
- **Release gate**: store upload, publish, commit, push and tag only when the
  owner says so, following the release skill.

---

## 3. Release 1.2.0

### R1. Timeline Quick View support

**Problem.** On rectangular watches (basalt, diorite, emery, flint), the
Timeline Quick View peek covers the bottom of the screen. Thin+ has no
`unobstructed_area` handling, so the bottom complication and the lower part of
the face are hidden.

**Requirements.**
- Subscribe with `unobstructed_area_service_subscribe` (guard with
  `PBL_API_EXISTS` or `PBL_RECT` as appropriate; round watches have no peek).
- When the unobstructed height is reduced:
  - Hide the **bottom** complication slot (it would be under the peek).
  - Keep the date column and top/left slots.
  - Hands and hour markers stay where they are (the face is analog; do not
    re-center or scale it).
- Restore everything when the peek leaves (handle `did_change`; animating via
  `change` is optional).
- No behavior change on round platforms.

**Acceptance.** Emulator evidence on emery and basalt: screenshots with
`emu-set-timeline-quick-view on` and `off`, bottom slot set to Steps. No crash
in logs. PT2 check: owner confirms the bottom number disappears while an event
peek is showing.

### R2. Settings that match the watch

**Problem.** The settings page offers options the watch cannot use (heart rate
on watches without a sensor, color pickers on black-and-white watches, health
slots on aplite).

**Requirements.**
- Use Clay `capabilities` on config items (supported names: `COLOR`, `BW`,
  `HEALTH`, `RECT`, `ROUND`, `PLATFORM_<NAME>`, each with optional `NOT_`
  prefix; see `node_modules/@rebble/clay/src/scripts/lib/utils.js`).
  - Theme select and all color pickers: `["COLOR"]`.
  - Complication selects: two variants with the **same messageKey** and
    exclusive capabilities, `["HEALTH"]` with health types and `["NOT_HEALTH"]`
    without Steps/Heart rate (and without R6 health types later).
  - R5 tap option: `["PLATFORM_EMERY"]`.
- `custom-clay.js` must tolerate missing items: `getItemByMessageKey` returns
  nothing for items not built on this watch. Skip theme logic entirely when
  the Theme item is absent.
- **Watch side, critical:** Clay does not send keys for items that were not
  built. `comm.c` currently calls `packet_get_*` for every key, so a missing
  key would turn toggles off and colors black. Change `comm.c` to apply a
  setting **only when its key is present** in the dictionary (`dict_find`),
  for every key. Add a host or emulator test for "missing key keeps the
  previous value".
- Heart rate on hardware without a sensor (Clay cannot tell; same platform can
  ship with or without HR): on the watch, treat the Heart rate slot as
  unavailable when `health_service_metric_accessible(HealthMetricHeartRateBPM,
  ...)` reports no availability, and draw nothing instead of `--`. Keep `--`
  for "sensor present, no reading yet".

**Acceptance.** Mock Clay tests pass with Theme/colors absent (BW) and present.
Host/emulator test proves missing keys keep previous values. Basalt emulator:
Heart rate slot draws nothing. PT2: settings page still shows everything it
showed before.

### R3. Disconnect alert

**Problem.** `bt_handler` in `src/c/windows/main_window.c` always calls
`vibes_long_pulse()` on disconnect, with no way to turn it off, and the only
visual cue is the 4px center dot turning into a hollow ring.

**Requirements.**
- New toggle **Vibrate on disconnect** (key `VibrateOnDisconnect`, default
  **on** = current behavior). Only shown/applicable when the disconnect
  indicator is enabled, or make it independent; document the choice.
- Clearer indicator, behind the existing **Show disconnected indicator**
  toggle. Proposal for the design gate: center dot drawn as a larger ring in a
  new color **Disconnected indicator** (key `ColorDisconnected`, default red on
  color watches, white on BW), plus optionally a small Bluetooth-off glyph
  under the 12 o'clock marker. Provide 2 mockups; owner picks.
- Use `emu-bt-connection --connected no` for evidence.

**PT2 check.** Turn phone Bluetooth off: indicator visible at a glance; buzz
follows the toggle.

### R4. README refresh and CI

- README: remove the stale "physical PT2 check is pending" text for 1.1.0 (the
  owner confirmed 1.1.0 works on his PT2 on 2026-10-19). Document new 1.2.0
  settings. Keep the credit to Chris Lewis.
- Add a GitHub Actions workflow at the **repo root**
  (`.github/workflows/thin-plus.yml`) that runs only for changes under
  `watchfaces/thin-plus/**`: install the Pebble tool and SDK, run
  `pebble build` in `watchfaces/thin-plus`, run the host tests and the mock
  Clay test. Pin tool/SDK versions to the ones used locally (Pebble Tool
  5.0.40, SDK 4.33.1). Verify the exact install commands locally first;
  if the SDK cannot be installed non-interactively in CI, build with what is
  possible and document the gap rather than faking a green check.
- Ask the owner whether to keep tracking `store/evidence/` and
  `store/releases/*/` logs in git or move them to an ignored location for new
  releases (existing history stays).

### R5. Tap to show the second hand (PT2 touchscreen)

- SDK 4.33.1 provides `touch_service_subscribe`/`touch_service_unsubscribe`
  (`PBL_TOUCH` is defined for emery). Guard all code with
  `#if defined(PBL_TOUCH)`.
- New toggle **Tap the face to show the second hand** (key `TapForSeconds`,
  default **off**, settings item capability `["PLATFORM_EMERY"]`). The
  description must say it may use more battery (the touch sensor is enabled
  while subscribed).
- On `TouchEvent_Liftoff` (a tap), call the existing `show_seconds()`. Only
  subscribe when the toggle and **Show second hand** are both on;
  unsubscribe otherwise (in `main_window_reload_config`).
- Touch probably cannot be simulated in the emulator; verify that it builds,
  that non-emery builds are unaffected, and test on the PT2.

**PT2 check.** With the option on, tapping the face shows the second hand for
15 s; with it off, taps do nothing.

### R9. Charging indicator

- When the battery is charging (`BatteryChargeState.is_charging`), the filled
  hour markers use a new color **Hour markers (charging)** (key
  `ColorCharging`, default green `00FF00` on color, white on BW), only when
  **Show battery level (hour markers)** is on. No animation (battery cost).
- Optional for the design gate: the same color for the Battery complication
  text while charging.
- Add the key to `COLOR_KEYS`, all `THEMES` and `NEWER_KEYS` (pick a value per
  theme that is visible on its background; Paper needs a dark green).
- Evidence: `emu-battery --percent 60 --charging`.

### R10. Startup animation toggle

- New toggle **Animate hands when the face opens** (key `EnableStartupAnim`,
  default **on** = current behavior). When off, skip the sweep in
  `main_window_push` and draw the current time immediately (make sure
  `s_animating` stays false and `animation_stopped`'s side effect,
  `main_window_reload_config()`, still happens once).

### 1.2.0 release checklist

- [ ] All R1–R5, R9, R10 acceptance items met; design gate approved.
- [ ] Clean build all 7 platforms, no new warnings; host + mock tests pass.
- [ ] Upgrade test: install over 1.1.0 with saved settings on emery; face
      unchanged.
- [ ] Settings dictionary size computed and recorded.
- [ ] Version `1.2.0` in `package.json`; PT2 gate passed (checklists above).
- [ ] Release notes drafted; release via the `thin-plus-release` skill at the
      release gate; tag `thin-plus-v1.2.0` after asking.

---

## 4. Release 1.3.0

### R6. More complication types

Append to `SlotType` (values are permanent):

| Value | Type | Display | Notes |
| --- | --- | --- | --- |
| 5 | Distance | `3.2` (km or mi, one decimal) | `HealthMetricWalkedDistanceMeters`; units from `health_service_get_measurement_system_for_display` |
| 6 | Active calories | `412` | `HealthMetricActiveKCalories` |
| 7 | Week number | `W43` | ISO week via `strftime("%V")` if supported, else compute |
| 8 | Second time zone | `14:05` | see below |
| 9 | Weather | `18°` | R7 |

- Health types follow the same availability rules as Steps (hidden when health
  is unavailable; only offered in the `["HEALTH"]` select variant).
- **Second time zone**: settings field (Clay select of common IANA zones, plus
  a text input fallback) key `SecondTimeZone`. The phone computes the
  zone's current UTC offset in minutes with `Intl.DateTimeFormat`
  (handles DST) and sends `TzOffsetMinutes` on settings save and on every
  weather/refresh cycle. The watch persists the offset and shows
  `gmtime(time(NULL) + offset)` formatted like the Digital time slot
  (12/24 h from `clock_is_24h_style()`). If no offset is known, draw nothing.
  Verify that `Intl` with `timeZone` works in the Pebble app's JS runtime;
  if not, fall back to a fixed-offset select (UTC-12..+14 in 15 min steps)
  and document the DST limitation in the setting's description.
- Text must fit in the left slot on 144-wide screens (check `W43`, `12:59`,
  `10.5`, `1234`).

### R7. Weather complication

- Data source: **Open-Meteo** (no API key):
  `https://api.open-meteo.com/v1/forecast?latitude=..&longitude=..&current=temperature_2m,weather_code`
  with `&temperature_unit=fahrenheit` for °F.
- Add `"location"` to `pebble.capabilities` in `package.json` (keep
  `"configurable"`). Use `navigator.geolocation.getCurrentPosition` with a
  timeout and a cached last position.
- Settings: **Temperature units** (°C/°F, key `WeatherUnits`, default °C),
  shown only when any slot is Weather is nice-to-have.
- Protocol:
  - Watch asks for an update (`WeatherRequest`) on launch if data is older
    than 30 min, and every 30 min on the minute tick, **only if a slot uses
    Weather**.
  - Phone replies with `WeatherTemp` (int, rounded) and `WeatherCode` (int).
  - Watch stores `{temp, code, timestamp}` under a **separate persist key**
    (do not grow `AppConfig` for volatile data).
  - Display `18°` (degree sign must exist in the font; verify, else `18`).
    If data is older than 3 hours, draw nothing (or `--`, decide at design
    gate).
  - Condition icon is optional; if added, use small PDC or bitmap resources
    and check resource size on aplite.
- Failure handling: no location, no network, HTTP error, timeout: keep the
  last good value, retry next cycle, log with `console.log` on the phone.
- Outbox currently 64 bytes; confirm it is enough for `WeatherRequest`.

### R8. Step-goal arc

- New toggle **Step goal ring** (key `EnableStepRing`, default off) and color
  **Step goal ring** (key `ColorStepRing`, default per theme).
- Goal: today's typical total from
  `health_service_sum_averaged(HealthMetricStepCount, time_start_of_today(),
  time_start_of_today() + SECONDS_PER_DAY, HealthServiceTimeScopeDaily)`;
  if unavailable or 0, fall back to 7,500 (document).
- Progress = steps today / goal, capped at 100%.
- Rendering: thin arc (2-3 px) just inside the hour markers using
  `graphics_draw_arc` with `GOvalScaleModeFitCircle` (round) or an
  equivalent rectangle-following path on rectangular screens. Provide
  mockups for both shapes at the design gate; the owner chooses.
- Must not cover the hour markers or the date column; drawn under the hands.
- Health-only; hidden when health is unavailable.

### R11. Date styles (owner-added scope, 2026-10-19)

- Append `DateStyle` to messageKeys and a `uint8_t date_style` to AppConfig.
  Set Full before reading saved data. Apply a received value only when its
  key is present; older saves and partial settings must preserve behavior.
- Add a **Date style** select, visible only when **Show current date** is on:
  **Full** (default, current Mon/19/Oct), **Day only** (19 vertically centered
  at three o'clock), and **Weekday and day** (Mon/19).
- Show native emery and gabbro screenshots of all three styles at the design
  gate before finalizing R11. Prior approval of R7/R8 remains valid.

### 1.3.0 release checklist

Same as 1.2.0, plus:
- [ ] Weather verified on the PT2 with real location (emulator JS can be
      exercised with `pebble install --emulator emery --logs` and `pypkjs`
      if available; otherwise PT2 only, stated as such).
- [ ] Location permission prompt and denial path tested on the phone.
- [ ] Store description updated for new complications and weather.
- [ ] Version `1.3.0`, tag `thin-plus-v1.3.0` after asking.

## 5. Reporting

At every gate, report three lists: verified in the emulator (with evidence
paths), verified on the PT2 by the owner, still pending. Never present an
emulator check as a physical one.
