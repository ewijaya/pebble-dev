'use strict';
// Dependencies are explicit so failure paths can run without a phone or network.
module.exports = function(env) {
  var generation = 0, busy = false, activeUnits = null, xhr = null, timer = null;
  function cancel() {
    generation++; busy = false;
    if (timer !== null) env.clearTimeout(timer);
    timer = null;
    if (xhr) { var old = xhr; xhr = null; old.abort(); }
  }
  function cachedPosition() {
    try {
      var p = JSON.parse(env.storage.getItem('thin-position'));
      return p && typeof p.lat === 'number' && typeof p.lon === 'number' &&
        Math.abs(p.lat) <= 90 && Math.abs(p.lon) <= 180 &&
        env.now() >= p.time && env.now() - p.time < 86400000 ? p : null;
    } catch (error) { return null; }
  }
  function request(units) {
    if (busy && units === activeUnits) return;
    if (busy) cancel();
    activeUnits = units;
    busy = true;
    var id = ++generation;
    function finish(reason) {
      if (id !== generation) return;
      busy = false;
      if (timer !== null) env.clearTimeout(timer);
      timer = null; xhr = null;
      if (reason) env.log('Weather: ' + reason + '; keeping the last reading.');
    }
    function fetchAt(position) {
      if (id !== generation) return;
      try {
        xhr = new env.XMLHttpRequest();
        var current = xhr;
        var url = 'https://api.open-meteo.com/v1/forecast?latitude=' + encodeURIComponent(position.lat) +
          '&longitude=' + encodeURIComponent(position.lon) + '&current=temperature_2m,weather_code' +
          '&temperature_unit=' + (units === 1 ? 'fahrenheit' : 'celsius');
        current.open('GET', url, true);
        // iOS PebbleKit JS does not implement XHR.timeout; use our own timer.
        timer = env.setTimeout(function() {
          if (id !== generation) return;
          generation++; busy = false; timer = null; xhr = null; current.abort();
          env.log('Weather: request timed out; keeping the last reading.');
        }, 15000);
        current.onerror = function() {finish('network error');};
        current.onload = function() {
          if (id !== generation || !busy) return;
          if (current.status !== 200) {finish('HTTP ' + current.status); return;}
          try {
            var result = JSON.parse(current.responseText).current;
            if (!result || typeof result.temperature_2m !== 'number' || !isFinite(result.temperature_2m) ||
                typeof result.weather_code !== 'number' || !isFinite(result.weather_code) ||
                result.weather_code < 0 || result.weather_code > 99 || result.weather_code % 1 !== 0 ||
                result.temperature_2m < -150 || result.temperature_2m > 180) throw new Error('invalid data');
            finish();
            env.log('Weather: received ' + (units === 1 ? 'Fahrenheit' : 'Celsius') + ' reading.');
            env.send({WeatherTemp: Math.round(result.temperature_2m), WeatherCode: result.weather_code, WeatherUnits: units});
          } catch (error) {finish('invalid response');}
        };
        current.send();
      } catch (error) {finish('request could not start');}
    }
    function locationFailed(error) {
      if (id !== generation || !busy || xhr) return;
      if (timer !== null) env.clearTimeout(timer);
      timer = null;
      // Respect a revoked permission instead of silently using stored coordinates.
      var cached = error && error.code === 1 ? null : cachedPosition();
      if (cached) fetchAt(cached); else finish('phone position unavailable');
    }
    if (!env.navigator || !env.navigator.geolocation) {locationFailed({code: 1}); return;}
    timer = env.setTimeout(function() {locationFailed({code: 3});}, 12000);
    try {
      env.navigator.geolocation.getCurrentPosition(function(position) {
        if (id !== generation || !busy || xhr) return;
        if (timer !== null) env.clearTimeout(timer);
        timer = null;
        var c = position && position.coords;
        if (!c || typeof c.latitude !== 'number' || typeof c.longitude !== 'number' ||
            !isFinite(c.latitude) || !isFinite(c.longitude) || Math.abs(c.latitude) > 90 || Math.abs(c.longitude) > 180) {
          locationFailed({code: 2}); return;
        }
        var p = {lat: c.latitude, lon: c.longitude, time: env.now()};
        try {env.storage.setItem('thin-position', JSON.stringify(p));} catch (error) {}
        fetchAt(p);
      }, locationFailed, {timeout: 10000, maximumAge: 30 * 60 * 1000, enableHighAccuracy: false});
    } catch (error) {locationFailed({code: 2});}
  }
  return {request: request, cancel: cancel};
};
