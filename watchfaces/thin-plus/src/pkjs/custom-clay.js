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
    'ColorBatteryEmpty'
  ];

  // Same order as COLOR_KEYS
  var THEMES = {
    classic: ['000000', 'AAAAAA', 'AA0000', 'FFFFFF', 'FFAA00', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFAA00', '555555'],
    neon: ['000000', '00FFFF', 'FF00FF', 'FFFFFF', 'FFFF00', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFF00', '555555'],
    ocean: ['0000AA', '55FFFF', 'FFAA00', 'FFFFFF', 'FFFF00', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFF00', '555555'],
    sunset: ['550000', 'FFAA00', 'FF5500', 'FFFFFF', 'FFFF00', 'FFAA55', 'FFFFFF', 'FFFFFF', 'FFFF00', '555555'],
    lime: ['000000', '55FF00', 'FF0055', 'FFFFFF', 'AAFF00', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'AAFF00', '555555'],
    mono: ['000000', 'AAAAAA', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFFFF', 'FFFFFF', '555555'],
    paper: ['FFFFFF', '555555', 'FF0000', '000000', '0000FF', '000000', '000000', '000000', '0000FF', 'AAAAAA']
  };

  clayConfig.on(clayConfig.EVENTS.AFTER_BUILD, function() {
    var themeItem = clayConfig.getItemByMessageKey('Theme');
    var colorItems = COLOR_KEYS.map(function(key) {
      return clayConfig.getItemByMessageKey(key);
    });

    // Newer keys are skipped, settings saved before they existed hold the default
    var NEWER_KEYS = ['ColorHandTips', 'ColorCenterDot', 'ColorSecondTip', 'ColorBatteryEmpty'];

    function matchesTheme(colors) {
      return colorItems.every(function(item, i) {
        return NEWER_KEYS.indexOf(COLOR_KEYS[i]) >= 0 || item.get() === parseInt(colors[i], 16);
      });
    }

    function applyTheme(colors) {
      colorItems.forEach(function(item, i) {
        item.set(colors[i]);
      });
    }

    function updateVisibility() {
      var custom = !THEMES[themeItem.get()];
      colorItems.forEach(function(item) {
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
    } else if (colors) {
      applyTheme(colors);
    }
    updateVisibility();
  });
};
