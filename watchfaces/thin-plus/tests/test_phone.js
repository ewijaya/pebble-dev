'use strict';
var assert=require('assert'), fs=require('fs'), vm=require('vm'), Module=require('module');
var names=require('../package.json').pebble.messageKeys, keys={};names.forEach(function(k,i){keys[k]=10000+i;});
var oldLoad=Module._load;Module._load=function(name,parent,isMain){return name==='message_keys'?keys:oldLoad(name,parent,isMain);};
var Clay=require('../node_modules/@rebble/clay/src/js/index.js');Module._load=oldLoad;
var events={},packets=[],store={'clay-settings':JSON.stringify({ColorDate:123,EnableStartupAnim:true})}, weatherCalls=[], cancelled=0;
var storage={getItem:function(k){return store[k]||null;},setItem:function(k,v){store[k]=v;}};
// Clay executes in Node's module context, while the production entry runs in VM.
global.localStorage=storage;
var pebble={platform:'pypkjs',addEventListener:function(k,cb){(events[k]||(events[k]=[])).push(cb);},
 sendAppMessage:function(p,ok){packets.push(p);ok();},getAccountToken:function(){return '';},getWatchToken:function(){return '';},getActiveWatchInfo:function(){return {platform:'emery'};}};
global.Pebble=pebble;
var context={Pebble:pebble,localStorage:storage,console:console,navigator:{},XMLHttpRequest:function(){},setTimeout:setTimeout,clearTimeout:clearTimeout,require:function(name){
 if(name==='@rebble/clay')return Clay;if(name==='message_keys')return keys;
 if(name==='./weather')return function(){return {request:function(u){weatherCalls.push(u);},cancel:function(){cancelled++;}};};
 if(name==='./config')return JSON.parse(JSON.stringify(require('../src/pkjs/config')));
 return require('../src/pkjs/'+name.slice(2));
}};
vm.runInNewContext(fs.readFileSync('src/pkjs/index.js','utf8'),context);
function fire(name,event){events[name].forEach(function(cb){cb(event);});}
fire('ready');assert.strictEqual(packets[0].PhoneReady,1);assert.strictEqual(weatherCalls.length,0);
fire('webviewclosed',{response:JSON.stringify({SlotTop:'9',WeatherUnits:'1',SecondTimeZone:'fixed:345',TimeZoneCustom:'ignored'})});
var packet=packets[1];assert.strictEqual(packet[keys.TzOffsetMinutes],345);assert.strictEqual(packet[keys.SecondTimeZone],undefined);assert.strictEqual(packet[keys.TimeZoneCustom],undefined);assert.strictEqual(packet[keys.ColorDate],undefined);assert.strictEqual(JSON.parse(store['clay-settings']).ColorDate,123);assert.strictEqual(weatherCalls[0],1);assert.strictEqual(cancelled,1);
fire('appmessage',{payload:{TimezoneRequest:1}});assert.strictEqual(packets[2].TzOffsetMinutes,345);
fire('appmessage',{payload:{WeatherRequest:1,WeatherUnits:0}});assert.strictEqual(weatherCalls[1],0);
fire('webviewclosed',{response:'CANCELLED'});assert.strictEqual(cancelled,1);
console.log('PASS: real Clay settings integration, PhoneReady handshake, computed offset, phone-only key removal, partial-setting preservation, weather selection/units and cancellation.');
function save(values) {fire('webviewclosed',{response:encodeURIComponent(JSON.stringify(values))});}
function saved() {return JSON.parse(store['clay-settings']);}
save({StepGoalMode:'1',CustomStepGoal:{value:'10000'}});
assert.strictEqual(saved().CustomStepGoal,10000);assert.strictEqual(saved().StepGoalMode,'1');
assert.strictEqual(packets[packets.length-1][keys.CustomStepGoal],10000);
save({StepGoalMode:'0'});assert.strictEqual(saved().CustomStepGoal,10000);
save({StepGoalMode:'1'});assert.strictEqual(saved().CustomStepGoal,10000);
[0,-1,999,100001,1000.5,'','1e4','1000junk',' 1000','+1000','1000.0',null,true,{}, {value:1000,precision:1}].forEach(function(value) {
 var before=store['clay-settings'],count=packets.length;
 save({CustomStepGoal:value,StepGoalMode:'0',EnableDate:false});
 assert.strictEqual(store['clay-settings'],before);assert.strictEqual(packets.length,count);
});
['',2,-1,'1junk',0.5,null].forEach(function(value) {
 var before=store['clay-settings'],count=packets.length;
 save({StepGoalMode:value});assert.strictEqual(store['clay-settings'],before);assert.strictEqual(packets.length,count);
});
[1000,100000].forEach(function(value) {save({CustomStepGoal:String(value)});assert.strictEqual(saved().CustomStepGoal,value);});
save({EnableDate:true});assert.strictEqual(saved().CustomStepGoal,100000);
assert.strictEqual(saved().ColorDate,123);assert.strictEqual(saved().EnableStartupAnim,true);
console.log('PASS: validated goals before real Clay persistence, integer wire values, range boundaries, missing keys, mode switching and atomic rejection.');
