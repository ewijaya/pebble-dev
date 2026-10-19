'use strict';
// Use Clay's actual capability rules; color manipulator set(hex), get(int),
// and change-only-on-change semantics are mirrored without needing a browser.
var assert = require('assert');
var config = require('../src/pkjs/config');
var custom = require('../src/pkjs/custom-clay');
var includes = require('../node_modules/@rebble/clay/src/scripts/lib/utils').includesCapability;
function page(platform, overrides, omit) {
  var items = {}, after;
  function walk(list) {
    list.forEach(function(spec) {
      if (!includes({platform: platform, firmware: {major: 4, minor: 33}}, spec.capabilities)) return;
      if (spec.items) walk(spec.items);
      if (!spec.messageKey || (omit || []).indexOf(spec.messageKey) >= 0) return;
      assert(!items[spec.messageKey], 'Duplicate active message key: ' + spec.messageKey);
      var handlers = [], value, visible = true, validity = "";
      function set(next) {
        if (spec.type === 'color') next = parseInt(next, 16);
        if (value !== next) { value = next; handlers.forEach(function(fn) {fn();}); }
      }
      set(Object.prototype.hasOwnProperty.call(overrides || {}, spec.messageKey) ? overrides[spec.messageKey] : spec.defaultValue);
      items[spec.messageKey] = {spec: spec, get: function() {return value;}, set: set,
        on: function(event, fn) {assert(['change','input change'].indexOf(event) >= 0); handlers.push(fn);},
        $manipulatorTarget: [{setCustomValidity: function(message) {validity = message;}}],
        validity: function() {return validity;},
        show: function() {visible = true;}, hide: function() {visible = false;},
        visible: function() {return visible;}};
    });
  }
  walk(config);
  custom.call({EVENTS: {AFTER_BUILD: 'built'}, on: function(event, fn) {after = fn;},
    getItemByMessageKey: function(key) {return items[key];}});
  after();
  return items;
}
['aplite', 'basalt', 'chalk', 'diorite', 'emery', 'flint', 'gabbro'].forEach(function(platform) {
  var items = page(platform);
  assert.strictEqual(items.EnableStartupAnim.get(), false);
  assert.strictEqual(items.DateStyle.get(), '0');
  assert.strictEqual(items.DateStyle.visible(), true);
  items.DateStyle.set('2');
  items.EnableDate.set(false);
  assert.strictEqual(items.DateStyle.visible(), false);
  items.EnableDate.set(true);
  assert.strictEqual(items.DateStyle.visible(), true);
  assert.strictEqual(items.DateStyle.get(), '2');
  assert.strictEqual(page(platform, {EnableDate: false, DateStyle: '1'}).DateStyle.visible(), false);
  assert.strictEqual(page(platform, {EnableStartupAnim: true}).EnableStartupAnim.get(), true);
  assert.strictEqual(!!items.Theme, ['basalt', 'chalk', 'emery', 'gabbro'].indexOf(platform) >= 0);
  ['SlotTop', 'SlotLeft', 'SlotBottom'].forEach(function(key) {
    assert.strictEqual(items[key].spec.options.length, platform === 'aplite' ? 6 : 10);
  });
  assert.strictEqual(!!items.StepGoalMode, platform !== 'aplite');
  assert.strictEqual(!!items.CustomStepGoal, platform !== 'aplite');
  if (items.StepGoalMode) {
    assert.strictEqual(items.EnableStepRing.get(), false);
    assert.strictEqual(items.StepGoalMode.get(), '0');
    assert.strictEqual(items.CustomStepGoal.get(), '7500');
    assert.strictEqual(items.CustomStepGoal.visible(), false);
    items.StepGoalMode.set('1');assert(items.CustomStepGoal.visible());
    items.CustomStepGoal.set('10000');assert.strictEqual(items.CustomStepGoal.validity(), '');
    items.StepGoalMode.set('0');assert(!items.CustomStepGoal.visible());
    items.StepGoalMode.set('1');assert.strictEqual(items.CustomStepGoal.get(), '10000');
    ['','0','999','100001','1000.5','1e4','1000junk'].forEach(function(value) {
      items.CustomStepGoal.set(value);assert(items.CustomStepGoal.validity());
    });
    items.StepGoalMode.set('0');assert.strictEqual(items.CustomStepGoal.get(), '10000');
    assert.strictEqual(items.CustomStepGoal.validity(), '');
    ['1000','100000'].forEach(function(value) {items.CustomStepGoal.set(value);assert.strictEqual(items.CustomStepGoal.validity(),'');});
  }
  if (items.TapForSeconds) assert.strictEqual(platform, 'emery');
});
var customGoalPage = page('emery', {StepGoalMode: '1', CustomStepGoal: '10000'});
assert(customGoalPage.CustomStepGoal.visible());
assert.strictEqual(customGoalPage.CustomStepGoal.get(), '10000');
// Saved colors remain byte-for-byte values when opening the page, including
// newer individual overrides made while a preset name was saved.
var saved = page('emery', {ColorCenterDot: 'AA0000', ColorSecondTip: '0000FF'});
assert.strictEqual(saved.ColorCenterDot.get(), 0xAA0000);
assert.strictEqual(saved.ColorSecondTip.get(), 0x0000FF);
var mismatch = page('emery', {ColorBackground: '550055'});
assert.strictEqual(mismatch.Theme.get(), 'custom');
assert.strictEqual(mismatch.ColorBackground.get(), 0x550055);
var items = page('emery');
['neon', 'ocean', 'sunset', 'lime', 'mono', 'paper', 'classic'].forEach(function(theme) {
  items.Theme.set(theme);
  Object.keys(items).filter(function(key) {return items[key].spec.type === 'color';}).forEach(function(key) {
    assert(Number.isInteger(items[key].get()));
    assert.strictEqual(items[key].visible(), false);
  });
  if (items.ColorCharging && theme === 'paper') assert.notStrictEqual(items.ColorCharging.get(), 0x00FF00);
});
items.Theme.set('custom');
assert.strictEqual(items.ColorBackground.visible(), true);
// Also tolerate a partially built color page, beyond the all-absent BW case.
page('emery', {}, ['ColorBackground', 'ColorSecondTip']);
page('aplite', {}, ['DateStyle']);
console.log('PASS: all seven capability profiles, no duplicate keys, absent/partial colors, saved overrides and seven themes.');
