// Values must match SlotType in src/c/modules/data.h
var slotOptions = [
  { "label": "None", "value": "0" },
  { "label": "Steps", "value": "1" },
  { "label": "Heart rate", "value": "2" },
  { "label": "Battery", "value": "3" },
  { "label": "Digital time", "value": "4" },
  { "label": "Distance (km/mi)", "value": "5" },
  { "label": "Active calories", "value": "6" },
  { "label": "Week number", "value": "7" },
  { "label": "Second time zone", "value": "8" },
  { "label": "Weather", "value": "9" }
];

function slotSelect(label, key, value, health) {
  return {
    type: 'select', label: label, messageKey: key, defaultValue: value,
    capabilities: [health ? 'HEALTH' : 'NOT_HEALTH'],
    options: health ? slotOptions : slotOptions.filter(function(option) {
      return ['1', '2', '5', '6'].indexOf(option.value) < 0;
    })
  };
}

module.exports = [
  { 
    "type": "heading", 
    "defaultValue": "Thin+ Configuration" ,
    "size": 3
  }, 
  {
    "type": "section",
    "items": [
      {
        "type": "heading",
        "defaultValue": "Features"
      },
      {
        "type": "toggle",
        "label": "Show current date",
        "messageKey": "EnableDate",
        "defaultValue": true
      },
      {
        type: 'select', label: 'Date style', messageKey: 'DateStyle', defaultValue: '0',
        options: [
          {label: 'Full', value: '0'},
          {label: 'Day only', value: '1'},
          {label: 'Weekday and day', value: '2'}
        ]
      },
      {
        "type": "toggle",
        "label": "Show disconnected indicator",
        "messageKey": "EnableBT",
        "defaultValue": true
      },
      {
        type: 'toggle', label: 'Vibrate on disconnect',
        messageKey: 'VibrateOnDisconnect', defaultValue: true,
        description: 'Buzz when the phone disconnects. Applies when Show disconnected indicator is on.'
      },
      {
        type: 'toggle', label: 'Larger disconnected indicator',
        messageKey: 'EnableEnhancedBT', defaultValue: false,
        description: 'Use a larger colored ring. Applies when Show disconnected indicator is on.'
      },
      {
        "type": "toggle",
        "label": "Show battery level (hour markers)",
        "messageKey": "EnableBattery",
        "description": "Hour marks around the edge dim as the battery drains. Turn off to keep every mark in its normal color.",
        "defaultValue": true
      },
      {
        type: 'toggle', label: 'Highlight hour markers while charging',
        messageKey: 'EnableChargingColor', defaultValue: false,
        description: 'Use the charging color for filled markers. Requires Show battery level (hour markers).'
      },
      {
        "type": "toggle",
        "label": "Show second hand (for 15s after a wrist flick)",
        "messageKey": "EnableSecondHand",
        "defaultValue": true
      },
      {
        type: 'toggle', label: 'Tap the face to show the second hand',
        messageKey: 'TapForSeconds', defaultValue: false,
        capabilities: ['PLATFORM_EMERY'],
        description: 'Requires Show second hand. May use more battery: the touch sensor stays enabled while this option is on.'
      },
      {
        type: 'toggle', label: 'Step goal ring', messageKey: 'EnableStepRing',
        defaultValue: false, capabilities: ['HEALTH'],
        description: 'Show progress toward your daily step goal, up to 100%.'
      },
      {
        type: 'select', label: 'Goal', messageKey: 'StepGoalMode',
        defaultValue: '0', capabilities: ['HEALTH'],
        options: [{label: 'Automatic', value: '0'}, {label: 'Custom', value: '1'}],
        description: 'Automatic uses Pebble Health’s typical daily step count, falling back to 7,500 when it is unavailable or zero. Custom uses your chosen daily target.'
      },
      {
        type: 'input', label: 'Daily step goal', messageKey: 'CustomStepGoal',
        defaultValue: '7500', capabilities: ['HEALTH'],
        attributes: {type: 'number', min: 1000, max: 100000, step: 1, required: true},
        description: 'Enter a whole number from 1,000 to 100,000. Your custom goal is kept when you switch to Automatic.'
      },
      {
        type: 'toggle', label: 'Animate hands when the face opens',
        messageKey: 'EnableStartupAnim', defaultValue: false
      },
      {
        "type": "toggle",
        "label": "Thicker hour and minute hands",
        "messageKey": "EnableThickHands",
        "defaultValue": false
      }
    ]
  },
  {
    "type": "section",
    "items": [
      {
        "type": "heading",
        "defaultValue": "Complications"
      },
      slotSelect('Top', 'SlotTop', '0', true),
      slotSelect('Top', 'SlotTop', '0', false),
      slotSelect('Left', 'SlotLeft', '0', true),
      slotSelect('Left', 'SlotLeft', '0', false),
      slotSelect('Bottom', 'SlotBottom', '1', true),
      slotSelect('Bottom', 'SlotBottom', '0', false),
      {
        type: 'select', label: 'Second time zone', messageKey: 'SecondTimeZone', defaultValue: 'UTC',
        description: 'Used by slots set to Second time zone. Named zones adjust for daylight saving when refreshed.',
        options: ['UTC', 'America/Los_Angeles', 'America/Denver', 'America/Chicago', 'America/New_York',
          'America/Sao_Paulo', 'Europe/London', 'Europe/Paris', 'Asia/Dubai', 'Asia/Kolkata',
          'Asia/Singapore', 'Asia/Tokyo', 'Australia/Sydney', 'Pacific/Auckland'].map(function(zone) {
          return {label: zone.replace(/_/g, ' '), value: zone};
        }).concat([{label: 'Custom IANA zone', value: 'custom'}])
      },
      {
        type: 'input', label: 'Custom IANA time zone', messageKey: 'TimeZoneCustom', defaultValue: '',
        attributes: {maxlength: 64},
        description: 'For Custom only, for example Europe/Rome. An invalid zone leaves the slot blank.'
      },
      {
        type: 'select', label: 'Temperature units', messageKey: 'WeatherUnits', defaultValue: '0',
        options: [{label: 'Celsius (°C)', value: '0'}, {label: 'Fahrenheit (°F)', value: '1'}],
        description: 'Weather uses your phone location only when a slot is set to Weather. Updates about every 30 minutes; readings older than 3 hours are hidden.'
      },
      {type: 'text', defaultValue: 'Weather by <a href="https://open-meteo.com/">Open-Meteo</a>.'},
      {
        "type": "toggle",
        "label": "Show battery percentage only below 20%",
        "messageKey": "BatteryOnlyWhenLow",
        "description": "Applies to top, left or bottom slots set to Battery. Hidden at 20% or higher. Hour markers are controlled separately.",
        "defaultValue": false
      }
    ]
  },
  {
    "type": "section",
    "items": [
      {
        "type": "heading",
        "defaultValue": "Colors"
      },
      {
        "type": "select",
        "label": "Theme",
        "messageKey": "Theme",
        "capabilities": ["COLOR"],
        "defaultValue": "classic",
        "description": "Choose Custom to pick each color yourself.",
        "options": [
          { "label": "Classic", "value": "classic" },
          { "label": "Neon", "value": "neon" },
          { "label": "Ocean", "value": "ocean" },
          { "label": "Sunset", "value": "sunset" },
          { "label": "Lime", "value": "lime" },
          { "label": "Mono", "value": "mono" },
          { "label": "Paper", "value": "paper" },
          { "label": "Custom", "value": "custom" }
        ]
      },
      {
        type: 'color',
        capabilities: ['COLOR'],
        label: 'Background',
        messageKey: 'ColorBackground',
        defaultValue: '000000'
      },
      {
        type: 'color',
        capabilities: ['COLOR'],
        label: 'Hour/minutes hand',
        messageKey: 'ColorHourMinutes',
        defaultValue: 'AAAAAA'
      },
      {
        type: 'color',
        capabilities: ['COLOR'],
        label: 'Seconds hand',
        messageKey: 'ColorSeconds',
        defaultValue: 'AA0000'
      },
      {
        type: 'color',
        capabilities: ['COLOR'],
        label: 'Seconds hand tip',
        messageKey: 'ColorSecondTip',
        defaultValue: 'FFAA00'
      },
      {
        type: 'color',
        capabilities: ['COLOR'],
        label: 'Hour markers',
        messageKey: 'ColorNotches',
        defaultValue: 'FFFFFF'
      },
      {
        type: 'color',
        capabilities: ['COLOR'],
        label: 'Hour markers (empty battery)',
        messageKey: 'ColorBatteryEmpty',
        defaultValue: '555555'
      },
      {
        type: 'color',
        capabilities: ['COLOR'],
        label: 'Hand tips',
        messageKey: 'ColorHandTips',
        defaultValue: 'FFFFFF'
      },
      {
        type: 'color',
        capabilities: ['COLOR'],
        label: 'Center dot',
        messageKey: 'ColorCenterDot',
        defaultValue: 'FFFFFF'
      },
      {
        type: 'color',
        capabilities: ['COLOR'],
        label: 'Day of the month',
        messageKey: 'ColorMonthDay',
        defaultValue: 'FFAA00'
      },
      {
        type: 'color', capabilities: ['COLOR'], label: 'Hour markers (charging)',
        messageKey: 'ColorCharging', defaultValue: '00FF00'
      },
      {
        type: 'color', capabilities: ['COLOR', 'HEALTH'], label: 'Step goal ring',
        messageKey: 'ColorStepRing', defaultValue: 'FFFFFF'
      },
      {
        type: 'color', capabilities: ['COLOR'], label: 'Disconnected indicator',
        messageKey: 'ColorDisconnected', defaultValue: 'FF0000'
      },
      {
        type: 'color',
        capabilities: ['COLOR'],
        label: 'Date',
        messageKey: 'ColorDate',
        defaultValue: 'FFFFFF'
      }
    ]
  },
  {
    "type": "submit",
    "defaultValue": "Save"
  }
]
