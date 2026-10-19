"""Write the Gate A inventory, including stable self-size accounting."""
from pathlib import Path
from PIL import Image
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
STORE=ROOT/'store'
v=json.loads((STORE/'evidence/final-validation.json').read_text())
pbw=ROOT/'build/thin-plus.pbw'
assert hashlib.sha256(pbw.read_bytes()).hexdigest()==v['pbw_sha256']
assert pbw.stat().st_size==v['pbw_bytes']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==v['source_commit']
for line in (STORE/'evidence/build-inputs.sha256').read_text().splitlines():
    digest,name=line.split('  ',1)
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
manifest=STORE/'manifest.md'
intro=f'''# Thin+ 1.0.0 — Gate A manifest

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
- Size: **{v['pbw_bytes']:,} bytes**.
- SHA-256: `{v['pbw_sha256']}`.
- Base source commit: `{v['source_commit']}` (`watchface/thin-plus`).
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
'''
manifest.touch(exist_ok=True)
for _ in range(10):
    rows=[]
    for p in sorted(STORE.rglob('*')):
        if not p.is_file():continue
        dims=''
        if p.suffix.lower()=='.png':
            with Image.open(p) as im: dims=f'{im.width}×{im.height}'
        rows.append(f'| `{p.relative_to(STORE)}` | {p.stat().st_size} | {dims} |\n')
    content=intro+''.join(rows)
    previous=manifest.read_text()
    manifest.write_text(content)
    if previous==content:break
else:raise RuntimeError('Manifest self-size did not converge')
print(f'Manifest written: {len(rows)} files; PBW {v["pbw_bytes"]} bytes / {v["pbw_sha256"]}')
