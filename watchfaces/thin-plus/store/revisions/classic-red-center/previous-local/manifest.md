# Thin+ 1.0.0 — Gate A manifest

Prepared 2026-10-19. Status: Gate A approved by Edward ("I approve all").
Approval scope and asset hashes: `evidence/gate-a-approval.json`.
Edward subsequently authorized API creation/upload and release publication.
Thin+ 1.0.0 is published and publicly listed. Edward confirmed the Gate B PT2
test and explicitly authorized Gate C. No additional commit, push or tag was
performed. Evidence: `evidence/release-publication.json` and
`evidence/listed-publication.json`.
Store IDs, asset checks and dashboard link: `evidence/store-verification.json`.

## Release candidate

- PBW: `../build/thin-plus.pbw` (kept outside `store/`; not committed).
- Size: **519,559 bytes**.
- SHA-256: `b5fe248bf60447b144b71ee5078db23933780916a865271d3a924967e1cae517`.
- Base source commit: `56012e58e2e6f7fe6aea894c352ad45c451ef85f` (`watchface/thin-plus`).
- The final candidate adds the **approved, uncommitted menu icon** to that
  commit. `evidence/release-source.patch` reconstructs that binary-input change;
  `evidence/build-inputs.sha256` identifies the exact source/resource inputs.
  This is not yet a fully committed release snapshot; no tag exists from this work.
- UUID: `0e83e240-01b8-469b-a51b-b2a0e767fefb` (unchanged).
- Embedded `displayName`: `Thin+`; `versionLabel`: `1.0.0`; watchface: `true`.
- Platforms: aplite, basalt, chalk, diorite, emery, flint, gabbro; all seven binaries present.
- ZIP integrity and embedded metadata: passed (`evidence/final-validation.json`).
- Toolchain: Pebble Tool 5.0.40 / SDK 4.33.1.
- Clean build: seven known RWX linker notices; no other compiler warnings.
- Aplite: 10,883 / 24,576 RAM bytes; 13,693 bytes linker-estimated heap headroom;
  resources 19,204 / 131,072 bytes. Runtime heap was not measured.

Do not rebuild just to upload: use this exact approved PBW. A changed source
input requires a new candidate hash and the applicable validation.

## Verification and limits

- Emulator: initial seven-platform smoke test and final-candidate seven-platform
  smoke test. Successful installs, visually inspected default renders, and no
  crash messages during the final 26-second log command windows. See
  `evidence/verification.md` and `evidence/final-smoke/`.
- PT2: Edward confirmed the two new color controls and complete settings save
  with the 512-byte inbox before commit. After release publication he confirmed
  the PT2 store-install/settings/theme check (Gate B). Physical checks are
  owner-reported, not independently observed by the agent.
- Screenshot variants came from scratch builds with temporary getter overrides;
  they are not uploadable release binaries. All scratch data files were restored,
  and production `src/` contains zero `TEMP_TEST` markers.
- Gate A is approved. Authorized unlisted listing creation and draft release
  upload are complete. The downloaded PBW hash matches exactly; native screenshot
  dimensions/order and banner were visually verified after server PNG optimization.
  Edward's shorter credit is applied to all descriptions and release notes.
- Release 1.0.0 is published after Edward's explicit approval. An unauthenticated
  public PBW download matches the approved SHA-256 exactly.
  Gate B is complete based on Edward's PT2 confirmation. Gate C is complete
  after his explicit go-ahead; the dashboard and public API both report listed
  visibility, and the public release download still matches the approved PBW.
- Asset/docs changes remain uncommitted; commit/push/tag need later authorization.
  README includes the verified store link.

## Asset requirements and selection

Edward supplied these current New App form requirements: small icon 80×80, large
icon 144×144; exact native screenshot sizes; maximum five screenshots per platform;
720×320 optional per-platform banner; maximum 4.4 MB per screenshot/banner.
The New App form omits watchface icon uploads, but the Edit form supports them.
The rectangular 80×80 and 144×144 store icons were saved through the edit endpoint and
verified in the dashboard list. App type remains Watchface.

- Upload screenshots: `screenshots/`, native PNGs. Emery: 200×228;
  gabbro: 260×260; chalk: 180×180; other platforms: 144×168.
- Emery recommended order: 01 Classic minimal, 02 Neon date only,
  03 Ocean medium, 04 Paper rich, 05 Sunset rich with thick hands/40%.
  All other platforms have Classic minimal, medium and rich images.
  The 23-image selection and provenance are in `screenshot-selection.json`. Superseded images remain in
  `evidence/previous-screenshots/` for the original approval audit.
- Banner: `banner-emery-720x320.png`, for the Emery platform tab. Updated with the
  minimal Classic face and "The Thin you love. More ways to make it yours."
- Store icons: `icons/thin-plus-80.png` and `icons/thin-plus-144.png`.
- In-app icon: `../resources/images/menu_icon.png`, 25×25, also copied to
  `icons/menu-icon-25.png`. Original geometric art; does not reuse Thin's icon.
  The store icons use a rectangular PT2-style outline; the embedded menu icon
  stays identical to the validated release candidate.
- `preview-*.png` are review sheets, not store uploads. `listing.md` contains the
  current listing/release-note text, credit, source link and later dashboard steps.
- The mixed gallery and rectangular store icons were requested by Edward after
  Gate A. Native capture configurations are recorded in
  `evidence/minimal-screenshot-provenance.json`,
  `evidence/medium-screenshot-provenance.json`, and
  `evidence/screenshot-provenance.json`.
- README screenshots are byte-identical copies of the corresponding files here.

## File inventory

All files under `store/` are listed below, including this manifest. Sizes are bytes.
The PBW is listed separately above. PNG dimensions are recorded without rescaling.

| File | Bytes | PNG dimensions |
| --- | ---: | --- |
| `banner-emery-720x320.png` | 8873 | 720×320 |
| `evidence/aplite-capture.log` | 294 |  |
| `evidence/aplite-default.png` | 1068 | 144×168 |
| `evidence/aplite-install.log` | 41 |  |
| `evidence/aplite-kill.log` | 0 |  |
| `evidence/aplite-runtime.log` | 0 |  |
| `evidence/banner-credit-audit.json` | 3264 |  |
| `evidence/basalt-capture.log` | 294 |  |
| `evidence/basalt-default.png` | 1298 | 144×168 |
| `evidence/basalt-install.log` | 41 |  |
| `evidence/basalt-kill.log` | 0 |  |
| `evidence/basalt-runtime.log` | 0 |  |
| `evidence/build-inputs.sha256` | 1936 |  |
| `evidence/capture-aplite-classic-medium.log` | 2994 |  |
| `evidence/capture-aplite-classic-minimal.log` | 3000 |  |
| `evidence/capture-aplite-classic.log` | 3087 |  |
| `evidence/capture-basalt-classic-medium.log` | 2994 |  |
| `evidence/capture-basalt-classic-minimal.log` | 3000 |  |
| `evidence/capture-basalt-classic.log` | 3134 |  |
| `evidence/capture-chalk-classic-medium.log` | 2990 |  |
| `evidence/capture-chalk-classic-minimal.log` | 2996 |  |
| `evidence/capture-chalk-classic.log` | 3130 |  |
| `evidence/capture-diorite-classic-medium.log` | 2998 |  |
| `evidence/capture-diorite-classic-minimal.log` | 3004 |  |
| `evidence/capture-diorite-classic.log` | 3144 |  |
| `evidence/capture-emery-01-classic-minimal.log` | 28036 |  |
| `evidence/capture-emery-01-classic.log` | 28170 |  |
| `evidence/capture-emery-02-neon-date-only.log` | 13548 |  |
| `evidence/capture-emery-02-neon.log` | 9453 |  |
| `evidence/capture-emery-03-ocean-medium.log` | 28053 |  |
| `evidence/capture-emery-03-ocean-steps-only.log` | 13643 |  |
| `evidence/capture-emery-03-ocean.log` | 9455 |  |
| `evidence/capture-emery-04-paper-digital-only.log` | 13636 |  |
| `evidence/capture-emery-04-paper.log` | 9775 |  |
| `evidence/capture-emery-05-sunset-battery-only.log` | 13739 |  |
| `evidence/capture-emery-05-sunset.log` | 64444 |  |
| `evidence/capture-emery-06-sunset-thick-40.log` | 13700 |  |
| `evidence/capture-flint-classic-medium.log` | 2990 |  |
| `evidence/capture-flint-classic-minimal.log` | 2996 |  |
| `evidence/capture-flint-classic.log` | 3127 |  |
| `evidence/capture-gabbro-classic-medium.log` | 13630 |  |
| `evidence/capture-gabbro-classic-minimal.log` | 13650 |  |
| `evidence/capture-gabbro-classic.log` | 13867 |  |
| `evidence/chalk-capture.log` | 373 |  |
| `evidence/chalk-default.png` | 1851 | 180×180 |
| `evidence/chalk-install.log` | 41 |  |
| `evidence/chalk-kill.log` | 0 |  |
| `evidence/chalk-runtime.log` | 0 |  |
| `evidence/diorite-capture.log` | 295 |  |
| `evidence/diorite-default.png` | 1095 | 144×168 |
| `evidence/diorite-install.log` | 41 |  |
| `evidence/diorite-kill.log` | 0 |  |
| `evidence/diorite-runtime.log` | 0 |  |
| `evidence/downloaded-platforms-review.png` | 43755 | 900×1860 |
| `evidence/downloaded-store-review.png` | 16015 | 900×620 |
| `evidence/emery-capture.log` | 373 |  |
| `evidence/emery-default.png` | 1801 | 200×228 |
| `evidence/emery-install.log` | 41 |  |
| `evidence/emery-kill.log` | 0 |  |
| `evidence/emery-runtime.log` | 0 |  |
| `evidence/final-clean-build.log` | 27596 |  |
| `evidence/final-clean.log` | 43 |  |
| `evidence/final-smoke/aplite-capture.log` | 306 |  |
| `evidence/final-smoke/aplite-default.png` | 1144 | 144×168 |
| `evidence/final-smoke/aplite-install.log` | 41 |  |
| `evidence/final-smoke/aplite-kill.log` | 0 |  |
| `evidence/final-smoke/aplite-observation.txt` | 106 |  |
| `evidence/final-smoke/aplite-runtime.log` | 0 |  |
| `evidence/final-smoke/basalt-capture.log` | 306 |  |
| `evidence/final-smoke/basalt-default.png` | 1385 | 144×168 |
| `evidence/final-smoke/basalt-install.log` | 41 |  |
| `evidence/final-smoke/basalt-kill.log` | 0 |  |
| `evidence/final-smoke/basalt-observation.txt` | 106 |  |
| `evidence/final-smoke/basalt-runtime.log` | 0 |  |
| `evidence/final-smoke/chalk-capture.log` | 385 |  |
| `evidence/final-smoke/chalk-default.png` | 1988 | 180×180 |
| `evidence/final-smoke/chalk-install.log` | 41 |  |
| `evidence/final-smoke/chalk-kill.log` | 0 |  |
| `evidence/final-smoke/chalk-observation.txt` | 106 |  |
| `evidence/final-smoke/chalk-runtime.log` | 0 |  |
| `evidence/final-smoke/cleanup.log` | 0 |  |
| `evidence/final-smoke/diorite-capture.log` | 307 |  |
| `evidence/final-smoke/diorite-default.png` | 1198 | 144×168 |
| `evidence/final-smoke/diorite-install.log` | 41 |  |
| `evidence/final-smoke/diorite-kill.log` | 0 |  |
| `evidence/final-smoke/diorite-observation.txt` | 106 |  |
| `evidence/final-smoke/diorite-runtime.log` | 0 |  |
| `evidence/final-smoke/emery-capture.log` | 385 |  |
| `evidence/final-smoke/emery-default.png` | 2110 | 200×228 |
| `evidence/final-smoke/emery-install.log` | 41 |  |
| `evidence/final-smoke/emery-kill.log` | 0 |  |
| `evidence/final-smoke/emery-observation.txt` | 106 |  |
| `evidence/final-smoke/emery-runtime.log` | 0 |  |
| `evidence/final-smoke/flint-capture.log` | 305 |  |
| `evidence/final-smoke/flint-default.png` | 1229 | 144×168 |
| `evidence/final-smoke/flint-install.log` | 41 |  |
| `evidence/final-smoke/flint-kill.log` | 0 |  |
| `evidence/final-smoke/flint-observation.txt` | 106 |  |
| `evidence/final-smoke/flint-runtime.log` | 0 |  |
| `evidence/final-smoke/gabbro-capture.log` | 466 |  |
| `evidence/final-smoke/gabbro-default.png` | 3149 | 260×260 |
| `evidence/final-smoke/gabbro-install.log` | 41 |  |
| `evidence/final-smoke/gabbro-kill.log` | 0 |  |
| `evidence/final-smoke/gabbro-observation.txt` | 106 |  |
| `evidence/final-smoke/gabbro-runtime.log` | 0 |  |
| `evidence/final-smoke/results.json` | 2346 |  |
| `evidence/final-validation.json` | 2811 |  |
| `evidence/flint-capture.log` | 293 |  |
| `evidence/flint-default.png` | 1091 | 144×168 |
| `evidence/flint-install.log` | 41 |  |
| `evidence/flint-kill.log` | 0 |  |
| `evidence/flint-runtime.log` | 0 |  |
| `evidence/gabbro-capture.log` | 454 |  |
| `evidence/gabbro-default.png` | 2935 | 260×260 |
| `evidence/gabbro-install.log` | 41 |  |
| `evidence/gabbro-kill.log` | 0 |  |
| `evidence/gabbro-runtime.log` | 0 |  |
| `evidence/gallery-icon-update.json` | 3026 |  |
| `evidence/gate-a-approval.json` | 6320 |  |
| `evidence/listed-publication.json` | 822 |  |
| `evidence/medium-screenshot-provenance.json` | 3918 |  |
| `evidence/minimal-screenshot-provenance.json` | 6057 |  |
| `evidence/pre-smoke-build.log` | 2385 |  |
| `evidence/previous-icons/thin-plus-144.png` | 9227 | 144×144 |
| `evidence/previous-icons/thin-plus-80.png` | 4764 | 80×80 |
| `evidence/previous-screenshots/aplite-classic.png` | 1485 | 144×168 |
| `evidence/previous-screenshots/banner-emery-720x320.png` | 8151 | 720×320 |
| `evidence/previous-screenshots/basalt-classic.png` | 1759 | 144×168 |
| `evidence/previous-screenshots/chalk-classic.png` | 2389 | 180×180 |
| `evidence/previous-screenshots/diorite-classic.png` | 1480 | 144×168 |
| `evidence/previous-screenshots/emery-01-classic.png` | 2502 | 200×228 |
| `evidence/previous-screenshots/emery-02-neon.png` | 2800 | 200×228 |
| `evidence/previous-screenshots/emery-03-ocean.png` | 2576 | 200×228 |
| `evidence/previous-screenshots/emery-04-paper.png` | 2485 | 200×228 |
| `evidence/previous-screenshots/emery-05-sunset.png` | 2616 | 200×228 |
| `evidence/previous-screenshots/emery-06-sunset-thick-40.png` | 2562 | 200×228 |
| `evidence/previous-screenshots/flint-classic.png` | 1587 | 144×168 |
| `evidence/previous-screenshots/gabbro-classic.png` | 4074 | 260×260 |
| `evidence/previous-screenshots/minimal-only/emery-03-ocean-steps-only.png` | 1950 | 200×228 |
| `evidence/previous-screenshots/minimal-only/emery-04-paper-digital-only.png` | 1596 | 200×228 |
| `evidence/previous-screenshots/minimal-only/emery-05-sunset-battery-only.png` | 1868 | 200×228 |
| `evidence/r1-clean-build.log` | 27596 |  |
| `evidence/r1-clean.log` | 43 |  |
| `evidence/r1-validation.json` | 2489 |  |
| `evidence/release-publication.json` | 1020 |  |
| `evidence/release-source.patch` | 859 |  |
| `evidence/screenshot-provenance.json` | 5238 |  |
| `evidence/smoke-candidate.json` | 173 |  |
| `evidence/smoke-cleanup.log` | 0 |  |
| `evidence/store-create-plan.json` | 5385 |  |
| `evidence/store-create-result.json` | 808 |  |
| `evidence/store-credit-update.json` | 433 |  |
| `evidence/store-icon-update.json` | 1233 |  |
| `evidence/store-minimal-update.json` | 1528 |  |
| `evidence/store-verification-before-gallery-icons.json` | 11009 |  |
| `evidence/store-verification-before-minimal.json` | 14366 |  |
| `evidence/store-verification.json` | 21254 |  |
| `evidence/verification.md` | 7510 |  |
| `icons/menu-icon-25.png` | 196 | 25×25 |
| `icons/thin-plus-144.png` | 4260 | 144×144 |
| `icons/thin-plus-80.png` | 2776 | 80×80 |
| `icons/thin-plus.svg` | 474 |  |
| `listing.md` | 6041 |  |
| `manifest.md` | 16532 |  |
| `preview-emery.png` | 24386 | 900×695 |
| `preview-platforms.png` | 54462 | 900×1955 |
| `screenshot-selection.json` | 16684 |  |
| `screenshots/aplite-classic-medium.png` | 1248 | 144×168 |
| `screenshots/aplite-classic-minimal.png` | 911 | 144×168 |
| `screenshots/aplite-classic-rich.png` | 1485 | 144×168 |
| `screenshots/basalt-classic-medium.png` | 1403 | 144×168 |
| `screenshots/basalt-classic-minimal.png` | 1094 | 144×168 |
| `screenshots/basalt-classic-rich.png` | 1759 | 144×168 |
| `screenshots/chalk-classic-medium.png` | 2019 | 180×180 |
| `screenshots/chalk-classic-minimal.png` | 1697 | 180×180 |
| `screenshots/chalk-classic-rich.png` | 2389 | 180×180 |
| `screenshots/diorite-classic-medium.png` | 1248 | 144×168 |
| `screenshots/diorite-classic-minimal.png` | 911 | 144×168 |
| `screenshots/diorite-classic-rich.png` | 1480 | 144×168 |
| `screenshots/emery-01-classic-minimal.png` | 1628 | 200×228 |
| `screenshots/emery-02-neon-date-only.png` | 1945 | 200×228 |
| `screenshots/emery-03-ocean-medium.png` | 2146 | 200×228 |
| `screenshots/emery-04-paper-rich.png` | 2485 | 200×228 |
| `screenshots/emery-05-sunset-rich.png` | 2562 | 200×228 |
| `screenshots/flint-classic-medium.png` | 1248 | 144×168 |
| `screenshots/flint-classic-minimal.png` | 911 | 144×168 |
| `screenshots/flint-classic-rich.png` | 1587 | 144×168 |
| `screenshots/gabbro-classic-medium.png` | 3212 | 260×260 |
| `screenshots/gabbro-classic-minimal.png` | 2622 | 260×260 |
| `screenshots/gabbro-classic-rich.png` | 4074 | 260×260 |
| `tools/capture-screenshots.py` | 5741 |  |
| `tools/draw-banner.py` | 1069 |  |
| `tools/draw-icons.py` | 1548 |  |
| `tools/make-previews.py` | 1438 |  |
| `tools/select-screenshots.py` | 2932 |  |
| `tools/smoke-test.sh` | 1201 |  |
| `tools/write-manifest.py` | 7210 |  |
