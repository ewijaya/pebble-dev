var Clay = require('@rebble/clay');
var config = require('./config');
var customClay = require('./custom-clay');
var timezones = require('./timezones');
var stepGoal = require('./step-goal');
var keys = require('message_keys');
var namedZones = timezones.supportsNamedZones(Pebble.platform);
timezones.configure(config, namedZones);
var clay = new Clay(config, customClay, {autoHandleEvents: false});

function settings() {
  try {return JSON.parse(localStorage.getItem('clay-settings')) || {};} catch (error) {return {};}
}
function selected(values, type) {
  return ['SlotTop', 'SlotLeft', 'SlotBottom'].some(function(key) {return String(values[key]) === String(type);});
}
// Serialize settings and live-data packets so AppMessages cannot collide.
var queue = [], sending = false;
function send(packet, done) {
  queue.push({packet: packet, done: done});
  drain();
}
function drain() {
  if (sending || !queue.length) return;
  sending = true;
  var item = queue.shift();
  Pebble.sendAppMessage(item.packet, function() {
    sending = false;
    if (item.done) item.done();
    drain();
  }, function() {
    sending = false;
    console.log('Thin+: message not delivered; retry on the next refresh or settings save.');
    drain();
  });
}
function timezoneValue(values) {
  var zone = values.SecondTimeZone || (namedZones ? 'UTC' : 'fixed:0');
  if (zone === 'custom') zone = String(values.TimeZoneCustom || '').trim().slice(0,64);
  if (!namedZones && zone !== 'UTC' && zone.indexOf('fixed:') !== 0) return 10000;
  var offset = timezones.offset(zone, new Date());
  return offset === null ? 10000 : offset;
}
function sendTimezone() {send({TzOffsetMinutes: timezoneValue(settings())});}
var weather = require('./weather')({navigator: navigator, XMLHttpRequest: XMLHttpRequest,
  setTimeout: setTimeout, clearTimeout: clearTimeout, storage: localStorage,
  now: function() {return Date.now();}, log: function(text) {console.log(text);}, send: send});

Pebble.addEventListener('ready', function() {
  console.log('Thin+ timezone mode: ' + (namedZones ? 'IANA with DST' : 'fixed UTC offset'));
  send({PhoneReady: 1});
});
Pebble.addEventListener('showConfiguration', function() {Pebble.openURL(clay.generateUrl());});
Pebble.addEventListener('webviewclosed', function(event) {
  if (!event || !event.response || event.response === 'CANCELLED') return;
  try {
    var prior = settings();
    // getSettings writes storage immediately: parse and validate before calling it.
    var response = event.response;
    var raw = JSON.parse(response.charAt(0) === '{' ? response : decodeURIComponent(response));
    stepGoal.validate(raw);
    raw = clay.getSettings(JSON.stringify(raw), false);
    Object.keys(raw).forEach(function(key) {
      prior[key] = raw[key] && typeof raw[key] === 'object' ? raw[key].value : raw[key];
    });
    prior.TimeZoneCustom = String(prior.TimeZoneCustom || '').slice(0,64);
    clay.setSettings(prior);
    var packet = Clay.prepareSettingsForAppMessage(raw);
    // Zone names stay on the phone; only the computed offset crosses AppMessage.
    delete packet[keys.SecondTimeZone]; delete packet[keys.TimeZoneCustom];
    packet[keys.TzOffsetMinutes] = timezoneValue(prior);
    weather.cancel();
    send(packet, function() {
      if (selected(prior, 9)) weather.request(Number(prior.WeatherUnits) === 1 ? 1 : 0);
    });
  } catch (error) {console.log('Thin+: could not read settings: ' + error.message);}
});
Pebble.addEventListener('appmessage', function(event) {
  var packet = event.payload || {};
  function value(name) {return packet[name] !== undefined ? packet[name] : packet[keys[name]];}
  if (value('TimezoneRequest')) sendTimezone();
  if (value('WeatherRequest')) {
    if (!value('TimezoneRequest') && selected(settings(), 8)) sendTimezone();
    weather.request(Number(value('WeatherUnits')) === 1 ? 1 : 0);
  }
});
