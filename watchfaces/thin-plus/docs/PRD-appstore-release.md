# PRD: Publish Thin+ 1.0.0 to the Pebble App Store

Status: release 1.0.0 published and publicly listed (2026-10-19); Gates A–C complete. Owner: Edward Wijaya (ewijaya@gmail.com).

Follow-up: version 1.1.0 is published and publicly listed with the optional
below-20% battery complication display. See `store/releases/1.1.0/` and the
current `store/manifest.md`. The requirements and completed gates below record
the original 1.0.0 launch; the physical PT2 check for 1.1.0 remains pending.

## 1. Goal

Publish **Thin+** as a new, free watchface on the Pebble App Store
(apps.repebble.com), for **all 7 platforms**, as version **1.0.0**, with its own
icon, screenshots, description and credit to the original Thin.

Out of scope: new watchface features (weather, step-goal arc), changes to the
original `watchfaces/thin`, and anything in the upstream repo.

## 2. Background

- Thin+ is a fork of **Thin** by Chris Lewis
  (store: https://apps.repebble.com/thin_550ccb556caaed4e0100006d, v1.20.0, 3.7K).
- **Chris Lewis gave permission** for this fork to be published (confirmed by
  Edward on 2026-10-19). The upstream repo has no LICENSE file, so the listing
  and README must credit him and link to the original.
- The owner's main device is a **Pebble Time 2 (emery, 200x228, colour)**. Emery
  is the primary platform for screenshots and the listing's first impression.
- Edward already publishes on this store (Roman Missal, CINÉ, Popeye G&W, ...)
  from https://developer.repebble.com/dashboard.

### What Thin+ adds over Thin (use for the description)

- Smooth anti-aliased hands, hand tips that line up exactly with the hands,
  and an opt-in **Thicker hour and minute hands** setting.
- **Battery-friendly second hand**: shown for 15 s after launch and after a
  wrist flick, otherwise the face only updates once a minute.
- **Three complication slots** (top, left, bottom): steps, heart rate,
  battery %, digital time or none. Numbers only, no labels.
- **Themes**: Classic, Neon, Ocean, Sunset, Lime, Mono, Paper, plus Custom.
- **Every colour customisable** in Custom: background, hour/minute hands,
  hand tips, center dot, second hand, second hand tip, hour markers, empty
  battery markers, day of month, date text.
- Battery level shown on the hour markers (kept from Thin).

## 3. Facts and environment (read before doing anything)

| Item | Value |
| --- | --- |
| Project dir | `~/projects/pebble-dev/watchfaces/thin-plus` |
| Repo / branch | `~/projects/pebble-dev`, branch `watchface/thin-plus` |
| Remotes | `origin` = github.com/ewijaya/pebble-dev (Edward's fork, push here); `upstream` = C-D-Lewis/pebble-dev (never push) |
| UUID | `0e83e240-01b8-469b-a51b-b2a0e767fefb` (never change it) |
| Display name | `Thin+`; package name `thin-plus`; version `1.0.0` in `package.json` |
| Tooling | Pebble Tool 5.0.40, SDK 4.33.1, headless AWS Ubuntu, shell is **zsh** |
| Build output | `build/thin-plus.pbw` (the PBW is named after the **directory**) |

Working notes learned the hard way:

- **Uncommitted work exists**: the "Seconds hand tip" and "Hour markers (empty
  battery)" colours and the AppMessage inbox increase (256 to 512). Edward was
  asked to check them on his PT2. **Ask him to confirm before committing them**,
  then commit them as their own commit.
- After changing `messageKeys` in `package.json`, run `pebble clean` first or
  the generated `MESSAGE_KEY_*` header is stale.
- **Emulators**: run one at a time (`pebble kill` between platforms). Install
  with `pebble install --emulator <platform>`, capture with
  `pebble screenshot --emulator <platform> --no-open <file.png>`. If SDL
  complains, prefix with `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy
  SDL_RENDER_DRIVER=software`. Battery level: `pebble emu-battery --emulator
  <platform> --percent 40`.
- zsh does not word-split `$var`; put multi-step loops in a `bash` script.
- **Screenshots of specific states** (themes, filled slots, thick hands): Clay's
  config page cannot run headless, so temporarily hard-code return values at
  the top of `data_get_color` / `data_get_slot` / `data_get_enable` in
  `src/c/modules/data.c`, mark each line `// TEMP_TEST`, build, capture, then
  restore the file and `grep -c TEMP_TEST` must be 0. Prefer doing this in a
  scratch copy (`rsync -a --exclude build`) so the repo is never dirty.
- Theme colours live in `src/pkjs/custom-clay.js` (`THEMES`, ordered like
  `COLOR_KEYS`).
- **Physical install** to Edward's PT2: `pebble install --cloudpebble
  build/thin-plus.pbw` (no phone IP, no tunnel; login persists on this server,
  check with `pebble login --status`). If it hangs, ask Edward to reopen the
  Pebble app on his phone (Xiaomi kills background apps).
- **Do not use `pebble publish`**: in pebble-tool 5.0.40 it rebuilds and forces
  the listing visible/published. Reference for the store dashboard API and a
  careful release procedure: `~/projects/pebble-daily-mass/docs/RELEASING.md`
  (section "Pebble App Store"). Read it; do not run its scripts.
- The README TODO says "Support flint once pebble-clay does". Thin's store page
  lists 2 Duo as supported, so verify the settings page path on flint is not
  broken (at minimum: builds, runs, and the face renders with defaults).

## 4. Requirements

### R1. Release candidate

1. Commit the pending work (after Edward confirms, see section 3).
2. Smoke-test **every platform** in the emulator: aplite, basalt, chalk,
   diorite, emery, flint, gabbro. For each: installs, face renders with
   defaults, no crash in `pebble logs` for ~20 s. Check aplite memory headroom
   in the build output (it has the least RAM).
3. Clean build (`pebble clean && pebble build`), no compiler warnings except
   the known linker `RWX` notices.
4. Validate `appinfo.json` inside the PBW (it is a ZIP): UUID, `displayName`
   `Thin+`, version `1.0.0`, `watchface: true`, all 7 `targetPlatforms`.
   Record PBW size and SHA-256.

### R2. Icon

- Design a **new icon** that reads as "Thin, plus": thin analog hands with a
  small plus, high contrast. It must not reuse Thin's icon.
- Store icon revision requested by Edward: use a rectangular PT2-style face
  outline rather than a circular dial. This changes the store icons only;
  the validated PBW's embedded menu icon remains unchanged.
- Replace `resources/images/menu_icon.png` (keep 25x25, same resource name
  `MENU_ICON`), and produce the store icon sizes the dashboard asks for.
  Historically these were **48x48** and **144x144** PNG; confirm the current
  sizes from the dashboard's New App form (ask Edward to read them out or send
  a screenshot) or from developer.repebble.com docs before finalising.

### R3. Screenshots

- Native resolution, unscaled, PNG, from the emulator:
  emery 200x228, gabbro 260x260, chalk 180x180, basalt/diorite/flint/aplite
  144x168 (aplite is black and white).
- Emery set (revised by Edward after Gate A): a range from minimal to rich.
  Classic with date and all slots hidden; Neon with date only; Ocean with
  digital time and steps; Paper with all complications; Sunset with all
  complications, **Thicker hands** on and battery at ~40%.
- Each other platform gets minimal, medium (digital time and date), and rich
  layouts. Health slots depend on the platform's capabilities.
- At least one screenshot for each other platform family: gabbro, chalk,
  basalt, aplite.
- Replace the old Thin screenshots in `screenshots/` that the README uses
  (keep `ghstats.png` only if the README still refers to Thin's history; it
  is Thin's history, so remove it from Thin+).
- If the dashboard supports a header/banner image (historically **720x320**),
  make one: the minimal emery face on a dark background with the name "Thin+"
  and Edward's selected tagline: "The Thin you love. More ways to make it yours."

### R4. Listing text

Draft in `store/listing.md` for Edward's review:

- **Name**: Thin+  **Category**: Faces  **Author**: Edward Wijaya (match how his
  other listings show the author).
- **Description**: short opener ("Thin, plus: ..."), then the feature list
  from section 2, then: "Based on Thin by Chris Lewis." with a link to the
  original listing. Use this exact credit, including the full stop, as revised
  by Edward after Gate A.
- **Release notes 1.0.0**: first release; summarise the features.
- **Source**: https://github.com/ewijaya/pebble-dev/tree/watchface/thin-plus/watchfaces/thin-plus
- **Website**: leave empty unless Edward gives one.

### R5. Packaging for the upload

Create `store/` in the project with the icon files, screenshots (named by
platform), banner if any, `listing.md`, and a `manifest.md` listing every file
with its size, the PBW SHA-256 and the source commit. The PBW itself stays in
`build/` (ignored); copy it to `store/` only if Edward wants it committed (default:
do not commit PBWs).

### R6. Publish (staged, with approval gates)

1. **Gate A**: show Edward the icon, the screenshots and `listing.md`. Iterate
   until he approves.
2. Edward creates the listing himself in the dashboard (**New**, Watchface),
   using the files in `store/`, with the app **hidden/unlisted** and the 1.0.0
   release uploaded. Offer step-by-step field-by-field instructions. Do not
   create the listing via API unless Edward explicitly asks for it.
3. Verify the listing (read-only): ask Edward for the dashboard/share link and
   check the public page fields, or, if he wants, read it via the dashboard API
   as described in the Daily Mass RELEASING.md (never print tokens).
4. **Gate B**: Edward installs Thin+ **from the store** on his PT2 and checks
   that the settings page opens and applies a theme.
5. **Gate C**: only after Edward says so, switch visibility to listed (he does
   it in the dashboard, or you do it via API if he asks).

### R7. After publishing

- Update `README.md`: describe Thin+ (not Thin), new screenshots, store link,
  credit line "Based on Thin by Chris Lewis."; remove Thin's stale TODO list
  and history section.
- Commit and push to `origin` (`watchface/thin-plus`). Then tag `thin-plus-v1.0.0`
  on the released commit and push the tag, **only after asking**.

## 5. Acceptance criteria

- [x] Pending colour work confirmed by Edward and committed.
- [x] All 7 platforms install and render in the emulator; evidence screenshots saved.
- [x] PBW `appinfo.json` validated; size and SHA-256 recorded in `store/manifest.md`.
- [x] New icon in the app and at the store sizes; Edward approved it.
- [x] Screenshots per section R3; Edward approved them.
- [x] `store/listing.md` approved by Edward, including the credit line.
- [x] Listing live and **installed from the store** on the PT2 with working settings.
- [x] Visibility switched to listed only after Edward's go-ahead.
- [ ] README updated, committed and pushed; tag pushed after asking.

## 6. Rules for the implementing agent

- Never push to `upstream`, never force-push, never change the UUID.
- Anything that publishes or changes the store (create listing, upload,
  publish, visibility) happens only at the gates above, with Edward's explicit
  go-ahead each time.
- Commit only when Edward asks or a gate above says so; conventional commit
  messages; follow `~/.claude/CLAUDE.md`.
- Report honestly what was verified in the emulator, what on the PT2, and what
  is still pending.
