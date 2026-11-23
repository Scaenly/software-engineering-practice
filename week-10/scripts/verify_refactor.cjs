// Differential check against the real checkpoint, without changing the Vitest suite.
const { createRequire } = require('node:module');
const { execFileSync } = require('node:child_process');
const { mkdtempSync, writeFileSync, rmSync } = require('node:fs');
const { tmpdir } = require('node:os');
const path = require('node:path');
const assert = require('node:assert/strict');
const app = path.resolve(__dirname, '../app');
const requireApp = createRequire(path.join(app, 'package.json'));
const esbuild = requireApp('esbuild');
const baseline = '0ca9e73';
const temp = mkdtempSync(path.join(tmpdir(), 'week10-refactor-'));

function load(file) {
  const output = esbuild.buildSync({ entryPoints: [file], bundle: true, write: false, format: 'cjs', platform: 'node' });
  const module = { exports: {} };
  new Function('module', 'exports', output.outputFiles[0].text)(module, module.exports);
  return module.exports;
}

try {
  for (const name of ['booking.ts', 'availability.ts']) {
    const source = execFileSync('git', ['show', `${baseline}:week-10/app/src/${name}`], { cwd: app, encoding: 'utf8' });
    writeFileSync(path.join(temp, name), source);
  }
  const before = load(path.join(temp, 'booking.ts'));
  const after = load(path.join(app, 'src/booking.ts'));
  const oldReasons = load(path.join(temp, 'availability.ts')).getAvailabilityReasons;
  const newReasons = load(path.join(app, 'src/availability.ts')).getAvailabilityReasons;
  const values = [NaN, -1, 0, 1, 539, 540, 541, 570, 599, 600, 601, 659, 660, 661, 719, 720, 721, 840, 841, 1439, 1440, 1441, Infinity];
  const schedules = [[], [{ start: 600, end: 660 }], [{ start: 720, end: 780 }, { start: 600, end: 660 }]];
  let decisions = 0;
  let feedback = 0;
  for (const start of values) for (const end of values) for (const now of [NaN, 0, 540, 660, 1439]) {
    for (const blocked of [false, true]) for (const bookings of schedules) {
      const request = { start, end, now, blocked, bookings };
      const original = structuredClone(request);
      assert.equal(after.canBook(request), before.canBook(request));
      assert.deepEqual(request, original);
      decisions++;
      if ([start, end, now].every(Number.isFinite)) {
        const room = { id: 'demo', name: 'Demo Room', building: 'Demo', capacity: 12, blocked };
        const data = bookings.map((b, i) => ({ ...b, id: `b${i}`, roomId: room.id, title: 'Fictional' }));
        assert.deepEqual(newReasons(room, start, end, now, data), oldReasons(room, start, end, now, data));
        feedback++;
      }
    }
  }
  console.log(`PASS: ${decisions} canBook decisions match checkpoint ${baseline}; fixtures unchanged.`);
  console.log(`PASS: ${feedback} finite-input feedback results match checkpoint ${baseline}.`);
  console.log('The intentional correction is invalid numeric feedback (R1); no valid UI behavior changed.');
} finally {
  rmSync(temp, { recursive: true, force: true });
}
