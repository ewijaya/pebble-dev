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
        "defaultValue": true
      },
      {
        "type": "toggle",
        "label": "Show second hand (for 15s after a wrist flick)",
        "messageKey": "EnableSecondHand",
        "defaultValue": true
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
        label: 'Notches',
        messageKey: 'ColorNotches',
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
