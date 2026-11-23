# Smart Campus availability demo

One fictional room, fictional bookings, no login or database. All data is local
and read-only. Do not add credentials or deploy this classroom prototype.

Use Node 22.12+ or Node 24 and Python 3.8+. From this directory:

```text
npm ci
npm test
npm run typecheck
npm run lint
npm run build
npm run dev
```

Open the local URL printed by Vite. For repeatable checks, append `?test=1`:
the simulated current time is 09:00, and the fictional booking is 10:00–11:00.
For example, 11:00–12:00 is Available and 10:30–11:30 is Unavailable.
The normal URL uses the browser's local clock. The simulation is not an access
control mechanism, and the page does not create or persist bookings.

- `src/App.tsx`: input state, browser clock and feedback rendering.
- `src/bookingRules.ts`: shared pure interval, time, duration and overlap rules.
- `src/booking.ts`: public `canBook(request): boolean`; no mutation.
- `src/availability.ts`: time conversion and explanations using the shared rules.
- `src/sampleData.ts`: the one-room fictional fixture.
- `src/booking.test.ts`: 29 inherited cases and the R1 regression, 30 tests total.
- `AGENTS.md`: constraints and acceptance gate; read it explicitly before editing.

AC1 rejects start ≥ end or start ≤ now. AC2 caps duration at 120 minutes. AC3
rejects a blocked room. AC4 allows touching endpoints and rejects overlaps. AC5
preserves input data and labels the decision. AC6 requires clear desktop/mobile
feedback.

Attach the changed-file diff, full test output, typecheck/lint/build output and
a review note to each proposed agent change. Local checks are required; no CI
workflow or hooks are provided. An old result can remain visible when the live
clock changes: run the check again before relying on it (R5 in the report).
