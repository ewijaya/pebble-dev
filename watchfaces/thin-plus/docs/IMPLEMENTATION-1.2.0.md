# Thin+ 1.2.0 implementation and design gate

Status on 2026-10-19: **1.2.0 is published and publicly listed** after explicit
upload and publication approvals. The owner approved all six sideloaded PT2
checks. The public download matches the tested candidate; all seven public
catalogs and the canonical page show 1.2.0 and the updated description.
Release ID: `e62d92c454904747b53fe0ea`. No commit, push or tag was performed.
Release 1.3.0 has not been started. The PT2 store-flow check remains pending.

## Decisions and compatibility

- After confirming the startup animation toggle works on PT2, the owner asked
  for it to default **off**. This explicitly supersedes R10's original default-on
  requirement: new installs and upgrades without this field skip the sweep.
  An existing saved 1.2.0 choice (on or off) is preserved.

- Owner approved keeping the new disconnect and charging visuals **opt-in**.
  `EnableEnhancedBT` and `EnableChargingColor` both default to false. Existing
  users keep the old disconnect ring and marker colors until enabling them.
- Vibration is conditional on **Show disconnected indicator**, as before;
  `VibrateOnDisconnect` defaults to true. Startup animation defaults to false;
  `TapForSeconds` defaults to false and appears only on Emery.
- The original 20-byte 1.1.0 config is an unchanged prefix. All seven new fields
  and message keys are appended. Both new colors start with `GColorClear` before
  reading storage and receive their fallback afterward. No slot values changed.
- Every toggle, color and slot is applied only if present in the AppMessage.
  Missing and unknown keys cannot clear saved values. Opening Clay also no
  longer reapplies a preset over saved individual color overrides.
- Theme/colors use `COLOR`; each slot has exclusive `HEALTH`/`NOT_HEALTH`
  variants. Aplite cannot select health slots. Heart-rate rendering checks metric
  accessibility; Basalt and Chalk, which have no HR sensor, are excluded even
  though their emulator can claim metric accessibility. Sensor-present/no-reading
  still displays `--`.
- Maximum Clay dictionary: **296 bytes on Emery**, 285 on other color platforms,
  138 on BW platforms. Includes a one-byte dictionary count, seven-byte tuple
  headers, four-byte integer/boolean values and longest select strings including
  NUL. The existing 512-byte inbox is retained; all are below 480 bytes.
- Owner chose ignored evidence for new releases. Use
  `dist/verification/<version>/`; existing tracked store evidence is retained.

## Design review

The boards contain enlarged native emulator screenshots, not generated artwork.
R3 disconnect captures retain `.raw.png` framebuffer originals alongside
brightness-normalized PNGs. The normal screenshot connection can reconnect BT
or time out while disconnected, so these use the SDK's QEMU framebuffer capture
after the real `emu-bt-connection --connected no` command. PebbleOS debounces
disconnect notifications for 25 seconds; tests wait 27 seconds before capture.

- [A/B disconnect comparison](../dist/verification/1.2.0/design-gate/disconnect-options.png):
  A is a larger ring; B adds a small Bluetooth-off glyph below the 12 marker.
  Both are shown on Emery and Chalk. The owner selected A; production uses the
  ring. The alternate glyph remains only as a reproducible review fixture.
- [Charging comparison](../dist/verification/1.2.0/design-gate/charging-review.png):
  Classic green and Paper dark-green filled hour markers at 60%, on Emery and
  Chalk. Empty markers and battery text keep their ordinary colors. Highlighting
  requires both the hour-marker battery display and the opt-in charging toggle.

## Verified in the emulator

Paths below are relative to the project root. Captures and command/runtime logs
are kept together. No app crash or assertion messages were observed in the
successful runs; the phone simulator emits existing QEMU-footer decode warnings.

| Requirement | Verification | Evidence |
| --- | --- | --- |
| R2 | Basalt HR slot blank; changing only the date preserves other settings | `dist/verification/1.2.0/r2-fixed/basalt-heart-rate-unavailable.png`, `basalt-partial-before.png`, `basalt-partial-date-off.png`, `basalt-partial-restored.png` |
| R1 | Emery and Basalt Quick View off/on/off; bottom Steps hidden/restored, date/top/left/geometry retained | `dist/verification/1.2.0/r1/{emery,basalt}-quick-view-{off,on,off-restored}.png` |
| R3 | Real debounced disconnect/reconnect on Emery and Chalk; both designs captured | `dist/verification/1.2.0/r3-final-{ring,glyph}/{emery,chalk}-disconnected-enhanced.png` and matching runtime logs |
| R5 | Seconds disabled, wrist-flick seconds visible, then hidden after 15 seconds on Emery and Basalt; non-touch platform runs | `dist/verification/1.2.0/r5/{emery,basalt}-{seconds-disabled,wrist-seconds-visible,seconds-expired}.png` |
| R9 | Normal/charging at 60%, opt-out, hour-marker display off, and Paper charging on Emery and Chalk | `dist/verification/1.2.0/r9/{emery,chalk}-{normal-60,charging-60,charging-opt-out,hour-markers-off,paper-charging-60}.png` |
| R10 | Both saved animation settings reinstall and reach the working face on Emery | `dist/verification/1.2.0/r10/emery-startup-{off,on}.png` |
| Upgrade | Released 1.1.0 -> candidate, custom colors/thick hands/slots retained; identical native screenshot pixels at the same time; every old message-key ID unchanged | `dist/verification/1.2.0/upgrade/result.json`, `before-1.1.0.png`, `after-candidate.png` |

Touchscreen liftoff was **not** simulated. `emu-tap` is an accelerometer gesture,
not a touchscreen event. Actual touch and vibration remain physical PT2 checks.
Host tests exercise the real touch handler, subscription logic, vibration edges,
15-second timer/rescheduling, and animation-off initialization exactly once.

The earlier `r3-ring`, `r3-glyph` and preliminary captures from before the debounce
fix are superseded by `r3-final-ring` and `r3-final-glyph`. A Basalt install failed
once and passed after restarting the emulator without wiping state. An initial
upgrade comparison caught unsynchronized emulator clocks; the final comparison
uses the SDK double-set/settle pattern and passes pixel equality.

## Updated candidate: startup animation defaults off

At the owner's request, the C and Clay defaults are both off. Saved choices
are retained, including a saved on value. The owner confirmed that the startup
animation toggle itself works on PT2 before requesting this default change.

- Current candidate: `dist/verification/1.2.0/final-startup-off/thin-plus.pbw`.
- SHA-256: `9a015a16f59e33794dabc7f5f47d825ec32c2c1e52893daa7dc5a330e66513f5`.
- Clean builds passed on all seven platforms with only the seven existing RWX
  linker warnings. ZIP and identity validation passed.
- Host tests confirm default-off for new and 1.1.0-prefix configurations, saved
  on persistence, and immediate startup behavior. Clay tests confirm default-off
  and saved-on preservation on all seven platform profiles.
- Emery smoke passed and the native screenshot was inspected:
  `dist/verification/1.2.0/final-startup-off/emery-smoke.png`.
- Upgrade from the released 1.1.0 PBW preserves the settled face pixel-for-pixel:
  `dist/verification/1.2.0/upgrade-final-startup-off/result.json`.
- Updated candidate successfully installed on PT2 through CloudPebble:
  `dist/verification/1.2.0/final-startup-off/pt2-install.log`.
- All seven current candidate binaries have now passed emulator smoke checks;
  screenshots were inspected and logs show no app crash/assertion messages.
- Earlier candidate evidence below is retained; it refers to the previous PBW.

## Previous 1.2.0 candidate

- Owner selected disconnect A (larger center ring) and approved charging visuals.
- Package and lockfile are 1.2.0. Both new visual options remain off by default.
- Final PBW: `dist/verification/1.2.0/final/thin-plus.pbw` (530,873 bytes).
- SHA-256: `90bd61b679784c96409ce177897284c13244773f991f6dd142c99f1b0d8cee53`.
- Clean build, ZIP integrity, all seven platform entries, unchanged UUID and old
  message-key IDs, and no source test overrides: `final/validation.json`.
- Final build has only the seven existing linker RWX warnings. All host and
  Clay tests passed again; dictionary maximum remains 296 bytes.
- All seven final platform binaries installed and rendered successfully. Native
  screenshots were visually inspected; runtime logs contain no app crash or
  assertion messages: `final/{aplite,basalt,chalk,diorite,emery,flint,gabbro}-smoke.png`,
  matching runtime logs, and `final/captures.json`.
- Upgrade from the frozen 1.1.0 PBW to this exact 1.2.0 PBW preserved the saved
  custom face pixel-for-pixel: `upgrade-final/result.json`, `before-1.1.0.png`,
  and `after-candidate.png`. The frozen 1.1.0 PBW remains intact.
- Evidence references in this section are under `dist/verification/1.2.0/`.

## Build, host tests and CI

- Clean seven-platform candidate build: `dist/verification/1.2.0/design-gate/build.log`.
  Only the seven existing linker RWX warnings remain; no new compiler warnings.
- Host ASan/UBSan tests: `dist/verification/1.2.0/host/{low-battery,settings,interactions}.log`.
  Covers legacy/1.1.0 prefix migration, new-field persistence, omitted keys,
  0/1/19/20/21/100% thresholds, HR availability and bottom-slot visibility.
- Mock Clay: `dist/verification/1.2.0/host/clay.log`; all seven capabilities,
  exclusive selects, missing/partial items, saved overrides and seven themes.
- Dictionary calculation: `dist/verification/1.2.0/host/dictionary-size.json`.
- Fresh isolated tool/SDK install plus `npm ci`, seven-platform build and host/Clay
  checks: `dist/verification/1.2.0/r4/{tool-install,sdk-install,ci-rehearsal}.log`.
  Pebble Tool 5.0.40 and SDK 4.33.1 install without interaction using:

  ```sh
  uv tool install --python /usr/bin/python3 pebble-tool==5.0.40
  pebble sdk install 4.33.1
  ```

  This follows the [official installation procedure](https://developer.repebble.com/sdk/)
  with pinned versions. `.github/workflows/thin-plus.yml` runs only for changes
  under this app. GitHub-hosted execution still awaits an authorized push.
- Source contains zero `TEMP_TEST` markers. Scratch builds exclude Waf lock
  files as well as build/dist directories. A copied Waf lock initially allowed
  scratch cleanup to remove the local build directory; `build/thin-plus.pbw` was
  restored from the intact frozen 1.1.0 PBW at that checkpoint. The frozen 1.1.0
  copy still has SHA-256
  `15e75184f8381cc19a94fbbcd192323251a2ae9bd0cf5e1676d64b22c50131fd`.

## Physical installation

CloudPebble reported **App install succeeded.** for the exact validated 1.2.0
PBW at `build/thin-plus.pbw`. Latest evidence:
`dist/verification/1.2.0/final-startup-off/pt2-install.log`. The earlier
`final/pt2-install-retry.log` records the previous candidate installation. The initial timeout evidence is retained.
Successful installation is separate from the owner's functional checks.

## Verified by the owner on PT2

- Version **1.1.0** works on the owner's physical PT2, confirmed 2026-10-19 in
  the approved PRD. Its prior pending note has been removed from the README.
- Owner confirmed **all six 1.2.0 PT2 checklist items** after installing the
  startup-default-off candidate: “I checked all approve all!” This covers saved
  settings, Quick View, disconnect controls, touch seconds, charging colors and
  startup animation. Evidence: `dist/verification/1.2.0/release-prep/pt2-approval.json`.
- This is a sideload result; the 1.2.0 store install/settings/theme flow remains
  pending owner confirmation after installing the published release.

## Pending

1. Confirm the 1.2.0 PT2 store-install/settings/theme flow. The sideload checklist
   has already passed; store publication does not establish this separate flow.
2. Commit, push and tag await explicit authorization. GitHub-hosted CI awaits a
   push; the local fresh-install CI rehearsal passed.
3. Start 1.3.0 only when the owner says go.

Publication evidence: `dist/verification/1.2.0/publication/` contains owner
approvals, the draft download comparison, dashboard snapshots, all seven public
catalogs, the matching public PBW digest and the canonical-page check.

## PT2 checklist

- Upgrade keeps your saved colors, date, slots, hand thickness and battery
  behavior. Open settings: existing PT2 options are still present; saving them
  applies correctly.
- With Steps in the bottom slot, an event peek hides that number and closing
  the peek restores it; top/left slots, date and hand positions stay put.
- Enable the larger disconnect indicator and turn phone Bluetooth off. After
  the system's disconnect delay, the chosen indicator is easy to see. Vibration
  follows its toggle; disabling Show disconnected indicator suppresses both.
  System-level disconnect vibration, if separately enabled, is independent.
- With Show second hand and Tap the face enabled, a screen tap shows seconds
  for 15 seconds. With tap disabled, tapping does nothing; wrist flicks retain
  their existing behavior. With Show second hand disabled, neither shows it.
- Enable charging highlight and the hour-marker battery display. On the
  charger, filled markers use the charging color; off the charger they return
  to their normal color. Turning either relevant toggle off removes the effect.
- Turn startup animation off and reopen the face: current time appears without
  the sweep. Turn it back on and reopen: the familiar sweep returns.
