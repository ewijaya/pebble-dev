# Thin+ 1.0.0 verification

## Physical Pebble Time 2

Edward confirmed in this session on 2026-10-19: the seconds-hand tip color,
empty-battery-marker color and full settings save with the 512-byte inbox
all work on his PT2. Those six source/config files were committed separately
as `56012e58e2e6f7fe6aea894c352ad45c451ef85f`.

This is owner-reported physical testing of the color changes, not a claim
that the agent observed the physical watch. After publication, Edward confirmed
the Gate B store-install/settings/theme check. That later confirmation is
recorded in `listed-publication.json`; the agent did not perform a physical install.

## Initial emulator smoke test (R1)

Platforms: aplite, basalt, chalk, diorite, emery, flint, gabbro.
Each installed successfully, was observed using `pebble logs` with a 23-second
command window, and rendered its default face in a captured PNG. All seven
captures were visually inspected. No crash messages appeared. The runtime
logs are empty because the app emitted no messages during those windows;
installation success and screenshot output are retained separately.

`pebble kill` was used between platforms. Headless SDL settings were used.
No emulator data wipe was performed. Flint passes the PRD's minimum build,
install and default-render check; the phone's Clay UI was not exercised.

The initial tested bundle is identified by `smoke-candidate.json`.
`r1-clean-build.log` and `r1-validation.json` record the subsequent clean
build and PBW checks before icon replacement.

## Final candidate

The production source retains its normal getters. The only binary input
changed after the confirmed source commit is the new 25×25 menu icon.
`release-source.patch` records that change; `build-inputs.sha256` records
all source/resource inputs and package metadata.

`final-clean-build.log` records a clean build with only seven known linker
RWX notices and no other compiler warnings. Aplite uses 10,883 of 24,576 RAM
bytes, leaving 13,693 bytes of linker-estimated heap headroom. This is not
measured runtime free heap. Its resources use 19,204 of 131,072 bytes.

`final-validation.json` records ZIP integrity, seven platform binaries, UUID,
display name, version, watchface flag, platform list, byte count and SHA-256.
The PBW stays in `build/thin-plus.pbw` and is not copied into `store/`.

Final-bundle runtime check: all seven platforms passed installation, default
rendering (visually inspected), and 26-second `pebble logs` command windows
without crash messages. The log windows emitted no app messages. Start/end
timestamps, successful install output, screenshots and the exact PBW hash are
recorded in `final-smoke/`, including `results.json`.

## Listing screenshots

Native emulator PNGs, unscaled and unedited. Settings were temporarily
hard-coded at the tops of `data_get_color`, `data_get_slot` and
`data_get_enable` in scratch copies; every override line was marked
`// TEMP_TEST`. Production C files were never changed. Scratch data files
were restored after capture. The exact configurations and emulator inputs
are recorded in `screenshot-provenance.json`.

Edward requested an assortment of minimal, medium and rich layouts after reviewing the minimal-only gallery. The final Emery order is Classic minimal, Neon date only, Ocean digital time and steps, Paper with all complications, and Sunset with all complications, thick hands and 40% battery. Each other platform has three Classic screenshots: minimal, medium (digital time and date), and rich (all slots where supported).

The gallery contains 23 native images. `../screenshot-selection.json` records the exact selection, hashes and provenance. Seven new medium captures came from restored scratch builds; their settings and production-source/PBW checks are in `medium-screenshot-provenance.json`. Minimal images are reused from `minimal-screenshot-provenance.json`; rich images are byte-identical copies of the earlier verified captures in `previous-screenshots/`. All selected images were visually inspected.

Captures use the live emulator clock. Step values are emulator inputs; health readings depend on platform support and can show zero in older emulators. Aplite's unsupported health slot is absent. No release source or PBW changed for this gallery revision.

The banner now uses the minimal Classic face at native size and Edward's chosen tagline: "The Thin you love. More ways to make it yours." Its uploaded copy was downloaded and visually inspected. Contact sheets are review aids, not upload assets.

Two capture-runner interruptions were recovered by restoring scratch source
and resuming missing captures. They are not watchface crash evidence.

## Pending and approval gates

- Gate A approved by Edward on 2026-10-19: "I approve all" (icon, screenshot
  selection, banner and listing text). See `gate-a-approval.json`.
- Dashboard icon sizes and exact screenshot/banner sizes were supplied by
  Edward from the New App form code without an upload or submission.
  Watchface icon fields may not be shown; the in-app icon is included regardless.
- Edward subsequently authorized programmatic creation/upload. Thin+ was created
  **unlisted** with release 1.0.0 **unpublished**, and the approved PBW/assets uploaded.
  See `store-verification.json` and `store-create-result.json` for IDs and evidence.
- The downloaded PBW hash matches exactly. Twenty-three screenshots and the banner
  retain native dimensions. The mixed gallery was checked in its new order.
  Server PNG optimization changes a small number of visible colors; the maximum
  per-channel mean visible error is below 0.1 on a 0–255 scale.
- The creation endpoint skipped watchface icon fields. The edit endpoint
  accepted the 80×80 and 144×144 icons. Edward then requested a rectangular
  PT2-style outline; the revised store icons are recorded in `store-verification.json`.
  The separate embedded menu icon remains in the verified PBW.
  The developer account name is Edward and was not changed.
- The shorter credit was verified in the main description, all platform
  descriptions and release notes after Edward requested it.
- All nine dashboard text fields and fresh public API responses for all seven
  platforms contain the exact credit "Based on Thin by Chris Lewis." The exact
  public page URL now includes the full stop too. The mixed screenshot gallery
  and rectangular store icons were downloaded and visually checked; see
  `gallery-icon-update.json`. Banner wording and its native screenshot were
  verified in `banner-credit-audit.json`.

- Edward authorized release publication with "okay relese them". Version 1.0.0
  is now published; the listing remains unlisted. The public API exposes the
  release, and an unauthenticated PBW download has the exact approved hash.
  See `release-publication.json`. Edward then confirmed the PT2 test and
  explicitly authorized listed visibility; see `listed-publication.json`.
  No additional commit, push or tag occurred.
- Gate B: complete based on Edward's confirmation of PT2 installation
  **from the store**, opening settings and applying a theme.
- Gate C: complete after explicit authorization. Dashboard visibility is listed
  and the public API reports visible=true with release 1.0.0. The public PBW
  download still matches the approved SHA-256 exactly.
- The approved asset/docs changes remain uncommitted. Commit, push and
  tag require the applicable later authorization. README now contains the
  verified live store link.
