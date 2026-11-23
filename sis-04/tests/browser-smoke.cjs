// Optional evidence runner: requires Playwright + a Chromium executable.
// Start app/ on port 5173, then NODE_PATH=<modules> node tests/browser-smoke.cjs.
const { createRequire } = require('node:module');
const { chromium } = createRequire(require('node:path').join(__dirname, '..', 'app', 'package.json'))('playwright');
const assert = require('node:assert/strict');
const path = require('node:path');

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 960 } });
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  const evidence = path.join(__dirname, '..', 'evidence');
  await page.goto('http://127.0.0.1:5173');
  await page.getByRole('heading', { name: 'Smart Campus Room Availability' }).waitFor();
  await page.getByRole('spinbutton', { name: 'Attendees' }).fill('24');
  await page.getByRole('checkbox', { name: 'projector', exact: true }).check();
  await page.getByRole('checkbox', { name: 'whiteboard', exact: true }).check();
  assert.equal(await page.getByRole('button', { name: /seats/ }).count(), 2);
  assert.equal(await page.getByRole('button', { name: /Thesis Hall/ }).count(), 1);
  assert.equal(await page.getByRole('button', { name: /Innovation Lab/ }).count(), 1);
  await page.screenshot({ path: path.join(evidence, 'filter-match.png'), fullPage: true });
  console.log('PASS F1 F2: 24 attendees + projector + whiteboard -> Thesis Hall and Innovation Lab.');

  await page.getByRole('spinbutton', { name: 'Attendees' }).fill('300');
  await page.getByRole('heading', { name: 'No rooms match' }).waitFor();
  assert.equal(await page.getByRole('button', { name: 'Check availability' }).isDisabled(), true);
  await page.screenshot({ path: path.join(evidence, 'filter-empty.png'), fullPage: true });
  console.log('PASS F4: 300 attendees -> No rooms match; availability button disabled.');

  await page.getByRole('spinbutton', { name: 'Attendees' }).fill('1');
  await page.getByRole('checkbox', { name: 'projector', exact: true }).uncheck();
  await page.getByRole('checkbox', { name: 'whiteboard', exact: true }).uncheck();
  await page.getByRole('button', { name: /Thesis Hall/ }).click();
  await page.getByRole('button', { name: 'Check availability' }).click();
  await page.getByText('Available — this slot is free.', { exact: true }).waitFor();
  await page.screenshot({ path: path.join(evidence, 'switch-a.png'), fullPage: true });
  await page.getByRole('button', { name: /Innovation Lab/ }).click();
  await page.getByText('Unavailable — this slot cannot be booked.', { exact: true }).waitFor();
  assert.match(await page.getByRole('status').innerText(), /Innovation Lab.*10:00–11:00/);
  await page.screenshot({ path: path.join(evidence, 'switch-b.png'), fullPage: true });
  console.log('PASS F5: same 10:00-11:00; Thesis Hall Available -> Innovation Lab Unavailable without resubmitting.');

  await page.getByRole('button', { name: /Faculty Lounge/ }).click();
  await page.getByText('Unavailable — this slot cannot be booked.', { exact: true }).waitFor();
  assert.match(await page.getByRole('status').innerText(), /Faculty Lounge/);
  console.log('PASS F3: blocked Faculty Lounge remains Unavailable.');
  await page.getByRole('spinbutton', { name: 'Attendees' }).fill('31');
  assert.equal(await page.getByRole('status').count(), 0);
  assert.equal(await page.getByRole('button', { name: /Thesis Hall/ }).getAttribute('aria-pressed'), 'true');
  console.log('PASS selection: filtering out selected room clears feedback and chooses a visible room.');

  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole('spinbutton', { name: 'Attendees' }).fill('8');
  await page.getByRole('checkbox', { name: 'whiteboard', exact: true }).check();
  await page.getByRole('button', { name: /Thesis Hall/ }).click();
  await page.getByRole('button', { name: 'Check availability' }).click();
  await page.getByText('Available — this slot is free.', { exact: true }).waitFor();
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
  await page.screenshot({ path: path.join(evidence, 'narrow.png'), fullPage: true });
  console.log('PASS AC6: 390px portrait, visible form/result and no horizontal overflow.');
  assert.deepEqual(errors, []);
  console.log('PASS browser console: no page errors. Five screenshots captured from the running app.');
  await browser.close();
})().catch(error => { console.error(error); process.exitCode = 1; });
