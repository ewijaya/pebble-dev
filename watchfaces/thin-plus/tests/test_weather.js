'use strict';
var assert = require('assert');
var makeWeather = require('../src/pkjs/weather');
var zones = require('../src/pkjs/timezones');
function setup() {
  var calls=[], sent=[], logs=[], timers={}, storage={}, success, failure, next=1;
  function XHR() {calls.push(this);}
  XHR.prototype.open=function(method,url){this.url=url;};
  XHR.prototype.send=function(){};
  XHR.prototype.abort=function(){this.aborted=true;};
  var env={navigator:{geolocation:{getCurrentPosition:function(ok,bad){success=ok;failure=bad;}}},
    XMLHttpRequest:XHR, now:function(){return 1800000000000;},
    storage:{getItem:function(k){return storage[k]||null;},setItem:function(k,v){storage[k]=v;}},
    setTimeout:function(fn){var id=next++;timers[id]=fn;return id;},clearTimeout:function(id){delete timers[id];},
    send:function(p){sent.push(p);},log:function(s){logs.push(s);}};
  var api=makeWeather(env);
  return {api:api, calls:calls,sent:sent,logs:logs,storage:storage,
    locate:function(){success({coords:{latitude:35.68,longitude:139.76}});},
    fail:function(code){failure({code:code});},
    timeout:function(){var id=Object.keys(timers)[0],fn=timers[id];delete timers[id];fn();},
    respond:function(status,body){var x=calls[calls.length-1];x.status=status;x.responseText=typeof body==='string'?body:JSON.stringify(body);x.onload();}};
}
var t=setup();t.api.request(0);t.locate();assert(t.calls[0].url.indexOf('temperature_unit=celsius')>=0);
t.respond(200,{current:{temperature_2m:18.6,weather_code:3}});assert.deepStrictEqual(t.sent,[{WeatherTemp:19,WeatherCode:3,WeatherUnits:0}]);
['bad json', {current:{temperature_2m:null,weather_code:0}}, {current:{temperature_2m:25,weather_code:'3'}}].forEach(function(body){t=setup();t.api.request(0);t.locate();t.respond(200,body);assert.strictEqual(t.sent.length,0);});
t=setup();t.api.request(0);t.locate();t.respond(503,{});assert.strictEqual(t.sent.length,0);assert(t.logs[0].indexOf('HTTP 503')>=0);
t=setup();t.api.request(0);t.locate();t.calls[0].onerror();assert.strictEqual(t.sent.length,0);
t=setup();t.api.request(0);t.locate();t.timeout();assert(t.calls[0].aborted);t.respond(200,{current:{temperature_2m:18,weather_code:0}});assert.strictEqual(t.sent.length,0);
t=setup();t.storage['thin-position']=JSON.stringify({lat:35,lon:139,time:1800000000000});t.api.request(0);t.fail(1);assert.strictEqual(t.calls.length,0); // permission denial never falls back
// A location timeout may use a fresh cached position, without a late callback launching a second request.
t=setup();t.storage['thin-position']=JSON.stringify({lat:35,lon:139,time:1800000000000});t.api.request(0);t.timeout();assert.strictEqual(t.calls.length,1);t.locate();t.fail(2);assert.strictEqual(t.calls.length,1);
t=setup();t.api.request(0);t.locate();var old=t.calls[0];t.api.request(1);assert(old.aborted);t.locate();assert(t.calls[1].url.indexOf('fahrenheit')>=0);old.status=200;old.responseText=JSON.stringify({current:{temperature_2m:18,weather_code:0}});old.onload();assert.strictEqual(t.sent.length,0);t.respond(200,{current:{temperature_2m:72.2,weather_code:0}});assert.strictEqual(t.sent[0].WeatherUnits,1);
t=setup();t.api.request(0);t.api.cancel();t.locate();assert.strictEqual(t.calls.length,0);
assert(zones.supportsNamedZones('android'));assert(!zones.supportsNamedZones('pypkjs'));
assert.strictEqual(zones.offset('America/New_York',new Date('2026-01-01T00:00:00Z')),-300);
assert.strictEqual(zones.offset('America/New_York',new Date('2026-07-01T00:00:00Z')),-240);
assert.strictEqual(zones.offset('Asia/Kolkata',new Date('2026-01-01T23:59:00Z')),330);
assert.strictEqual(zones.offset('Pacific/Auckland',new Date('2026-01-01T12:00:00Z')),780);
assert.strictEqual(zones.offset('No/Such_Zone',new Date()),null);
assert.strictEqual(zones.offset('fixed:-345',new Date()),-345);
assert.strictEqual(zones.offset('fixed:841',new Date()),null);
var config=JSON.parse(JSON.stringify(require('../src/pkjs/config')));zones.configure(config,false);
var items=config.reduce(function(a,s){return a.concat(s.items||[]);},[]);
assert(!items.some(function(x){return x.messageKey==='TimeZoneCustom';}));
assert.strictEqual(items.filter(function(x){return x.messageKey==='SecondTimeZone';})[0].options.length,105);
console.log('PASS: weather success, C/F, malformed data, HTTP/network/timeout/denial, cache fallback, late callbacks, cancellation, DST/IANA validation and fixed-offset fallback.');
