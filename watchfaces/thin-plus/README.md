# Thin+

Thin, plus: a clean analog Pebble watchface with splashes of color and the
information you choose.

![Minimal Classic on Pebble Time 2](screenshots/emery.png)
![Ocean with digital time and steps on Pebble Time 2](screenshots/emery-medium.png)
![Sunset with all complications and thicker hands on Pebble Time 2](screenshots/emery-rich.png)

## Features

- Smooth, anti-aliased hands, precisely aligned tips, and optional thicker
  hour and minute hands.
- A battery-friendly second hand, shown for 15 seconds after launch or a
  wrist flick. Otherwise, the face updates once a minute.
- Three complication slots (top, left and bottom): steps, heart rate,
  battery percentage, digital time or none. Numbers only, without labels.
- Classic, Neon, Ocean, Sunset, Lime, Mono and Paper themes, plus Custom.
- Individual colors for the background, hands, tips, center dot, hour
  markers, empty battery markers and date.
- Hour markers that show battery level, optional date and disconnected
  indicator.

Keep it minimal: hide the date and leave any or all complication slots empty.

Settings are provided by [Clay](https://github.com/pebble/clay).
Colors and health readings depend on the watch's capabilities.

## Platforms

Targets aplite, basalt, chalk, diorite, emery, flint and gabbro. The release
preparation includes an install, default rendering and crash-log smoke test
for each platform; this does not verify the phone settings page on every watch.

![Gabbro](screenshots/gabbro.png)
![Chalk](screenshots/chalk.png)
![Basalt](screenshots/basalt.png)
![Aplite](screenshots/aplite.png)

## Build

With the Pebble SDK installed, run `pebble build`. The bundle is
`build/thin-plus.pbw`. Run `pebble clean` before rebuilding after changing
the message keys in `package.json`.

## Available release

[Thin+ 1.3.0 is available on the Pebble App Store](https://apps.repebble.com/b0a4b28dbe9440c3b19f68e3).
It is published and publicly listed. All seven platforms passed emulator checks,
and the owner approved the full PT2 checklist on the same sideloaded bytes.
The public PBW matches that tested candidate. The owner also confirmed installing
1.3.0 from the store, opening settings and applying a theme. See [listing](store/listing.md) and [release manifest](store/manifest.md).

Version 1.1.0 adds an option to show selected battery complications only below
20%. It defaults to off and is independent of the hour-marker battery display.
See [behavior and test notes](docs/LOW-BATTERY-COMPLICATION.md).

## New in 1.2.0

[Release details and verification](store/release-1.2.0.md).

- Timeline Quick View hides the bottom complication while the event peek is
  visible, then restores it. Hands, markers, date and other slots stay fixed.
- Settings match the watch: colors and themes appear on color watches; health
  complications appear on health-capable watches. Missing message keys preserve
  saved values, and heart-rate slots stay blank when a sensor is unavailable.
- **Vibrate on disconnect** defaults to on and applies when **Show disconnected
  indicator** is enabled. **Larger disconnected indicator** is opt-in and uses a larger center ring with a customizable color.
- **Tap the face to show the second hand** is available on PT2 only and defaults
  to off. It requires **Show second hand** and keeps the touch sensor enabled,
  which may use more battery. A tap shows seconds for 15 seconds.
- **Highlight hour markers while charging** is opt-in and requires the hour-marker
  battery display. Filled markers use the charging color; empty markers and
  complication text keep their usual colors. Paper uses dark green when chosen
  from the theme selector.
- **Animate hands when the face opens** defaults to off, showing the current
  time immediately. Turn it on to restore the opening sweep. Saved choices
  are preserved.

Both visual enhancements default to off so updates preserve the existing face.
See [implementation and verification notes](docs/IMPLEMENTATION-1.2.0.md) for
test evidence, remaining checks and the PT2 checklist.

## New in 1.3.0

The weather, ring and date-style designs are approved. The owner also confirmed
the updated custom-goal candidate on PT2 and approved its Emery/Gabbro previews.
The same tested package is now published as the latest public release.
See the [release record](store/release-1.3.0.md).
It adds distance,
active calories, ISO week, a second time zone and Open-Meteo temperature to
the complication choices, plus an optional step-goal ring. Existing slot
choices remain unchanged and the ring defaults to off.

**Date style** offers Full (the current weekday/day/month), Day only centered
at three o'clock, or Weekday and day. Full is the default. The select appears
only while **Show current date** is on and keeps its choice when hidden.

Weather uses location only when selected and refreshes every 30 minutes.
The approved design leaves weather blank when unavailable or more than
three hours old. Named time zones adjust for DST where the phone runtime
supports them; other runtimes offer a fixed UTC offset with a manual DST
adjustment. Under **Step goal ring**, **Goal** defaults to **Automatic**:
Pebble Health's typical daily step count, or 7,500 when unavailable or zero.
Choose **Custom** to reveal **Daily step goal**, a whole number from 1,000 to
100,000 (default 7,500). Switching back to Automatic retains your custom
target. These controls appear only on health-capable watches; the ring remains
off by default and progress stops at 100%. Invalid goals are rejected on both
the phone and watch without changing saved settings.

See [1.3.0 implementation and design review](docs/IMPLEMENTATION-1.3.0.md)
for evidence, runtime limitations and remaining release checks.

## Automated checks

The repository workflow [Thin+ checks](../../.github/workflows/thin-plus.yml)
runs for pushes and pull requests changing `watchfaces/thin-plus/**`. It uses
Pebble Tool **5.0.40**, SDK **4.33.1**, and Node 24, builds all seven platforms,
and runs:

```sh
python3 tests/test_low_battery.py
python3 tests/test_settings.py
python3 tests/test_interactions.py
python3 tests/test_complications.py
python3 tests/test_health.py
python3 tests/test_step_ring.py
node tests/test_custom_clay.js
node tests/test_weather.js
node tests/test_phone.js
node tests/check_settings_size.js
```

The pinned tool/SDK installation and build were rehearsed locally in a fresh,
isolated SDK directory. GitHub-hosted execution awaits an authorized push.
New emulator screenshots, build logs and release evidence go in ignored
`dist/verification/<version>/`; previously tracked store evidence stays in Git.

## Credit

Based on [Thin by Chris Lewis](https://apps.repebble.com/thin_550ccb556caaed4e0100006d).
Thin+ is maintained by Edward Wijaya.
