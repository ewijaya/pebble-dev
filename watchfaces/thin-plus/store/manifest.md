# Thin+ 1.2.0 — release manifest

Status: **published and publicly listed**. The owner separately approved upload
and publication after passing all six PT2 sideload checks.

- Store: https://apps.repebble.com/b0a4b28dbe9440c3b19f68e3
- Release ID: `e62d92c454904747b53fe0ea`.
- UUID: `0e83e240-01b8-469b-a51b-b2a0e767fefb`.
- Frozen PBW: `../dist/releases/1.2.0/thin-plus.pbw`, **530,875 bytes**.
- SHA-256: `9a015a16f59e33794dabc7f5f47d825ec32c2c1e52893daa7dc5a330e66513f5`.
- Source base: `246a67973784e4f03d3d709c7c0f82eba1efed12` plus uncommitted
  binary-input changes. Exact hashes and patch:
  `../dist/verification/1.2.0/release-prep/{build-inputs.sha256,source.patch}`.
  The base commit alone does not reproduce the release. No new commit/tag/push.
- Tool 5.0.40, SDK 4.33.1. Clean builds for all seven platforms; seven existing
  linker RWX warnings only. Aplite RAM footprint 11,329 / 24,576 bytes; linker
  heap headroom 13,247 bytes (not a runtime measurement). Resources 19,204 bytes.
- All seven emulators installed and rendered the final PBW; screenshots inspected.
  Host/Clay tests passed. 1.1.0 upgrade retained the saved face pixel-for-pixel.
- Owner approved saved settings, Quick View, disconnect controls, tap-for-seconds,
  charging colors and startup animation on PT2. Startup animation defaults off;
  existing saved choices are retained. New visual enhancements remain opt-in.
- Draft and public downloads match the frozen PBW exactly. All seven public
  catalogs and the canonical page show 1.2.0 and updated text.
- Main description, all seven platform descriptions and release notes retain:
  **Based on Thin by Chris Lewis.**
- Approved rectangular icons, Classic banner and 23-image gallery retained.
  Asset paths, dimensions, sizes and SHA-256 hashes:
  [asset inventory](../dist/verification/1.2.0/release-prep/asset-inventory.json).
- [Listing and release notes](release-1.2.0.md).
- [Preparation manifest](../dist/verification/1.2.0/release-prep/manifest.json).
- [Publication verification](../dist/verification/1.2.0/publication/public-download-verification.json).

Pending: owner PT2 store-install/settings/theme confirmation; explicit Git
commit/push/tag approval. Start 1.3.0 only after the owner says go.

Historical 1.0.0 and 1.1.0 evidence remains under `releases/`. Their frozen PBWs
remain under `../dist/releases/`. The previous active manifest is preserved at
`../dist/verification/1.2.0/publication/pre-publication-manifest.md`.
