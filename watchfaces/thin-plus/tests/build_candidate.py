#!/usr/bin/env python3
"""Build a checkpoint in isolation, preserving the published build/ PBW."""
from pathlib import Path
import argparse, hashlib, json, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('stage')
parser.add_argument('--release', default='1.2.0')
parser.add_argument('--fixed-step-goal', type=int, help='Scratch-only simulated goal for design comparisons')
parser.add_argument('--glyph', action='store_true', help='Build the alternate disconnect design in the scratch copy only')
args = parser.parse_args()
out = ROOT/'dist/verification'/args.release/args.stage
out.mkdir(parents=True, exist_ok=True)
scratch = Path(tempfile.mkdtemp(prefix='thin-plus-'+args.release+'-'))
subprocess.run(['rsync', '-a', '--exclude', 'build', '--exclude', 'dist',
                '--exclude', '.lock-waf*',
                '--exclude', 'node_modules', '--exclude', 'store', '--exclude', 'marketing',
                str(ROOT)+'/', str(scratch)+'/'], check=True)
(scratch/'node_modules').symlink_to(ROOT/'node_modules', target_is_directory=True)
if args.glyph:
    source = scratch/'src/c/windows/main_window.c'
    source.write_text(source.read_text().replace(
        'graphics_fill_circle(ctx, center, center_radius);',
        'graphics_fill_circle(ctx, center, center_radius);\n// Alternate disconnect design review insertion point.').replace(
        '// Alternate disconnect design review insertion point.',
        (ROOT/'tests/fixtures/disconnect-glyph.inc').read_text()))
if args.fixed_step_goal is not None:
    assert args.fixed_step_goal > 0
    source = scratch/'src/c/modules/health.c'
    source.write_text(source.read_text().replace('int health_get_step_goal(void) {',
        'int health_get_step_goal(void) { return '+str(args.fixed_step_goal)+'; // TEMP_TEST simulated design goal\n'))
with (out/'build.log').open('w') as log:
    for command in [['pebble', 'clean'], ['pebble', 'build']]:
        subprocess.run(command, cwd=scratch, stdout=log, stderr=subprocess.STDOUT, check=True)
pbw = out/'thin-plus.pbw'
pbw.write_bytes(next((scratch/'build').glob('*.pbw')).read_bytes())
(out/'build-context.json').write_text(json.dumps({'scratch':str(scratch), 'pbw':str(pbw),
    'sha256':hashlib.sha256(pbw.read_bytes()).hexdigest(),
    'tool':'5.0.40', 'sdk':'4.33.1', 'stage':args.stage, 'simulated_step_goal':args.fixed_step_goal}, indent=2)+'\n')
print('Built all seven platforms: '+str(pbw))
