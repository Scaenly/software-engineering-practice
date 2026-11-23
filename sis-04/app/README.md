# Smart Campus room catalog

Fictional room data, a fixed demo clock of 09:00, and read-only availability checks.

```sh
npm install
npm run dev
npx vitest run
npm run typecheck
npm run lint
npm run build
```

Enter a positive integer number of attendees and choose required equipment. All selected
items must be present. Blocked rooms stay visible and cannot be available. Select a room,
enter times and check availability. After a check, selecting another room recomputes the
result immediately. Filter or time edits clear previous feedback.

Catalog data lives in `src/rooms.ts`, filtering in `src/filter.ts`, and availability in
`src/booking.ts`. `src/availability.ts` only parses/formats times. The UI calls these modules.

The suite uses Vitest, Testing Library and jsdom with independent fixtures; no mocks.
The original 29 Week 08 cases are retained, plus 14 catalog cases and three UI cases.

To capture the five screenshots on a computer with Chromium support, keep the development
server running on port 5173. In another terminal, from `app/`:

```sh
npx playwright install chromium
node ../tests/browser-smoke.cjs
```

The runner checks the page and writes five PNGs to `../evidence/`. To use an existing browser,
set `CHROMIUM_PATH` to its executable. The initial local workspace could not launch Chromium. The committed captures were obtained
in GitHub Actions with the runner's installed Chrome; the successful output and provenance are
in ../evidence/. jsdom tests alone do not prove mobile layout.
