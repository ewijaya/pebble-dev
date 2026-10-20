# Thin+ — current store listing

Status: **1.3.0 published and publicly listed**. All seven native emulators passed,
and the owner approved the updated sideloaded PT2 checks and previews. Store-flow
installation, settings and theme application are also owner-confirmed. [Release evidence](release-1.3.0.md).

## Fields

- **Name:** Thin+
- **Type:** Watchface
- **Category:** Faces
- **Author:** Edward Wijaya
- **Price:** Free
- **Version:** 1.3.0
- **Platforms:** aplite, basalt, chalk, diorite, emery, flint, gabbro
- **Source:** https://github.com/ewijaya/pebble-dev/tree/watchface/thin-plus/watchfaces/thin-plus
- **Website:** Leave empty.

## Description

Thin, plus: a clean analog watchface with splashes of color and the information you choose.

Keep it minimal: hide the date and leave any or all complication slots empty.

- Three complication slots—top, left and bottom—show steps, heart rate, battery percentage, digital time, distance, active calories, ISO week number, a second time zone, weather or nothing.
- Three date styles: Full (weekday, day and month), Day only, or Weekday and day. The date can also be hidden completely.
- Weather in Celsius or Fahrenheit, using your phone's location only when a Weather slot is selected. It refreshes about every 30 minutes and hides readings older than three hours. Weather by Open-Meteo: https://open-meteo.com/
- A second time zone with named zones and daylight-saving adjustments where supported. Other phone runtimes offer a fixed UTC offset, adjusted manually for daylight saving.
- An optional step-goal ring follows the edge of the face. Automatic uses Pebble Health’s typical daily step count, with a 7,500-step fallback when unavailable or zero. Custom lets you choose a whole-number target from 1,000 to 100,000 and keeps it when you switch modes. Off by default, with a customizable color.
- Smooth, anti-aliased hands with precisely aligned tips. Turn on thicker hour and minute hands for extra weight.
- A second hand appears for 15 seconds after launch or a wrist flick. On Pebble Time 2, you can also enable a screen tap to show it. Tap detection is off by default and may use more battery.
- Seven themes: Classic, Neon, Ocean, Sunset, Lime, Mono and Paper, plus individual color controls.
- Hour markers double as a battery indicator. An optional charging highlight changes the filled markers' color while charging.
- Optional low-battery-only display: show selected battery percentages below 20%, and hide them at 20% or higher. Off by default; independent of the hour-marker battery indicator.
- Optional disconnected indicator, with a choice of the original small indicator or a larger colored center ring. Disconnect vibration can be switched off.
- Timeline Quick View hides the bottom complication during an event peek and restores it afterward on supported rectangular watches.
- Hands open at the current time by default. Enable “Animate hands when the face opens” if you prefer the opening sweep.

Available for all seven Pebble platforms. Settings adapt to your watch's capabilities; health features require Pebble Health, and heart-rate slots stay blank when a sensor is unavailable. Distance follows your km/mi preference. Both time complications follow your 12- or 24-hour preference.

Existing settings are preserved when updating. New complications are optional, the step ring starts off, and Full keeps the original date layout.

Based on Thin by Chris Lewis.
Original Thin: https://apps.repebble.com/thin_550ccb556caaed4e0100006d

## Release notes — 1.3.0

More information when you want it. A simpler face when you don't.

- New complications: distance, active calories, ISO week number, a second time zone and weather.
- Open-Meteo temperature in °C or °F, refreshed about every 30 minutes while selected. Weather uses phone location and hides readings older than three hours.
- Second time zone supports named zones with daylight-saving updates where available, or a fixed UTC-offset fallback.
- Optional step-goal ring with a customizable color. Automatic uses typical daily steps, falling back to 7,500; Custom accepts a daily goal from 1,000 to 100,000. Switching modes keeps your custom target.
- New Date style setting: Full, Day only, or Weekday and day. It appears only while Show current date is on.
- Existing saved settings and appearance are preserved. The step ring defaults to off and the date defaults to Full.

Supports all seven Pebble platforms; health features depend on the watch.

Based on Thin by Chris Lewis.

## Release notes — 1.2.0 (historical)

More control, with settings that fit your watch.

- Timeline Quick View now hides and restores the bottom complication during an event peek.
- Settings show options supported by your watch. Partial settings updates preserve omitted values, and opening settings preserves saved color overrides.
- Optional larger disconnect ring with a customizable color, plus a disconnect vibration switch.
- Optional screen tap to show seconds for 15 seconds on Pebble Time 2. Off by default; enabling touch detection may use more battery.
- Optional charging color for filled battery hour markers.
- Startup animation is now optional and defaults to off. Saved on/off choices are preserved.

Supports all seven Pebble platforms. The new disconnect and charging visuals are off by default.

Based on Thin by Chris Lewis.

## Release notes — 1.1.0 (historical)

Battery information when you need it.

- New optional setting: show battery percentage only below 20%. Applies to any top, left or bottom complication set to Battery. At 20% or higher, those slots stay blank; below 20%, their percentages appear.
- The option defaults to off, preserving existing settings and behavior.
- Battery changes immediately refresh the selected battery complications.
- Added a clearer explanation of the separate hour-marker battery indicator.

Supports all seven Pebble platforms.

Based on Thin by Chris Lewis.

## Release notes — 1.0.0 (historical)

First release of Thin+.

Adds smooth hands with aligned tips, an optional thicker-hand style, a second hand that appears briefly after launch or a wrist flick, three configurable complication slots, seven themes and individual color controls. Includes the original Thin's hour-marker battery display. Supports all seven Pebble platforms.

Based on Thin by Chris Lewis.

## Dashboard assets and suggested order

Dashboard requirements supplied by Edward on 2026-10-19 after reading the New App form code, without uploading or submitting anything:

- Optional icons: 80×80 small and 144×144 large, square. The form reportedly exposes these only for watchapps/plugins; keep the supplied icons available if a watchface icon field appears. Do not change the app type to expose it.
- Up to five screenshots per platform, exact native dimensions, PNG/JPEG/GIF, maximum 4.4 MB each.
- Optional per-platform banner: exactly 720×320, PNG/JPEG, maximum 4.4 MB.
- The in-app menu icon remains 25×25.

Emery upload order (five files), refreshed with owner approval on 2026-10-20:

1. `screenshots/emery-01-classic-signature.png` — Classic signature; teal goal ring at 50%, 5,000 steps toward a custom 10,000 goal, day-only date, seconds hand and dark-red center dot. Top and left slots hidden.
2. `screenshots/emery-02-classic-minimal.png` — pure Classic; seconds and dark-red dot, with date, ring and all complications hidden.
3. `screenshots/emery-03-ocean-weather.png` — Ocean; weather, digital time and weekday/day date.
4. `screenshots/emery-04-paper-second-time.png` — Paper; second time zone, battery and Full date, with the left slot empty.
5. `screenshots/emery-05-sunset-fitness.png` — Sunset; distance, active calories, steps, Full date, partial goal ring and thicker hands.

All five are native 200×228 captures of the unchanged published 1.3.0 binary.
Time, health values and weather are simulated demonstration data. This gallery
update preserves other platforms, icons, banner, copy, release and visibility.
[Capture and upload evidence](../dist/verification/1.3.0/gallery-refresh-2026-10-20/).

Each other platform uses its `*-classic-minimal.png`, `*-classic-medium.png`, and `*-classic-rich.png` images in that order. Medium shows digital time and date. Rich enables all complication slots, subject to platform capabilities. The final selection and provenance are recorded in `screenshot-selection.json`: 23 native images total. Superseded images remain in `evidence/previous-screenshots/` for the approval audit.

The Emery banner uses the minimal Classic face and Edward's selected tagline: **The Thin you love. More ways to make it yours.** The screenshot remains at its native 200×228 resolution inside the 720×320 banner.

## Release status and remaining check

Release **1.3.0** (`0eacf6a087fb4fc38af9f2d7`) is published and publicly listed.
All seven fresh public catalogs select it as latest. The public download matches
the owner-tested candidate. Description and notes are verified in the catalogs;
the canonical webpage initially retained cached 1.2.0 content. Existing artwork
and listed visibility were preserved.

The owner approved the updated sideloaded PT2 checks, then confirmed installing
1.3.0 from the store, opening settings and applying a theme. Release source is
identified by the `thin-plus-v1.3.0` GitHub tag.

Evidence: `../dist/verification/1.3.0/publication/`.
