// Values must match SlotType in src/c/modules/data.h
var slotOptions = [
  { "label": "None", "value": "0" },
  { "label": "Steps", "value": "1" },
  { "label": "Heart rate", "value": "2" },
  { "label": "Battery", "value": "3" },
  { "label": "Digital time", "value": "4" }
];

function slotSelect(label, key, value, health) {
  return {
    type: 'select', label: label, messageKey: key, defaultValue: value,
    capabilities: [health ? 'HEALTH' : 'NOT_HEALTH'],
    options: health ? slotOptions : slotOptions.filter(function(option) {
      return option.value !== '1' && option.value !== '2';
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
