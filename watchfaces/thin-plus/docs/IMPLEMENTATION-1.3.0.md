# Thin+ 1.3.0 implementation

Status: **published and publicly listed; PT2 store-flow check confirmed**, 2026-10-19.
The owner approved the R7/R8 and R11 designs and the earlier sideloaded candidate.
After the configurable step goal was added and the updated 600,042-byte package
was sideloaded, the owner confirmed: “All checks pass; I approve the custom-goal
previews too”. This covers the updated goal checks and Emery/Gabbro previews.
Version remains 1.3.0. See [release review](../store/release-1.3.0.md) for the
frozen candidate and published copy. The owner explicitly approved upload and
public publication; the public download matches the tested bytes. The owner
then confirmed the PT2 store-install/settings/theme check and requested GitHub
release tags. Source is identified by `thin-plus-v1.3.0`.

## Configurable step goal

Under Step goal ring, Goal offers Automatic (default) and Custom on health
platforms only. Goal remains visible while the ring is off, allowing users to
set their target first. Daily step goal appears only for Custom. It defaults
to 7,500 and accepts whole numbers from 1,000 to 100,000. Automatic uses
Pebble Health's typical full-day step count, falling back to 7,500 when the
average is unavailable or zero. Settings explain both calculations. The ring
still defaults off, uses the approved geometry/colors, and caps progress at 100%.

AppConfig now appends uint8_t step_goal_mode at offset 34 and uint32_t
custom_step_goal at offset 36 (40 bytes total). The 20-, 27- and 34-byte older
records remain prefixes. Defaults are initialized before reading persisted
settings. Invalid persisted values resolve to Automatic/7,500. Message keys
StepGoalMode (10040) and CustomStepGoal (10041) are appended; SlotType and all
previous keys are unchanged. Missing keys preserve saved values; switching
mode never clears the custom goal.

The settings form uses a numeric field with range, step and required
constraints, plus strict decimal validation. Switching to Automatic discards
an invalid unsaved field edit before hiding it; a valid custom value is kept.
The phone validates before Clay's storage-writing parser, rejects an invalid
save without altering any saved settings, and normalizes the target to an
integer for AppMessage. The watch validates decimal strings and integer
values before applying any settings in a malformed goal packet. It rejects
fractions, signs, junk suffixes, invalid types and out-of-range values. A
zero/invalid stored denominator falls back safely. The largest full settings
dictionary is **367 bytes**, leaving 145 bytes in the unchanged 512-byte inbox
(and 113 bytes below the PRD's 480-byte limit).

New evidence: `dist/verification/1.3.0/custom-goal-final/`. Ten host suites
cover migration, save/load, mode changes, missing keys, malformed values,
automatic fallback, goal boundaries and rectangular/round progress geometry.
Actual Clay integration tests verify validation occurs before storage changes;
mock Clay tests verify capability filtering and live Custom-field visibility
on all seven platforms, including monochrome Health watches. All seven targets
build cleanly apart from the seven existing SDK linker RWX notices.

The earlier `custom-goal/` experiment is superseded: its parser produced an SDK
zero-length-array warning. The final parser uses bounded memchr validation;
`custom-goal-final/` is the candidate for all subsequent checks.

### Custom-goal candidate evidence

- PBW: `dist/verification/1.3.0/custom-goal-final/thin-plus.pbw`, 600,042 bytes.
  SHA-256: `b25a9fdbe9b55c30ed6fd1dc1df62c0412ea844976e0d8035033303513f656a7`.
  `build/thin-plus.pbw` contains these same tested bytes. `validation.json`
  records source hashes, the complete input snapshot and package validation.
- `emery-custom-10000-half.png` and `gabbro-custom-10000-half.png` show real
  settings selecting Custom = 10,000 and 5,000 injected steps, with no getter
  overrides. Each platform also has `custom-10000-at-target.png` (10,000
  steps) and `custom-10000-above-target.png` (15,000 steps). The ring pixels
  match at and above the target. Native SDK screenshots use its normal display
  correction; the captures have not been resized or composited.
- `emery-custom-goal-result.json` and `gabbro-custom-goal-result.json` record
  mode-switch restoration and whole-packet rejection of an invalid custom
  value, with identical face pixels before and after. Gabbro also proves a
  real close/open saves and reloads the target and mode. Ring-off is captured
  on Gabbro. The single-connection harness is `tests/verify_custom_goal.py`.
- The Emery App BlobDB filled during a repeat installation, after the final
  PBW had successfully installed and completed its goal captures. Its successful
  original screenshots were retained. Subsequent Ping-screen captures are
  quarantined in `attempt3-launch-failure/` and excluded from verification.
  `install-diagnostic.log` identifies `BlobStatus.DatabaseFull`. No emulator
  state was wiped. Emery reopening remains unverified for this final binary;
  host persistence, Gabbro reopening and the owner-confirmed PT2 check cover that area.
- `dist/verification/1.3.0/final-custom-goal-smoke/smoke-review.json` records
  inspected native rendering and crash-free app logs on all seven platforms.
  Emery/Gabbro use the goal checks above; the other five have smoke screenshots.
  Basalt/Diorite needed startup retries. Chalk's simulated-phone WebSocket
  repeatedly failed, so its final install/log/screenshot check uses the SDK's
  direct QEMU transport, without simulated phone JS. The native Chalk check
  passed. A Ping overlay capture is retained as rejected evidence. The actual
  bundle passed the separate V8 probe and phone/Clay host tests. An orphaned
  Diorite QEMU left by a timed-out startup was stopped by its task-owned PID;
  emulator state was preserved throughout.
- `pt2-install.log` records successful installation of the exact candidate via
  `pebble install --cloudpebble build/thin-plus.pbw`. Installation alone is not
  owner confirmation. The owner subsequently confirmed the updated checks below;
  see `release-prep-custom-goal/owner-confirmation.json` for the exact reply and scope.

## Approved design

The owner approved the weather text and optional step ring shown in
`dist/verification/1.3.0/design-options/design-review.png`:

- Weather is a rounded temperature with a degree sign, in the selected slot.
  It stays blank when unavailable or more than three hours old.
- The ring follows the rectangle on PT2 and a circle on round watches. It is
  two pixels wide, inside the hour markers, under the hands and outside the
  date column. It starts at twelve o'clock and fills clockwise.
- The comparison shows 3,750 and 7,500 simulated steps against a controlled
  7,500 goal, plus simulated 18°C weather. Teal is a demonstration color;
  the ring has a color setting and a value in each theme. It defaults off.

These are native emulator captures, enlarged by nearest-neighbor scaling.
The design fixture overrides the goal only in its isolated scratch build;
the production source and candidate have no overrides. Actual emulator
history changes its computed typical goal when step totals are injected,
so a controlled goal makes the two percentages comparable. The fixture PBW
must not be installed as a release.

## Implementation

R11 adds a Date style select: Full (default, existing layout), Day only
(numeral centered vertically at three o'clock), and Weekday and day (the
existing weekday/day positions, without the month). The select is shown only
when Show current date is on; hiding it does not reset the saved style. This
logic also runs on monochrome pages without a Theme control. Full restores
the original day frame after switching away from Day only.

The owner approved the six native previews in
`dist/verification/1.3.0/r11-centered/date-style-review.png`.

R6 appends Distance (5), Active calories (6), ISO week (7), Second time zone
(8) and Weather (9). Distance uses the watch's km/mi preference with one
decimal. Health changes redraw the slots and ring; daily totals refresh at
midnight. ISO weeks are computed without relying on SDK support for `%V`.
The second time zone follows the existing digital slot's 12/24-hour style.

The phone computes named IANA offsets with `Intl.DateTimeFormat`, including
DST, when supported. Common zones and a custom IANA input are available.
It refreshes offsets on settings save and every 30-minute refresh while the
slot is selected. Unsupported runtimes get UTC-12 through UTC+14 at 15-minute
increments, with an explicit manual-DST description. An invalid or unknown
offset leaves the slot blank.

The installed emulator's STPyV8 crashes natively inside ICU on named-zone
formatting; a JavaScript try/catch cannot recover. The `pypkjs` platform
therefore bypasses Intl and selects the fixed-offset fallback. Node tests
verify named-zone winter/summer offsets, but the actual mobile runtime
still needs the PT2 check below.

R7 uses [Open-Meteo's current-weather API](https://open-meteo.com/en/docs).
Settings link to Open-Meteo for attribution. GPS is requested only with a
Weather slot selected. The watch requests data at launch when stale and
on minute ticks after 30 minutes, avoiding background phone timer dependence.
Successful weather is stored under persist key 51, separate from AppConfig.
The cache includes units so a delayed Celsius response cannot be shown as
Fahrenheit. A unit change hides old data until a matching response arrives.

The phone validates responses and keeps the last good value on location,
network, HTTP or timeout errors. Cached coordinates younger than 24 hours
can cover transient location failures; explicit permission denial does not
use them. Changing settings cancels obsolete requests and late callbacks.
Manual request timers accommodate the phone-runtime limitations described
in the [PebbleKit JS guide](https://developer.repebble.com/guides/communication/using-pebblekit-js/).

R8 defaults to today's typical full-day step total from the Health API, falling
back to 7,500 when no average is available or it is zero. Custom overrides the
target with the saved daily goal, as described above. Progress is capped at 100% and
hidden when health is unavailable. The setting appears only on health
platforms. Existing Quick View handling continues to hide the bottom slot.

## Saved-settings compatibility

- The 27-byte 1.2.0 AppConfig prefix is unchanged. New ring, units and offset
  fields are appended and initialized before reading saved data.
- The new ring color uses GColorClear and the existing marker-color fallback.
- All original SlotType values and message-key IDs are retained. New keys
  are appended. Missing settings still preserve saved values.
- New complications require selection; the ring defaults off. The owner's
  animation-off default remains unchanged.
- Actual Clay integration tests cover partial saves and phone-only zone keys.
  Maximum settings dictionary including DateStyle and custom goal: 367 bytes on emery, below the 480-byte budget
  and 512-byte inbox. Maximum refresh request: 34 bytes in the 64-byte outbox.
- R11 appends a uint8_t date_style and the DateStyle message key. Full is set
  before reading saved config, and messages apply it only if present. Invalid
  values are rejected; an invalid stored value renders Full.

## Verified in the emulator and on the host

All paths below are relative to this watchface directory and ignored by Git.

- `dist/verification/1.3.0/final-approved/`: previously approved production package,
  source snapshot, clean build and validation, and successful install/rendering
  smoke checks on all seven platforms. Each run observed runtime logs for at
  least 20 seconds and saved an inspected native screenshot. `smoke-review.json`
  records no app crashes and counts known phone-simulator footer warnings
  separately. Chalk and Gabbro required emulator restarts after connection
  failures before installation; both retries passed without wiping state.
  The PBW matches the approved `r11-centered` bytes and the upgrade-tested
  package: SHA-256 `c3bcb1ccc10d00f9cb26cd41107f0f514adcf03210c0080f0b0bd031dd8d7cae`.
  Its source snapshot records the inputs of that earlier candidate. The custom
  goal candidate supersedes these bytes; its fresh PT2 check is now owner-confirmed.
  `pt2-install.log` records `pebble install --cloudpebble build/thin-plus.pbw`
  completing with "App install succeeded." Installation success does not mark
  the owner's real-location, permission, timezone or interaction checks as done.

- `dist/verification/1.3.0/r11-centered/`: earlier 1.3.0 package, clean build for
  all seven platforms and validation/source hashes. This supersedes `final/`,
  which was built before R11. Native emery and gabbro screenshots cover Full,
  Day only, Weekday and day, date hidden, and Full restored. The restored Full
  screenshot matches the initial Full screenshot pixel for pixel.
  `layout-validation.json` confirms that only the date region changes and
  Day only's visible numeral is exactly centered vertically on both screens.
  `r11-design/` holds the earlier placement; `r11-centered/` remains the approved date design evidence.
- `dist/verification/1.3.0/r11-host/`: all ten suites passed after R11,
  including legacy Full defaults, persisted style, missing-key preservation,
  explicit zero/string values and rejected out-of-range values. Mock Clay
  verifies initial and live visibility plus retained selection on all seven
  platforms, including monochrome watches.
- `dist/verification/1.3.0/upgrade-r11-centered/result.json`: the current R11
  package installs over published 1.2.0 with identical saved-face pixels and
  unchanged message-key IDs. Native emery/gabbro logs contain no app crashes.

- `dist/verification/1.3.0/design-gate/`: emery, gabbro and flint installs,
  AppMessage settings, new complications, negative/Celsius/Fahrenheit weather,
  second time, week number, ring on/off and runtime/command logs.
- `dist/verification/1.3.0/design-gate/flint-left-*.png`: `10.5`, `1234`,
  `W43` and `12:59` fit the left slot at native 144×168 resolution.
- `dist/verification/1.3.0/design-options/`: emery and gabbro native design
  captures at 50% and 100%; `build-context.json` identifies the simulated goal.
- `dist/verification/1.3.0/upgrade-candidate/result.json`: installed the real
  published 1.2.0 PBW, saved custom settings, then installed the production
  development candidate without wiping. Before/after pixels are identical
  at the same clock time; original message-key IDs are unchanged.
- `dist/verification/1.3.0/candidate/build.log` and `validation.json`: clean
  build and ZIP validation for all seven platforms, production source hashes,
  no TEMP_TEST overrides. No compiler warnings; the seven existing SDK linker
  RWX warnings remain. Aplite: 19,204 resource bytes and 9,912 free heap bytes.
- `dist/verification/1.3.0/host/`: all ten host/Clay checks pass, including
  persistence, missing keys, C/F and expiry, GPS denial/timeouts, cancellation,
  DST and fixed offsets, health units/midnight, and rectangular/round geometry.
- `dist/verification/1.3.0/host/runtime-probe.json`: actual bundled JavaScript
  runs in the installed emulator V8, using simulated GPS, HTTP and AppMessage
  APIs. It verifies the ready handshake, weather response and fixed-zone mode.
- `dist/verification/1.3.0/open-meteo-check.json`: a live API request using
  public Tokyo coordinates returned HTTP 200. This is not the owner's GPS.

Weather design screenshots use injected readings. The `weather-unit-change`
capture can already contain a fresh network response; it is not evidence of
the intermediate blank state. Unit-mismatch blanking is verified by host tests.
Phone-simulator footer-decoding errors occur in CLI logs; they are not treated
as successful end-to-end phone GPS verification.

The earlier all-seven-platform emulator smoke pass is recorded in `final-approved/`.
The earlier pre-R11 `final/` run is superseded and is not release evidence.
GitHub Actions includes the new tests but has not run remotely without a push.

## Verified by the owner on PT2

- The owner approved the full 1.2.0 sideload checklist before publication.
- The owner confirmed the earlier R11 1.3.0 candidate checklist before invoking
  the release skill. That covers the previously sideloaded version, not the new
  custom-goal controls. The exact phone timezone mode was not reported.
- The owner confirmed the updated custom-goal checks: saved face unchanged,
  Custom = 10,000, mode switching and reopening preserve 10,000, blank/999/
  100,001/decimals are rejected, and ring-off preserves the target. The owner
  also approved the Emery/Gabbro custom-goal previews. Boundary values and
  automatic fallback are covered by host tests; no separate PT2 observations
  were reported for those cases.

## Updated PT2 checklist and remaining release gate

Checklist supplied for the updated candidate (confirmation scope recorded above):

1. The saved face and settings stay unchanged after updating; Goal initially
   shows Automatic and the ring retains its previous on/off choice.
2. Enable the ring, choose Custom, and save Daily step goal = 10,000. The ring
   should match today's steps divided by 10,000, capped at a full ring.
3. Switch to Automatic, save, reopen settings, then return to Custom: 10,000
   is still there. Reopen the watchface and confirm it remains in use.
4. Try blank, 999, 100,001 and a decimal: Save must be blocked and the last
   valid saved goal must remain intact. 1,000 and 100,000 are valid boundaries.
5. Confirm the Custom field appears only in Custom mode, and turning the ring
   off hides the ring without losing the target. Restore your preferred goal.

New goal screenshots and physical checks are owner-approved. The same tested
bytes are frozen in `dist/releases/1.3.0/` and now published with explicit owner
approval. The owner subsequently confirmed installation from the store, opening
settings and applying a theme, and authorized adding the GitHub release tags.

## Previously confirmed PT2 checklist (earlier candidate)

1. Before changing settings, confirm the saved face, colors and slots look
   unchanged and the opening-animation choice is preserved.
2. Try Full, Day only and Weekday and day. Turn Show current date off: the
   date and style select should disappear. Turn it back on: the chosen style
   should return.
3. Try Distance, Active calories and Week number in the slots, including Left.
   Distance should follow the watch's km/mi preference and show one decimal.
4. Select Second time zone, choose a zone and compare it with a trusted clock.
   Check 12/24-hour formatting. Report whether the phone offers named zones
   (automatic DST) or the fixed UTC-offset fallback (manual DST adjustment).
5. Select Weather and allow phone location. Check a real reading, then switch
   Celsius/Fahrenheit. Confirm it updates again after about 30 minutes.
6. Test denied location permission: no crash; the last good weather can remain
   for up to three hours, or the slot stays blank without cached weather.
   Restore permission and save settings to request fresh weather. Remove all
   Weather slots and confirm Thin+ no longer requests location.
7. The step ring should initially be off. Enable it, try themes or set a color
   under Custom, and check progress/readability. Its goal is today's typical
   total, with 7,500 as fallback when history is unavailable.

Only after the owner confirms these PT2 checks, prepare release text and
artifacts with the thin-plus-release skill. Store upload/publication and Git
actions remain separate explicit approvals.

The 1.2.0 store-install/settings/theme check is still distinct from its approved
sideload checklist; starting 1.3.0 does not mark that store check as passed.
