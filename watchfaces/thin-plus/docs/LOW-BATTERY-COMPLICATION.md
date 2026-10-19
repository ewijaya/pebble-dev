# Low-battery-only complication (1.1.0)

The Complications section now has **Show battery percentage only below 20%**.
It defaults to off so existing installations retain their current behavior.

- With the option on, slots set to **Battery** display their percentage at 0–19%
  and are blank at 20–100%. It applies to any or all of Top, Left and Bottom.
- Slots set to None, Steps, Heart rate or Digital time keep their own behavior.
- **Show battery level (hour markers)** is independent: when on, the marks around
  the edge change to the empty-marker color as the battery drains. When off, all
  markers use their normal color. The settings page now explains this.
- Battery events redraw both the hour-marker canvas and the complication layer.
  A hidden battery slot remains subscribed to battery changes so it appears when
  the level crosses below 20% and disappears when it recovers to 20%.

The new message key is appended to preserve existing key IDs. The persisted
boolean is appended to the settings struct and initialized to false before
reading older settings. Older settings messages without the key preserve the
current value. Existing themes and marker colors are unchanged.

## Development verification

Run `python3 tests/test_low_battery.py`. This compiles the production data and
slot-rendering code with small host SDK stubs and address/undefined-behavior
sanitizers. It checks old-record migration, preference persistence, all three
positions, 0/1/19/20/21/100%, both toggle states, other complication types and
independence from the hour-marker switch.

The development PBW is `dist/low-battery/thin-plus.pbw`; its clean-build log,
emulator screenshots, command logs and results are alongside it. These files
are ignored development artifacts. The build ran in a scratch copy because the
existing `build/thin-plus.pbw` is the published 1.0.0 artifact and was preserved.

Verified in development:

- Clean builds and PBW validation passed for all seven platforms. Host tests
  passed with address and undefined-behavior sanitizers.
- All seven emulators hid all three battery slots at a reported 20% and showed
  them below 20%, using real settings messages and battery events.
- Emery, Flint and Gabbro showed 19% and hid 20%. Aplite and Diorite reported
  10% for a requested 19%; Basalt and Chalk reported 20% for that request, so
  those two were additionally checked at reported 10% and 0% (visible), then
  20% (hidden). Exact 19%/20% logic is also covered by the host tests.
- Emery checks covered migration from the released PBW (new option off),
  switching the option off at 20%, mixed complication types, and saving and
  restoring the enabled preference after reinstalling the development PBW.
- These emulator checks exercised AppMessage and rendering. The phone settings
  UI and physical PT2 behavior still need checking on the device.

Development PBW SHA-256:
`9afb435867795de55d093a37da685bbe2650c3d62f4a66fe1bc5eeaa4d4ef729`.

Version 1.1.0 is now published and publicly listed. The release PBW is
`dist/releases/1.1.0/thin-plus.pbw`, also copied to `build/thin-plus.pbw`.
The original 1.0.0 PBW is preserved in `dist/releases/1.0.0/thin-plus.pbw`.
Final-candidate builds, seven-platform emulator checks, upgrade/persistence
evidence and public download verification are in `store/releases/1.1.0/`.
The approved Classic artwork is unchanged. A physical PT2 store-install,
settings/theme and new battery-option check is still pending.

Release PBW SHA-256: `15e75184f8381cc19a94fbbcd192323251a2ae9bd0cf5e1676d64b22c50131fd`.
