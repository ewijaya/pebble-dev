# Thin+ 1.2.0 — release review

Status: **published and publicly listed** after explicit upload and publication
approval. Release ID: `e62d92c454904747b53fe0ea`. The owner approved every PT2
checklist item on the sideloaded candidate. Draft and public downloads both match
the frozen PBW. The PT2 store-flow check and Git actions remain pending.

## Candidate

- Version: **1.2.0**, all seven platforms; existing app and UUID retained.
- Frozen PBW: [thin-plus.pbw](../dist/releases/1.2.0/thin-plus.pbw).
- Size: **530,875 bytes**.
- SHA-256: `9a015a16f59e33794dabc7f5f47d825ec32c2c1e52893daa7dc5a330e66513f5`.
- Startup animation defaults **off**, as requested; saved choices are retained.
- Larger disconnect ring and charging colors remain opt-in.
- [Evidence and source manifest](../dist/verification/1.2.0/release-prep/manifest.json).
- [Implementation and PT2 checklist](../docs/IMPLEMENTATION-1.2.0.md).

## Published description

Thin, plus: a clean analog watchface with splashes of color and the information you choose.

Keep it minimal: hide the date and leave any or all complication slots empty.

- Smooth, anti-aliased hands with precisely aligned tips. Turn on thicker hour and minute hands for extra weight.
- A second hand appears for 15 seconds after launch or a wrist flick. On Pebble Time 2, you can also enable a screen tap to show it. Tap detection is off by default and may use more battery.
- Three complication slots—top, left and bottom—show steps, heart rate, battery percentage, digital time or nothing. Just the numbers, without labels.
- Seven themes: Classic, Neon, Ocean, Sunset, Lime, Mono and Paper.
- Custom colors for the background, hands and tips, center dot, date, battery hour markers, charging highlight and larger disconnect indicator.
- Hour markers double as a battery indicator. An optional charging highlight changes the filled markers' color while charging.
- Optional low-battery-only display: show selected battery percentages below 20%, and hide them at 20% or higher. Off by default; independent of the hour-marker battery indicator.
- Optional date and disconnected indicator, with a choice of the original small indicator or a larger colored center ring. Disconnect vibration can be switched off.
- Timeline Quick View hides the bottom complication during an event peek and restores it afterward on supported rectangular watches.
- Hands open at the current time by default. Enable “Animate hands when the face opens” if you prefer the opening sweep.

Available for all seven Pebble platforms. Settings adapt to your watch's capabilities; heart-rate slots stay blank when the sensor is unavailable. Digital time follows your 12- or 24-hour preference.

Based on Thin by Chris Lewis.
Original Thin: https://apps.repebble.com/thin_550ccb556caaed4e0100006d

## Published release notes

More control, with settings that fit your watch.

- Timeline Quick View now hides and restores the bottom complication during an event peek.
- Settings show options supported by your watch. Partial settings updates preserve omitted values, and opening settings preserves saved color overrides.
- Optional larger disconnect ring with a customizable color, plus a disconnect vibration switch.
- Optional screen tap to show seconds for 15 seconds on Pebble Time 2. Off by default; enabling touch detection may use more battery.
- Optional charging color for filled battery hour markers.
- Startup animation is now optional and defaults to off. Saved on/off choices are preserved.

Supports all seven Pebble platforms. The new disconnect and charging visuals are off by default.

Based on Thin by Chris Lewis.

## Selected artwork

Retain the existing approved artwork and its order. The update preserves these
settled layouts; its new disconnect and charging appearances are optional.
No new artwork upload is proposed.

- Rectangular store icons: [80 px](icons/thin-plus-80.png), [144 px](icons/thin-plus-144.png).
- [Classic banner](banner-emery-720x320.png), with visible seconds and a dark-red
  center dot. Tagline: **The Thin you love. More ways to make it yours.**
- Emery: [Classic minimal](screenshots/emery-01-classic-minimal.png),
  [Neon date only](screenshots/emery-02-neon-date-only.png),
  [Ocean medium](screenshots/emery-03-ocean-medium.png),
  [Paper rich](screenshots/emery-04-paper-rich.png),
  [Sunset rich](screenshots/emery-05-sunset-rich.png).
- Each other platform: existing Classic minimal, medium and rich screenshots,
  as recorded in [the selection manifest](screenshot-selection.json).

## Publication verification

- Draft upload and publication were separately authorized and completed.
- Draft and public downloads match the frozen candidate byte-for-byte.
- All seven public catalogs expose 1.2.0, with matching description and notes.
- The canonical page shows 1.2.0, the new description and the exact credit.
- Existing icons, banner, 23 screenshots, metadata, earlier releases and listed
  visibility were preserved.
- [Publication evidence](../dist/verification/1.2.0/publication/).

Pending: owner PT2 install from the store, settings and theme check; explicit
commit/push/tag authorization. No 1.3.0 work until the owner says go.
