# Thin+ 1.3.0 — release manifest

Status: **published and publicly listed**, 2026-10-19. The owner approved the
updated PT2 candidate and previews, release review, upload and public publication.

- Store: https://apps.repebble.com/b0a4b28dbe9440c3b19f68e3
- Release ID: `0eacf6a087fb4fc38af9f2d7`.
- UUID: `0e83e240-01b8-469b-a51b-b2a0e767fefb`.
- [Frozen PBW](../dist/releases/1.3.0/thin-plus.pbw): **600,042 bytes**.
- SHA-256: `b25a9fdbe9b55c30ed6fd1dc1df62c0412ea844976e0d8035033303513f656a7`.
- Source base: `246a67973784e4f03d3d709c7c0f82eba1efed12` plus uncommitted
  inputs. [Exact manifest](../dist/releases/1.3.0/manifest.json), complete source
  snapshot and binary source patch are frozen beside the PBW. The base commit
  alone does not reproduce this release. The matching source is identified by
  [thin-plus-v1.3.0](https://github.com/ewijaya/pebble-dev/tree/thin-plus-v1.3.0/watchfaces/thin-plus).
- Tool 5.0.40, SDK 4.33.1. Clean builds for all seven platforms, zero compiler
  warnings and seven known SDK linker notices. Aplite RAM: 15,534 / 24,576 bytes;
  linker-estimated heap headroom 9,042 bytes; resources 19,204 / 131,072 bytes.
- All seven native emulator smoke checks and ten host suites passed.
  [Implementation evidence and emulator limitations](../docs/IMPLEMENTATION-1.3.0.md).
- Owner confirmed the updated custom-goal behavior on PT2 and approved the
  Emery/Gabbro previews. Previous design and PT2 approvals remain recorded.
- Draft and public PBW downloads match the tested package exactly. All seven
  fresh public catalogs show 1.3.0 as latest, with the approved description and
  notes. The canonical webpage initially showed cached 1.2.0 content; final
  page status is recorded in the verification below.
- Credit: **Based on Thin by Chris Lewis.** Verified in all eight descriptions
  and the release notes. Rectangular icons, Classic banner and 23 screenshots
  retained; [26-file asset inventory](../dist/verification/1.3.0/release-prep-custom-goal/asset-inventory.json).
- [Published listing and release notes](release-1.3.0.md).
- [Public download verification](../dist/verification/1.3.0/publication/public-download-verification.json).

The owner confirmed the 1.3.0 PT2 store-install/settings/theme check and requested
the missing GitHub release tags. Tags `thin-plus-v1.2.0` and `thin-plus-v1.3.0`
identify source snapshots checked against the released build-input hashes.
Listed visibility remains unchanged.

Previous active manifest preserved at
`../dist/verification/1.3.0/publication/pre-publication-store-manifest.md`.
Historical release evidence and frozen PBWs are retained.

## Gallery amendment — 2026-10-20

The owner approved replacing only Emery's five screenshots with the 1.3.0
feature gallery: Classic signature/teal ring first, pure Classic second,
Ocean weather, Paper second time zone and Sunset fitness. Screenshot pixels
come directly from the published binary's native SDK framebuffer. Inputs use
simulated time, weather and activity values. No app source or PBW changed.

Other platform galleries, icons, banner, listing copy, release and listed
visibility were verified unchanged. Current selection and hashes are in
[screenshot selection](screenshot-selection.json); earlier inventories remain
historical. [Gallery verification](../dist/verification/1.3.0/gallery-refresh-2026-10-20/public-verification.json).
