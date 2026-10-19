// Validate before Clay can persist or truncate a numeric value for AppMessage.
exports.validate = function(raw) {
  [['StepGoalMode', 0, 1], ['CustomStepGoal', 1000, 100000]].forEach(function(spec) {
    if (!Object.prototype.hasOwnProperty.call(raw, spec[0])) return;
    var entry = raw[spec[0]];
    var value = entry && typeof entry === 'object' ? entry.value : entry;
    if ((typeof value !== 'string' && typeof value !== 'number') ||
        !/^[0-9]+$/.test(String(value)) || Number(value) < spec[1] || Number(value) > spec[2] ||
        (entry && typeof entry === 'object' && entry.precision)) {
      throw new Error('Invalid ' + spec[0] + '; saved settings were kept.');
    }
    // Goal mode remains a select string; the target is always an int32 on wire.
    raw[spec[0]] = spec[0] === 'CustomStepGoal' ? Number(value) : String(Number(value));
  });
  return raw;
};
