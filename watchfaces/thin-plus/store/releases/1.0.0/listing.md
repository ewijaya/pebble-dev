# Thin+ — approved store listing

Status: Gate A approved by Edward on 2026-10-19 ("I approve all"). Release 1.0.0 was published on 2026-10-19 after Edward said "okay relese them". Edward confirmed the Gate B PT2 test and authorized publicly listed visibility; Gate C is complete.

## Fields

- **Name:** Thin+
- **Type:** Watchface
- **Category:** Faces
- **Author:** Edward Wijaya
- **Price:** Free
- **Version:** 1.0.0
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
- Optional date and disconnected indicator.

Available for all seven Pebble platforms. Colors and health readings depend on your watch's capabilities. Digital time follows your 12- or 24-hour preference.

Based on Thin by Chris Lewis.
Original Thin: https://apps.repebble.com/thin_550ccb556caaed4e0100006d

## Release notes — 1.0.0

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

1. `screenshots/emery-01-classic-minimal.png` — minimal Classic; hands and markers only.
2. `screenshots/emery-02-neon-date-only.png` — light Neon; date only.
3. `screenshots/emery-03-ocean-medium.png` — medium Ocean; digital time and steps, with date and left slot hidden.
4. `screenshots/emery-04-paper-rich.png` — rich Paper; digital time, battery, steps and date.
5. `screenshots/emery-05-sunset-rich.png` — rich Sunset; all complications, thicker hands and 40% battery markers.

Each other platform uses its `*-classic-minimal.png`, `*-classic-medium.png`, and `*-classic-rich.png` images in that order. Medium shows digital time and date. Rich enables all complication slots, subject to platform capabilities. The final selection and provenance are recorded in `screenshot-selection.json`: 23 native images total. Superseded images remain in `evidence/previous-screenshots/` for the approval audit.

The Emery banner uses the minimal Classic face and Edward's selected tagline: **The Thin you love. More ways to make it yours.** The screenshot remains at its native 200×228 resolution inside the 720×320 banner.

## Approval and later steps

Gate A approved: Edward approved the icon, screenshot selection, banner and listing text, including the author field, on 2026-10-19 ("I approve all"). The approval is recorded in `evidence/gate-a-approval.json`. That approval was recorded without a store write. Edward subsequently authorized programmatic creation/upload and the shorter credit line. No commit, push or tag followed.

The authorized API setup is complete: [Thin+ dashboard](https://developer.repebble.com/dashboard/apps/b0a4b28dbe9440c3b19f68e3/edit). App ID `b0a4b28dbe9440c3b19f68e3`; release ID `c652f752f6254eb694d76511`. The approved PBW and Emery banner were uploaded and checked. Edward later requested minimal layouts; the gallery was revised to show minimal, medium and rich layouts. Listing visibility is **listed**; release 1.0.0 is **published**. The PBW is not included in `store/`.

The creation endpoint did not retain the optional store icon fields for this watchface. The edit endpoint accepts them: the 80×80 and 144×144 icons are saved there. Edward subsequently requested a rectangular PT2-style outline for these store icons. The separate 25×25 menu icon is embedded in the verified PBW. The existing developer account displays **Edward**, matching the other listings; its global profile was not changed. The PBW author remains Edward Wijaya.

Release publication is complete after Edward's explicit go-ahead. The public API exposes version 1.0.0, and an unauthenticated PBW download matches the approved SHA-256 exactly. Edward then confirmed the PT2 test and authorized listed visibility. Public API visibility is now true. See `evidence/release-publication.json` and `evidence/listed-publication.json`.

Gate B is complete based on Edward's confirmation of installation **from the store**, opening settings and applying a theme on PT2. Gate C is complete after his explicit listed-visibility instruction. README includes the verified store link. Committing, pushing and tagging `thin-plus-v1.0.0` remain pending separate authorization.
