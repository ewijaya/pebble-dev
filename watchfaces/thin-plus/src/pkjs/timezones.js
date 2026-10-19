'use strict';

function offset(zone, when) {
  if (/^fixed:-?\d+$/.test(zone)) {
    var fixed = Number(zone.slice(6));
    return fixed >= -720 && fixed <= 840 && fixed % 15 === 0 ? fixed : null;
  }
  if (zone === 'UTC') return 0;
  try {
    var parts = new Intl.DateTimeFormat('en-US', {timeZone: zone, year: 'numeric',
      month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit',
      hourCycle: 'h23', hour12: false}).formatToParts(when);
    var values = {};
    parts.forEach(function(part) {values[part.type] = part.value;});
    var local = Date.UTC(Number(values.year), Number(values.month) - 1, Number(values.day),
      Number(values.hour) % 24, Number(values.minute));
    var result = Math.round((local - Math.floor(when.getTime() / 60000) * 60000) / 60000);
    return isFinite(result) && result >= -720 && result <= 840 ? result : null;
  } catch (error) { return null; }
}

function supportsNamedZones(platform) {
  // The bundled emulator V8 crashes inside ICU (not a catchable JS exception).
  if (platform === 'pypkjs' || typeof Intl === 'undefined') return false;
  return offset('Asia/Tokyo', new Date('2026-01-01T00:00:00Z')) === 540 &&
    offset('America/New_York', new Date('2026-07-01T00:00:00Z')) === -240;
}

function configure(config, namedZones) {
  if (namedZones) return;
  function walk(items) {
    for (var i = items.length - 1; i >= 0; i--) {
      var item = items[i];
      if (item.items) walk(item.items);
      if (item.messageKey === 'TimeZoneCustom') items.splice(i, 1);
      if (item.messageKey === 'SecondTimeZone') {
        item.defaultValue = 'fixed:0';
        item.description = 'Fixed UTC offset. This phone runtime cannot format named zones; adjust manually for daylight-saving changes.';
        item.options = [];
        for (var minutes = -720; minutes <= 840; minutes += 15) {
          var magnitude = Math.abs(minutes);
          item.options.push({value: 'fixed:' + minutes, label: 'UTC' + (minutes < 0 ? '-' : '+') +
            ('0' + Math.floor(magnitude / 60)).slice(-2) + ':' + ('0' + (magnitude % 60)).slice(-2)});
        }
      }
    }
  }
  walk(config);
}
module.exports = {offset: offset, supportsNamedZones: supportsNamedZones, configure: configure};
