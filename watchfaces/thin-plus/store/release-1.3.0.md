# Thin+ 1.3.0 — release record

Status: **published and publicly listed**, 2026-10-19.
The owner confirmed the updated candidate on PT2 and approved the custom-goal
previews, then explicitly approved the release review, upload and making 1.3.0
the latest public version. The owner subsequently confirmed the PT2 store flow
and requested the missing GitHub release tags.

## Frozen candidate

- App: Thin+ / Watchface / Faces, Edward Wijaya.
- Existing listing: https://apps.repebble.com/b0a4b28dbe9440c3b19f68e3
- Version: **1.3.0**; UUID `0e83e240-01b8-469b-a51b-b2a0e767fefb`.
- [Frozen PBW](../dist/releases/1.3.0/thin-plus.pbw): **600,042 bytes**.
- SHA-256: `b25a9fdbe9b55c30ed6fd1dc1df62c0412ea844976e0d8035033303513f656a7`.
- [Release manifest](../dist/releases/1.3.0/manifest.json), complete source
  snapshot and binary source patch are frozen beside the PBW. Source base:
  `246a67973784e4f03d3d709c7c0f82eba1efed12`, plus uncommitted inputs recorded
  in the manifest. The base commit alone does not reproduce this release.
- Targets: aplite, basalt, chalk, diorite, emery, flint, gabbro.
- [Clean build and package validation](../dist/verification/1.3.0/custom-goal-final/validation.json):
  all seven targets; ZIP/metadata valid; zero compiler warnings and seven known
  SDK linker notices. Aplite RAM: 15,534 / 24,576 bytes, linker-estimated heap
  headroom: 9,042 bytes; resources: 19,204 / 131,072 bytes.
- [Native emulator smoke review](../dist/verification/1.3.0/final-custom-goal-smoke/smoke-review.json):
  all seven render with crash-free app logs. Chalk used direct SDK transport;
  simulated phone transport was unreliable. Emery reopening was blocked by
  full emulator BlobDB after successful goal captures; host, Gabbro and the
  owner-confirmed PT2 check cover persistence. No emulator data was wiped.
- Ten host suites passed, including migration, phone/watch validation, Clay
  visibility, automatic fallback and progress below/at/above target.
- [PT2 and preview confirmation](../dist/verification/1.3.0/release-prep-custom-goal/owner-confirmation.json):
  saved face unchanged, Custom = 10,000, mode-switch/reopen persistence,
  invalid-input rejection and target retention with the ring off.
- Maximum settings dictionary: 367 bytes, inbox: 512; refresh request: 34
  bytes, outbox: 64. New goal fields and message keys are appended.

## Published description

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

## Published release notes

More information when you want it. A simpler face when you don't.

- New complications: distance, active calories, ISO week number, a second time zone and weather.
- Open-Meteo temperature in °C or °F, refreshed about every 30 minutes while selected. Weather uses phone location and hides readings older than three hours.
- Second time zone supports named zones with daylight-saving updates where available, or a fixed UTC-offset fallback.
- Optional step-goal ring with a customizable color. Automatic uses typical daily steps, falling back to 7,500; Custom accepts a daily goal from 1,000 to 100,000. Switching modes keeps your custom target.
- New Date style setting: Full, Day only, or Weekday and day. It appears only while Show current date is on.
- Existing saved settings and appearance are preserved. The step ring defaults to off and the date defaults to Full.

Supports all seven Pebble platforms; health features depend on the watch.

Based on Thin by Chris Lewis.

## Presentation retained

The live artwork URLs match the previously approved 1.2.0 presentation. Keep
the icons, banner and screenshot order as they are; the new features are
introduced in the description and release notes above.

- Rectangular PT2-style icons: [80px](icons/thin-plus-80.png),
  [144px](icons/thin-plus-144.png). The embedded 25px menu icon is unchanged.
- [Classic banner](banner-emery-720x320.png): visible seconds hand and dark-red
  center dot. Tagline: **The Thin you love. More ways to make it yours.**
- Five emery screenshots: Classic minimal, Neon date, Ocean medium, Paper rich,
  Sunset rich. [Review the Emery gallery](../dist/verification/1.3.0/release-prep-custom-goal/preview-emery.png).
- Three screenshots for each other platform: minimal, medium and rich.
  [Review other platforms](../dist/verification/1.3.0/release-prep-custom-goal/preview-platforms.png).
- All 23 gallery files retain their original native pixels, dimensions and
  order. They demonstrate existing configurations still supported by 1.3.0;
  they are not presented as newly captured 1.3.0 weather screenshots.
- Existing selection is recorded in `store/screenshot-selection.json`.
  [Release asset inventory](../dist/verification/1.3.0/release-prep-custom-goal/asset-inventory.json) records all 26 files, dimensions, sizes and hashes.

## Publication and remaining check

Release `0eacf6a087fb4fc38af9f2d7` is published, and the listing remains publicly listed.
All seven fresh public catalogs identify **1.3.0** as the latest release and
show the reviewed description and notes. The unauthenticated public PBW download
matches the owner-tested frozen package exactly. Existing artwork, previous
releases and unrelated listing fields were preserved. All eight descriptions
and the release notes retain **Based on Thin by Chris Lewis.**

The canonical webpage initially retained cached 1.2.0 content despite the fresh
catalogs serving 1.3.0. See [public verification](../dist/verification/1.3.0/publication/public-download-verification.json)
for the final page check. No additional publication or visibility change is needed.

[Authorization and read-back evidence](../dist/verification/1.3.0/publication/)
records the upload, exact remote bytes, publication and copy update separately.
The pre-publication review is preserved there.

The owner subsequently confirmed installing **1.3.0 from the store** on PT2,
opening settings and applying a theme. Both sideload and store-flow checks are
complete. Source is recorded by `thin-plus-v1.3.0`; the missing 1.2.0 source
snapshot is recorded separately by `thin-plus-v1.2.0`. Each tag is checked
against the original released build-input hashes.
