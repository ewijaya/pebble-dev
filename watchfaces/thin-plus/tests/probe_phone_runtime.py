#!/usr/bin/env python3
"""Run the actual bundled JS in the emulator's V8, with explicit test phone APIs."""
import json,sys,zipfile
import STPyV8 as v8
setup=r'''
var events={},sent=[],logs=[],storage={};
var console={log:function(s){logs.push(s);},error:function(s){logs.push(s);}};
var Pebble={platform:'pypkjs',addEventListener:function(k,cb){(events[k]||(events[k]=[])).push(cb);},
 getAccountToken:function(){return '';},getWatchToken:function(){return '';},getActiveWatchInfo:function(){return {platform:'emery',firmware:{major:4,minor:33}};},
 sendAppMessage:function(p,ok){sent.push(p);if(ok)ok();},openURL:function(){}};
var localStorage={getItem:function(k){return storage[k]||null;},setItem:function(k,v){storage[k]=v;}};
var navigator={geolocation:{getCurrentPosition:function(ok){ok({coords:{latitude:35,longitude:139}});}}};
var setTimeout=function(){return 1;},clearTimeout=function(){};
function XMLHttpRequest(){}
XMLHttpRequest.prototype.open=function(method,url){this.url=url;};
XMLHttpRequest.prototype.abort=function(){};
XMLHttpRequest.prototype.send=function(){this.status=200;this.responseText=JSON.stringify({current:{temperature_2m:18.4,weather_code:3}});this.onload();};
function fire(name,event){events[name].forEach(function(cb){cb(event);});}
'''
with zipfile.ZipFile(sys.argv[1]) as z:bundle=z.read('pebble-js-app.js').decode()
with v8.JSContext() as ctx:
 ctx.eval(setup);ctx.eval(bundle)
 ctx.eval("fire('ready');fire('appmessage',{payload:{WeatherRequest:1,WeatherUnits:0}});")
 result=json.loads(ctx.eval('JSON.stringify({sent:sent,logs:logs})'))
 assert result['sent'][0]['PhoneReady']==1
 assert any(p.get('WeatherTemp')==18 and p.get('WeatherUnits')==0 for p in result['sent'])
 assert any('fixed UTC offset' in line for line in result['logs'])
 result['scope']='Actual bundled JS in installed STPyV8; simulated phone location/HTTP/AppMessage. Not a phone GPS or end-to-end QEMU transport test.'
 print(json.dumps(result,indent=2))
