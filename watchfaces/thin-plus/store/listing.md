# Thin+ — current store listing

Status: 1.1.0 is published and publicly listed after the owner explicitly requested a version bump and release. All seven platforms passed final-candidate emulator checks. Physical PT2 verification of 1.1.0 is pending. The historical 1.0.0 listing and approvals are preserved in `releases/1.0.0/listing.md`.

## Fields

- **Name:** Thin+
- **Type:** Watchface
- **Category:** Faces
- **Author:** Edward Wijaya
- **Price:** Free
- **Version:** 1.1.0
- **Platforms:** aplite, basalt, chalk, diorite, emery, flint, gabbro
- **Source:** https://github.com/ewijaya/pebble-dev/tree/watchface/thin-plus/watchfaces/thin-plus
- **Website:** Leave empty.

## Description

Thin, plus: a clean analog watchface with splashes of color and the information you choose.

Keep it minimal: hide the date and leave any or all complication slots empty.

- Smooth, anti-aliased hands with precisely aligned tips. Turn on thicker hour and minute hands for extra weight.
- A battery-friendly second hand appears for 15 seconds after launch or a wrist flick. Otherwise, the face updates once a minute.
- Three complication slots—top, left and bottom—show steps, heart rate, battery percentage, digital time or nothing. Just the numbers, without labels.
- Seven themes: Classic, Neon, Ocean, Sunset, Lime, Mono and Paper.
- Custom colors for the background, hour/minute hands, hand tips, center dot, second hand and tip, hour markers and empty battery markers, day of month and date text.
- Hour markers double as a battery indicator.
- Optional low-battery-only display: show selected battery percentages below 20%, and hide them at 20% or higher. Off by default; independent of the hour-marker battery indicator.
- Optional date and disconnected indicator.

Available for all seven Pebble platforms. Colors and health readings depend on your watch's capabilities. Digital time follows your 12- or 24-hour preference.

Based on Thin by Chris Lewis.
Original Thin: https://apps.repebble.com/thin_550ccb556caaed4e0100006d

## Release notes — 1.1.0

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

Emery upload order (five files):

1. `screenshots/emery-01-classic-minimal.png` — minimal Classic; visible seconds hand and dark-red center dot, with date and complications hidden.
2. `screenshots/emery-02-neon-date-only.png` — light Neon; date only.
3. `screenshots/emery-03-ocean-medium.png` — medium Ocean; digital time and steps, with date and left slot hidden.
4. `screenshots/emery-04-paper-rich.png` — rich Paper; digital time, battery, steps and date.
5. `screenshots/emery-05-sunset-rich.png` — rich Sunset; all complications, thicker hands and 40% battery markers.

Each other platform uses its `*-classic-minimal.png`, `*-classic-medium.png`, and `*-classic-rich.png` images in that order. Medium shows digital time and date. Rich enables all complication slots, subject to platform capabilities. The final selection and provenance are recorded in `screenshot-selection.json`: 23 native images total. Superseded images remain in `evidence/previous-screenshots/` for the approval audit.

The Emery banner uses the minimal Classic face and Edward's selected tagline: **The Thin you love. More ways to make it yours.** The screenshot remains at its native 200×228 resolution inside the 720×320 banner.

## Release status and remaining check

The owner explicitly requested the 1.1.0 version bump and release. The candidate
was uploaded as a draft, downloaded and checked byte-for-byte, then published.
The existing publicly listed visibility and approved gallery, banner and icons
were preserved. The description now includes the optional low-battery setting.

Release ID: `0e3dc4efd60e460586b8dff5`. Evidence: `releases/1.1.0/`.

PT2: the 1.0.0 store-install/settings/theme test was previously confirmed by the
owner. For 1.1.0, installation from the store, settings/theme application and the
new battery option still require the owner's physical check. No Git commit,
push or tag was performed as part of this release.
