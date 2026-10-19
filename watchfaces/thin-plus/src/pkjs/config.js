// Values must match SlotType in src/c/modules/data.h
var slotOptions = [
  { "label": "None", "value": "0" },
  { "label": "Steps", "value": "1" },
  { "label": "Heart rate", "value": "2" },
  { "label": "Battery", "value": "3" },
  { "label": "Digital time", "value": "4" }
];

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
        "type": "toggle",
        "label": "Show battery level (hour markers)",
        "messageKey": "EnableBattery",
        "description": "Hour marks around the edge dim as the battery drains. Turn off to keep every mark in its normal color.",
        "defaultValue": true
      },
      {
        "type": "toggle",
        "label": "Show second hand (for 15s after a wrist flick)",
        "messageKey": "EnableSecondHand",
        "defaultValue": true
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
      {
        "type": "select",
        "label": "Top",
        "messageKey": "SlotTop",
        "defaultValue": "0",
        "options": slotOptions
      },
      {
        "type": "select",
        "label": "Left",
        "messageKey": "SlotLeft",
        "defaultValue": "0",
        "options": slotOptions
      },
      {
        "type": "select",
        "label": "Bottom",
        "messageKey": "SlotBottom",
        "defaultValue": "1",
        "options": slotOptions
      },
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
        label: 'Background',
        messageKey: 'ColorBackground',
        defaultValue: '000000'
      },
      {
        type: 'color',
        label: 'Hour/minutes hand',
        messageKey: 'ColorHourMinutes',
        defaultValue: 'AAAAAA'
      },
      {
        type: 'color',
        label: 'Seconds hand',
        messageKey: 'ColorSeconds',
        defaultValue: 'AA0000'
      },
      {
        type: 'color',
        label: 'Seconds hand tip',
        messageKey: 'ColorSecondTip',
        defaultValue: 'FFAA00'
      },
      {
        type: 'color',
        label: 'Hour markers',
        messageKey: 'ColorNotches',
        defaultValue: 'FFFFFF'
      },
      {
        type: 'color',
        label: 'Hour markers (empty battery)',
        messageKey: 'ColorBatteryEmpty',
        defaultValue: '555555'
      },
      {
        type: 'color',
        label: 'Hand tips',
        messageKey: 'ColorHandTips',
        defaultValue: 'FFFFFF'
      },
      {
        type: 'color',
        label: 'Center dot',
        messageKey: 'ColorCenterDot',
        defaultValue: 'FFFFFF'
      },
      {
        type: 'color',
        label: 'Day of the month',
        messageKey: 'ColorMonthDay',
        defaultValue: 'FFAA00'
      },
      {
        type: 'color',
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
