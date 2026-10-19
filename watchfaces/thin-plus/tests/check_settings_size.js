'use strict';
var assert = require('assert');
var config = require('../src/pkjs/config');
var includes = require('../node_modules/@rebble/clay/src/scripts/lib/utils').includesCapability;
var reports = [];
['aplite','basalt','chalk','diorite','emery','flint','gabbro'].forEach(function(platform) {
  var items = {};
  function walk(list) {
    list.forEach(function(item) {
      if (!includes({platform:platform, firmware:{major:4,minor:33}},item.capabilities)) return;
      if (item.items) walk(item.items);
      if (item.messageKey) {
        assert(!items[item.messageKey], 'duplicate key on '+platform);
        items[item.messageKey] = item;
      }
    });
  }
  walk(config);
  var bytes = 1 + 7 + 4; // Computed TzOffsetMinutes is appended by the phone.
  // Zone names are retained on the phone and removed before sending.
  delete items.SecondTimeZone; delete items.TimeZoneCustom;
  // Pebble dictionary tuple count is included above.
  Object.keys(items).forEach(function(key) {
    var item = items[key];
    var valueBytes = 4; // Bools, colors, ints; CustomStepGoal is normalized to int32 before Clay.
    if (item.type === 'select') {
      valueBytes = Math.max.apply(null,item.options.map(function(option) {
        return Buffer.byteLength(option.value,'utf8') + 1;
      }));
    }
    bytes += 7 + valueBytes;
  });
  assert(bytes < 480, platform+' dictionary would exceed 480-byte budget');
  reports.push({platform:platform, keys:Object.keys(items).length, bytes:bytes, inbox:512});
});
console.log(JSON.stringify(reports,null,2));
