// Runs inside the config page (serialized by Clay), so it must be self-contained ES5
module.exports = function() {
  var clayConfig = this;

  var COLOR_KEYS = [
    'ColorBackground',
    'ColorHourMinutes',
    'ColorSeconds',
    'ColorNotches',
    'ColorMonthDay',
    'ColorDate',
    'ColorHandTips',
    'ColorCenterDot',
    'ColorSecondTip',
    'ColorBatteryEmpty',
    'ColorDisconnected',
    'ColorCharging',
    'ColorStepRing'
  ];

  // Same order as COLOR_KEYS
  var THEMES = {
    classic: ['000000', 'AAAAAA', 'AA0000', 'FFFFFF', 'FFAA00', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFAA00', '555555', 'FF0000', '00FF00', 'FFFFFF'],
    neon: ['000000', '00FFFF', 'FF00FF', 'FFFFFF', 'FFFF00', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFF00', '555555', 'FF0000', '00FFAA', '00FFFF'],
    ocean: ['0000AA', '55FFFF', 'FFAA00', 'FFFFFF', 'FFFF00', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFF00', '555555', 'FF0000', '55FFAA', '55FFFF'],
    sunset: ['550000', 'FFAA00', 'FF5500', 'FFFFFF', 'FFFF00', 'FFAA55', 'FFFFFF', 'FFFFFF', 'FFFF00', '555555', 'FF0000', 'AAFF00', 'FFAA00'],
    lime: ['000000', '55FF00', 'FF0055', 'FFFFFF', 'AAFF00', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'AAFF00', '555555', 'FF0000', '55FF00', '55FF00'],
    mono: ['000000', 'AAAAAA', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFFFF', '555555', 'FF0000', 'FFFFFF', 'FFFFFF'],
    paper: ['FFFFFF', '555555', 'FF0000', '000000', '0000FF', '000000', '000000', '000000', '0000FF', 'AAAAAA', 'FF0000', '005500', '555555']
  };

  clayConfig.on(clayConfig.EVENTS.AFTER_BUILD, function() {
    var goalMode = clayConfig.getItemByMessageKey('StepGoalMode');
    var customGoal = clayConfig.getItemByMessageKey('CustomStepGoal');
    if (goalMode && customGoal) {
      var lastValidGoal = customGoal.get();
      var validGoal = function(value) {
        return /^[0-9]+$/.test(String(value)) && Number(value) >= 1000 && Number(value) <= 100000;
      };
      if (!validGoal(lastValidGoal)) lastValidGoal = '7500';
      var validateGoal = function() {
        var valid = validGoal(customGoal.get());
        if (valid) lastValidGoal = customGoal.get();
        // Native form validation also blocks decimal/exponent spellings.
        var input = customGoal.$manipulatorTarget[0];
        input.setCustomValidity(valid ? '' : 'Enter a whole number from 1,000 to 100,000.');
      };
      var updateGoalVisibility = function() {
        if (String(goalMode.get()) === '1') customGoal.show();
        else {
          // Discard an invalid, unsaved edit before hiding the field.
          if (!validGoal(customGoal.get())) customGoal.set(lastValidGoal);
          customGoal.hide();
        }
        validateGoal();
      };
      customGoal.on('input change', validateGoal);
      goalMode.on('change', updateGoalVisibility);
      updateGoalVisibility();
    }
    // Date controls also apply on monochrome pages, before the theme early return.
    var dateEnabled = clayConfig.getItemByMessageKey('EnableDate');
    var dateStyle = clayConfig.getItemByMessageKey('DateStyle');
    if (dateEnabled && dateStyle) {
      var updateDateVisibility = function() {
        if (dateEnabled.get()) dateStyle.show();
        else dateStyle.hide();
      };
      dateEnabled.on('change', updateDateVisibility);
      updateDateVisibility();
    }
    var themeItem = clayConfig.getItemByMessageKey('Theme');
    if (!themeItem) return; // BW pages contain neither Theme nor color pickers.
    var colorItems = COLOR_KEYS.map(function(key) {
      return clayConfig.getItemByMessageKey(key);
    });

    // Newer keys are skipped, settings saved before they existed hold the default
    var NEWER_KEYS = ['ColorHandTips', 'ColorCenterDot', 'ColorSecondTip', 'ColorBatteryEmpty', 'ColorDisconnected', 'ColorCharging', 'ColorStepRing'];

    function matchesTheme(colors) {
      return colorItems.every(function(item, i) {
        return !item || NEWER_KEYS.indexOf(COLOR_KEYS[i]) >= 0 || item.get() === parseInt(colors[i], 16);
      });
    }

    function applyTheme(colors) {
      colorItems.forEach(function(item, i) {
        if (item) item.set(colors[i]);
      });
    }

    function updateVisibility() {
      var custom = !THEMES[themeItem.get()];
      colorItems.forEach(function(item) {
        if (!item) return;
        if (custom) {
          item.show();
        } else {
          item.hide();
        }
      });
    }

    themeItem.on('change', function() {
      var colors = THEMES[themeItem.get()];
      if (colors) {
        applyTheme(colors);
      }
      updateVisibility();
    });

    // Colors saved before themes existed may not match the selected theme
    var colors = THEMES[themeItem.get()];
    if (colors && !matchesTheme(colors)) {
      themeItem.set('custom');
    }
    // Opening settings must not overwrite saved individual colors. Presets are
    // applied only after the user chooses a theme.
    updateVisibility();
  });
};
