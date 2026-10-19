# Thin+ 1.1.0 — release manifest

Status: published and publicly listed. The owner explicitly requested a version
bump and release. Physical PT2 verification of 1.1.0 remains pending.

- Release ID: `0e3dc4efd60e460586b8dff5`.
- PBW: `../dist/releases/1.1.0/thin-plus.pbw`, also in `../build/thin-plus.pbw`.
- PBW size: 521,806 bytes.
- PBW SHA-256: `15e75184f8381cc19a94fbbcd192323251a2ae9bd0cf5e1676d64b22c50131fd`.
- Source base: `56012e58e2e6f7fe6aea894c352ad45c451ef85f` plus uncommitted version,
  low-battery feature and menu-icon changes. Exact inputs and binary patch:
  `releases/1.1.0/build-inputs.sha256` and `releases/1.1.0/source.patch`.
- No Git commit, push or tag was made. The source base alone does not reproduce
  this release.
- UUID: `0e83e240-01b8-469b-a51b-b2a0e767fefb`; all seven platforms included.
- Clean build: seven known RWX notices only. Aplite RAM: 11,039 / 24,576 bytes;
  linker-estimated heap: 13,537 bytes. Runtime heap was not measured.
- Host tests with ASan/UBSan: threshold, settings migration, persistence, slot
  independence and non-battery complications passed.
- Final candidate: installs, default-settings renders, 22-second log observation
  and low-battery transitions checked on all seven emulators. Exact 19%/20%
  checks on Emery, Flint and Gabbro; older emulators checked at reported 10%/20%.
- Emery upgrade and saved-option persistence checks passed. Phone settings UI
  and physical PT2 behavior are not established by emulator tests.
- The uploaded draft and unauthenticated public PBW downloads match the frozen
  candidate. All seven public catalogs expose 1.1.0. The canonical page now shows the new
  version and feature description. Public listing remains listed.
- Artwork: existing approved 23-image gallery, rectangular icons and Classic
  banner/first PT2 screenshot with visible seconds hand and dark-red center dot.
- Description adds the optional below-20% display; all public text retains the
  exact credit: Based on Thin by Chris Lewis.
- Evidence: `releases/1.1.0/verification.json` and
  `releases/1.1.0/publication-verification.json`. Release notes:
  `releases/1.1.0/release-notes.txt`.
- Historical 1.0.0 manifest/listing/verification: `releases/1.0.0/`.
  Original PBW: `../dist/releases/1.0.0/thin-plus.pbw`.

## File inventory

PBWs stay outside `store/`. Preview sheets are not upload screenshots.
All files under `store/` are included below. Sizes are bytes.

| File | Bytes | PNG dimensions |
| --- | ---: | --- |
| `banner-emery-720x320.png` | 9012 | 720×320 |
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
| `evidence/store-verification.json` | 595 |  |
| `evidence/verification.md` | 7510 |  |
| `icons/menu-icon-25.png` | 196 | 25×25 |
| `icons/thin-plus-144.png` | 4260 | 144×144 |
| `icons/thin-plus-80.png` | 2776 | 80×80 |
| `icons/thin-plus.svg` | 474 |  |
| `listing.md` | 5579 |  |
| `manifest.md` | 20131 |  |
| `preview-emery.png` | 24573 | 900×695 |
| `preview-platforms.png` | 54462 | 900×1955 |
| `releases/1.0.0/listing.md` | 6041 |  |
| `releases/1.0.0/manifest.md` | 19641 |  |
| `releases/1.0.0/store-verification.json` | 21765 |  |
| `releases/1.1.0/aplite-10-visible.png` | 1291 | 144×168 |
| `releases/1.1.0/aplite-20-hidden-again.png` | 939 | 144×168 |
| `releases/1.1.0/aplite-20-hidden.png` | 939 | 144×168 |
| `releases/1.1.0/aplite-commands.log` | 3104 |  |
| `releases/1.1.0/aplite-defaults.png` | 1101 | 144×168 |
| `releases/1.1.0/aplite-runtime.log` | 0 |  |
| `releases/1.1.0/basalt-10-visible.png` | 1463 | 144×168 |
| `releases/1.1.0/basalt-20-hidden-again.png` | 1084 | 144×168 |
| `releases/1.1.0/basalt-20-hidden.png` | 1084 | 144×168 |
| `releases/1.1.0/basalt-commands.log` | 3104 |  |
| `releases/1.1.0/basalt-defaults.png` | 1289 | 144×168 |
| `releases/1.1.0/basalt-runtime.log` | 0 |  |
| `releases/1.1.0/build-context.json` | 357 |  |
| `releases/1.1.0/build-inputs.sha256` | 1936 |  |
| `releases/1.1.0/build.log` | 27326 |  |
| `releases/1.1.0/canonical-page.html` | 46026 |  |
| `releases/1.1.0/chalk-10-visible.png` | 2053 | 180×180 |
| `releases/1.1.0/chalk-20-hidden-again.png` | 1656 | 180×180 |
| `releases/1.1.0/chalk-20-hidden.png` | 1656 | 180×180 |
| `releases/1.1.0/chalk-commands.log` | 3086 |  |
| `releases/1.1.0/chalk-defaults.png` | 1908 | 180×180 |
| `releases/1.1.0/chalk-runtime.log` | 0 |  |
| `releases/1.1.0/cleanup-commands.log` | 44 |  |
| `releases/1.1.0/dashboard-after.json` | 18692 |  |
| `releases/1.1.0/dashboard-before.json` | 15943 |  |
| `releases/1.1.0/dashboard-draft.json` | 17204 |  |
| `releases/1.1.0/dashboard-published.json` | 17244 |  |
| `releases/1.1.0/description-attempt.json` | 25 |  |
| `releases/1.1.0/description.txt` | 1338 |  |
| `releases/1.1.0/diorite-10-visible.png` | 1268 | 144×168 |
| `releases/1.1.0/diorite-20-hidden-again.png` | 909 | 144×168 |
| `releases/1.1.0/diorite-20-hidden.png` | 909 | 144×168 |
| `releases/1.1.0/diorite-commands.log` | 3122 |  |
| `releases/1.1.0/diorite-defaults.png` | 1119 | 144×168 |
| `releases/1.1.0/diorite-runtime.log` | 0 |  |
| `releases/1.1.0/draft-verification.json` | 185 |  |
| `releases/1.1.0/emery-19-visible.png` | 2194 | 200×228 |
| `releases/1.1.0/emery-20-hidden-again.png` | 1612 | 200×228 |
| `releases/1.1.0/emery-20-hidden.png` | 1643 | 200×228 |
| `releases/1.1.0/emery-commands.log` | 8510 |  |
| `releases/1.1.0/emery-defaults.png` | 1951 | 200×228 |
| `releases/1.1.0/emery-migration-option-off-20.png` | 2220 | 200×228 |
| `releases/1.1.0/emery-option-off-20.png` | 2176 | 200×228 |
| `releases/1.1.0/emery-persisted-low-only-19-settled.png` | 2040 | 200×228 |
| `releases/1.1.0/emery-persisted-low-only-20-settled.png` | 1471 | 200×228 |
| `releases/1.1.0/emery-persisted-low-only-20.png` | 1612 | 200×228 |
| `releases/1.1.0/emery-runtime.log` | 0 |  |
| `releases/1.1.0/emulator-captures.json` | 6042 |  |
| `releases/1.1.0/flint-19-visible.png` | 1278 | 144×168 |
| `releases/1.1.0/flint-20-hidden-again.png` | 871 | 144×168 |
| `releases/1.1.0/flint-20-hidden.png` | 871 | 144×168 |
| `releases/1.1.0/flint-commands.log` | 3086 |  |
| `releases/1.1.0/flint-defaults.png` | 1089 | 144×168 |
| `releases/1.1.0/flint-runtime.log` | 0 |  |
| `releases/1.1.0/gabbro-19-visible.png` | 3212 | 260×260 |
| `releases/1.1.0/gabbro-20-hidden-again.png` | 2476 | 260×260 |
| `releases/1.1.0/gabbro-20-hidden.png` | 2507 | 260×260 |
| `releases/1.1.0/gabbro-commands.log` | 3984 |  |
| `releases/1.1.0/gabbro-defaults.png` | 2885 | 260×260 |
| `releases/1.1.0/gabbro-runtime.log` | 0 |  |
| `releases/1.1.0/host-tests.log` | 124 |  |
| `releases/1.1.0/pbw-validation.json` | 1267 |  |
| `releases/1.1.0/public-aplite.json` | 20199 |  |
| `releases/1.1.0/public-basalt.json` | 20199 |  |
| `releases/1.1.0/public-chalk.json` | 20195 |  |
| `releases/1.1.0/public-diorite.json` | 20203 |  |
| `releases/1.1.0/public-emery.json` | 20483 |  |
| `releases/1.1.0/public-flint.json` | 20195 |  |
| `releases/1.1.0/public-gabbro.json` | 20199 |  |
| `releases/1.1.0/publication-verification.json` | 2323 |  |
| `releases/1.1.0/publish-attempt.json` | 69 |  |
| `releases/1.1.0/release-authorization.json` | 1783 |  |
| `releases/1.1.0/release-notes.txt` | 539 |  |
| `releases/1.1.0/review-chalk-diorite.png` | 14201 | 1040×560 |
| `releases/1.1.0/review-first-three.png` | 18811 | 1040×840 |
| `releases/1.1.0/review-flint-gabbro.png` | 16204 | 1040×600 |
| `releases/1.1.0/source.patch` | 6861 |  |
| `releases/1.1.0/upload-attempt.json` | 127 |  |
| `releases/1.1.0/verification.json` | 2723 |  |
| `releases/1.1.0/verify-emulators.py` | 3841 |  |
| `releases/1.1.0/verify-persistence.py` | 923 |  |
| `revisions/classic-red-center/approval.json` | 430 |  |
| `revisions/classic-red-center/banner-emery-720x320.png` | 9012 | 720×320 |
| `revisions/classic-red-center/capture.log` | 2382 |  |
| `revisions/classic-red-center/dashboard-after.json` | 15943 |  |
| `revisions/classic-red-center/dashboard-before.json` | 15943 |  |
| `revisions/classic-red-center/downloaded/banner.png` | 3338 | 720×320 |
| `revisions/classic-red-center/downloaded/emery-01.png` | 769 | 200×228 |
| `revisions/classic-red-center/downloaded/emery-02.png` | 931 | 200×228 |
| `revisions/classic-red-center/downloaded/emery-03.png` | 921 | 200×228 |
| `revisions/classic-red-center/downloaded/emery-04.png` | 1393 | 200×228 |
| `revisions/classic-red-center/downloaded/emery-05.png` | 1421 | 200×228 |
| `revisions/classic-red-center/emery-01-classic-red-center.png` | 1868 | 200×228 |
| `revisions/classic-red-center/mutation-result.json` | 21 |  |
| `revisions/classic-red-center/previous-local/banner-emery-720x320.png` | 8873 | 720×320 |
| `revisions/classic-red-center/previous-local/emery-01-classic-minimal.png` | 1628 | 200×228 |
| `revisions/classic-red-center/previous-local/manifest.md` | 16532 |  |
| `revisions/classic-red-center/previous-local/screenshot-selection.json` | 16684 |  |
| `revisions/classic-red-center/previous-local/store-verification.json` | 21254 |  |
| `revisions/classic-red-center/previous-remote/banner.png` | 3139 | 720×320 |
| `revisions/classic-red-center/previous-remote/emery-01.png` | 706 | 200×228 |
| `revisions/classic-red-center/previous-remote/emery-02.png` | 931 | 200×228 |
| `revisions/classic-red-center/previous-remote/emery-03.png` | 921 | 200×228 |
| `revisions/classic-red-center/previous-remote/emery-04.png` | 1424 | 200×228 |
| `revisions/classic-red-center/previous-remote/emery-05.png` | 1430 | 200×228 |
| `revisions/classic-red-center/provenance.json` | 1526 |  |
| `revisions/classic-red-center/public-banner.png` | 3338 | 720×320 |
| `revisions/classic-red-center/public-current.json` | 18197 |  |
| `revisions/classic-red-center/public-first.png` | 769 | 200×228 |
| `revisions/classic-red-center/public-page.html` | 43568 |  |
| `revisions/classic-red-center/verification.json` | 1773 |  |
| `screenshot-selection.json` | 17036 |  |
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
| `screenshots/emery-01-classic-minimal.png` | 1868 | 200×228 |
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
| `tools/capture-classic-red-center.py` | 3837 |  |
| `tools/capture-screenshots.py` | 5741 |  |
| `tools/draw-banner.py` | 1282 |  |
| `tools/draw-icons.py` | 1548 |  |
| `tools/make-previews.py` | 1438 |  |
| `tools/select-screenshots.py` | 2932 |  |
| `tools/smoke-test.sh` | 1201 |  |
| `tools/write-manifest.py` | 7210 |  |
