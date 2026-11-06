# Week 07 — Lab report

**Name:** Yerassyl Arystanbek
**Group:** Monday 16:00–19:00 (as recorded in the repository README)
**Date:** 6 November 2026

AI disclosure: ChatGPT assisted with extraction, the test-plan draft and suggested X1/X2, test generation, review, the mutation runner, and drafting this report. These contributions are listed in AI_USAGE.md. Section 10 is reserved for the student's own conclusion.

Terminal evidence below reproduces the visible output of the supplied logs. ANSI colour-control sequences are omitted for Markdown display; test names, results, failures, timings and paths are unchanged. The original raw log files in evidence/ are preserved unchanged.

---

## 1. Setup

| | |
| --- | --- |
| Project I continue (`week-06` = my Week 06 Bolt project, `starter` = the provided starter) | week-06: local final project copied from week-06/prototype into week-07/app |
| Bolt project link (or `not shared`, and why) | not shared: the local Week 06 export was used; no share URL was supplied |
| Assistant that generated the tests (tool) | ChatGPT, in a separate conversation for the first suite and its improvement |
| Exact model (with its version, or `not displayed`) | not displayed |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | My Windows computer, CMD / VS Code terminal; Node v24.13.1 and Python 3.12.10 |
| Vitest version (the `RUN  v…` line of a run) | 5.1.0 |
| Test command | npx vitest run, from week-07/app |

---

## 2. Task 1 — baseline and the booking function

**Before editing:**

| | |
| --- | --- |
| File and function (or "inside the page component") | app/src/availability.ts, checkAvailability |
| Its inputs | Selected room (or null), candidate start and end minutes, supplied current time, and all existing bookings |
| What it returned | An AvailabilityResult containing available and a list of reasons |
| How the page used it | App.tsx called checkAvailability in handleCheck and rendered its result |

<!-- Write below this line -->

With ChatGPT assistance, I moved the Boolean booking rules into app/src/booking.ts as canBook. The page now imports and calls this real function. App.tsx filters bookings to the selected room before passing them to canBook. The existing time conversion and feedback formatting remain in availability.ts, whose feedback function is now getAvailabilityReasons. The bounds, supplied-time comparison, duration limit, blocked-room rejection and strict overlap comparisons were preserved. The production build and TypeScript check passed. Manual checks at now = 09:00 still returned Available for 11:00–12:00 and Unavailable for 10:30–11:30 against the 10:00–11:00 booking.

The baseline was committed before extraction: 25a648c. The extraction commit is 3463a4a. The normal page uses the real clock; ?test=1 fixes now to 540 and supplies the sample 600–660 booking for reproducible manual checks.

---

## 3. Task 2 — the test plan

Default fixture: `now = 540`, `blocked = false`, `bookings = [{ start: 600, end: 660 }]`. Each test uses fresh data unless its row specifies different bookings. Expected results come from the acceptance criteria.

AI assistance: ChatGPT drafted the reasons and suggested X1 and X2.

| ID | Candidate / changed input | Expected | AC | Reason (in your words) |
| --- | --- | --- | --- | --- |
| T01 | 660–720 (touching after) | true | AC4 | The existing booking ends at 660, exactly when the request starts. Touching endpoints are allowed. |
| T02 | 540–570 (starts now) | false | AC1 | The request starts at 540, equal to now. Its start must be strictly after now. |
| T03 | 720–720 (zero duration) | false | AC1 | Start and end are equal. AC1 requires start to be less than end. |
| T04 | 750–720 (reversed) | false | AC1 | The request ends before it starts, so the time order is invalid. |
| T05 | 1380–1441 (past day end) | false | AC1 | The end is 1441, which exceeds the maximum day boundary of 1440. |
| T06 | 720–840 (120 minutes) | true | AC2 | The duration is exactly 120 minutes. AC2 rejects only durations above 120, and this interval has no overlap. |
| T07 | 720–841 (121 minutes) | false | AC2 | The duration is 121 minutes, one minute above the allowed maximum. |
| T08 | 570–600 (touching before) | true | AC4 | The request ends at 600, exactly when the existing booking starts. They only touch. |
| T09 | 630–690 (partial overlap) | false | AC4 | Both intervals use the room from 630 to 660, so they overlap. |
| T10 | 570–690 (contains booking) | false | AC4 | The request contains the entire existing 600–660 booking. Those occupied minutes cannot be booked again. |
| T11 | 615–645 (inside booking) | false | AC4 | The whole request falls inside the existing 600–660 booking. |
| T12 | 600–660 (identical interval) | false | AC4 | The requested interval is identical to the existing booking, so every requested minute conflicts. |
| T13 | 660–720, blocked = true | false | AC3 | A blocked room must reject a request even when its times would otherwise be valid. |
| T14 | 630–690, bookings = [] | true | AC4 | There are no existing bookings to overlap. The request also satisfies the time and duration limits. |
| AC5 | 660–720; compare bookings with a deep copy taken before the call | true, data unchanged | AC5 | Checking an available interval must only read the schedule. The booking array and its objects must retain their original values. |
| X1 | 1380–1440; other inputs unchanged | true | AC1 | The request ends exactly at the allowed day boundary of 1440. Its duration is 60 minutes, it starts after now, and it has no overlap. |
| X2 | 720–780; bookings = [{ start: 600, end: 660 }, { start: 750, end: 810 }] | false | AC4 | The request misses the first booking but overlaps the second from 750 to 780. Every existing booking must be checked. |

---

## 4. Task 3 — the generation prompt and the first suite

The prompt exactly as sent:

```text
Generate tests for the existing booking function using Vitest. Use AC1–AC6 and the reviewed case table below.

Import the real function used by the page. Keep its code unchanged. Use fixed time and fresh fixtures. Assert exact decisions and unchanged booking data.

Return the test file, run command, and AC mapping. Flag unclear requirements. We will run the tests ourselves.
```


The reviewed table and booking.ts were supplied as attachments rather than repeated inline: README.md, lab-report(1).md and booking.ts were attached to the generation conversation.

The assistant's supplied answer, excluding its separate test-file attachment. Markdown layout is represented as text below:

```text
Contains **17 tests** with fixed time, fresh fixtures, exact Boolean expectations, and booking-data preservation checks. `booking.ts` is unchanged. **Tests have not been run.**

Save identical copies as:

- `week-07/suites/first/booking.test.ts`
- `week-07/app/src/booking.test.ts`

From the repository root, run:
cd week-07/app
npx vitest run

| Requirement | Coverage |
| --- | --- |
| AC1 — time validity | T02–T05, X1 |
| AC2 — duration limit | T06, T07 |
| AC3 — blocked room | T13 |
| AC4 — overlaps and touching | T01, T08–T12, T14, X2 |
| AC5 — unchanged booking data | All tests, including dedicated AC5 test |
| AC6 — layout and validation feedback | Requires manual page checks |

Unclear requirements: invalid existing bookings, nonfinite numbers, and fractional minutes have no specified expected behavior, so no expectations were invented for them.

Visible Available/Unavailable labels also need page checks. The suite imports the real `./booking` module; the page source was not supplied, so its use of that same function remains unverified.
```


The first suite was saved to suites/first/ before the working copy was changed: **yes**. It contains 17 tests. The immutable copy remains separate from app/src/booking.test.ts, which now contains 27 tests.

The generator initially could not verify the page's import because App.tsx was not attached to that conversation. The page was separately updated to import canBook from ./booking, built, typechecked and checked manually in this workflow.

---

## 5. Task 4 — review of the first suite

This review was completed with ChatGPT assistance before the first test run.

| # | Test or part of the suite | What is weak or wrong | Decision: accept / revise / reject | AC or reason |
| --- | --- | --- | --- | --- |
| 1 | T01–T14 expectations | No incorrect expectations found. Every case asserts the exact Boolean result required by the plan. | accept | AC1–AC4: expected values follow the criteria, including exactly 120 minutes and touching endpoints. |
| 2 | freshRequest and AC5 checks | No shared fixture or live clock found. Each test creates fresh data and compares bookings with a deep copy. | accept | AC5: the dedicated preservation test uses an Available request, which can reach the successful path. |
| 3 | Current-time coverage | T02 checks start equal to now, but no case checks a valid interval starting earlier than now. | revise | AC1: add a 539–570 request with now = 540, expected false. This detects a faulty check that rejects equality only. |
| 4 | Multiple-booking coverage | X2 checks an overlap with the second booking, but the bookings are sorted by start time. | revise | AC4: add an unsorted schedule whose first booking is later than the request and whose second booking overlaps it. This detects an incorrect early return based on booking order. |

---

## 6. Task 5 — running, diagnosing, improving

### 6.1 The first run

Real first-suite run: evidence/first-run.txt. This run contains 17 tests, all passing.

```text

 RUN  v5.1.0 C:/Users/777/Desktop/SE/software-engineering-practice/week-07/app

 ✓ src/booking.test.ts (17 tests) 4ms

 Test Files  1 passed (1)
      Tests  17 passed (17)
   Start at  23:39:06
   Duration  473ms (transform 55%, import 28%, worker 11%, tests 6%)
```


| Failing test | Observed failure | First check | Test repair or implementation fix? | Action taken |
| --- | --- | --- | --- | --- |
| none | 17 passed, 0 failed | Reviewed each expected decision against AC1–AC4 and the case table | No first-run repair or implementation fix | Preserve the first suite and improve coverage |

A separate discovery problem occurred later while installing the improved file: it was named booking.test (1).ts. Vitest reported No test files found because this name did not match its discovery pattern. Renaming it to booking.test.ts corrected discovery. This was a filename/setup repair; it did not change the first run's failure count or any expected decision.

### 6.2 The improvement prompt

Prompt as supplied in the test-generation conversation, with the actual first-run output:

```text
Review this test suite against AC1–AC6 and our case table. Identify incorrect expectations, weak assertions, duplicated cases, and missing boundaries.

For each proposed change, explain the requirement and the defect it could detect. Improve the tests without changing correct expectations to match buggy behavior.

Use the actual failure output below. Separate test repairs from implementation fixes.

 RUN  v5.1.0 C:/Users/777/Desktop/SE/software-engineering-practice/week-07/app

 Γ£ô src/booking.test.ts (17 tests) 4ms

 Test Files  1 passed (1)
      Tests  17 passed (17)
   Start at  23:39:06
   Duration  473ms (transform 55%, import 28%, worker 11%, tests 6%)
```


Assistant's supplied answer, excluding its separate improved test-file attachment:

```text
Your output shows **17 passed, 0 failed**. All original expectations match the case table. The suite already uses exact Boolean assertions, fresh fixtures, and independent booking snapshots.

The main duplication is **AC5 repeating T01’s inputs and assertions**. I revised AC5 and added boundary coverage.

The improved suite contains **27 tests**. T01–T14, X1, and X2 remain unchanged.

| Test improvement | Requirement | Defect it could detect |
| --- | --- | --- |
| AC5: unsorted bookings; check twice; expect `true` and unchanged data after each call | AC5 | In-place sorting, booking mutation, or state changes between calls |
| T15–T16: start one minute before/after now → `false` / `true` | AC1 | Accepting past requests or rejecting the first valid future minute |
| T17–T19: negative start, midnight equal to now, and a valid 1–2 interval → `false` / `false` / `true` | AC1 | Invalid early times being accepted or valid early bookings being rejected |
| T20–T21: one-minute overlaps at either endpoint → `false` | AC4 | Allowing small overlaps through rounding or tolerance |
| T22: first booking conflicts, second does not → `false` | AC4 | Checking only the last booking or overwriting an earlier conflict |
| T23: request touches two bookings in an unsorted schedule → `true` | AC4 | Rejecting a valid gap or depending on booking order |
| T24: blocked room with an empty schedule → `false` | AC3 | Checking the blocked flag only inside the booking loop |

T17 also violates the future-start rule, so it does **not independently prove** that the lower-bound guard works.

**Test repairs:** no incorrect expectations needed correction. Changes strengthen coverage and remove the redundant AC5 scenario.

**Implementation fixes:** none are justified by the supplied run or reviewed cases. `booking.ts` remains unchanged.

AC5’s visible labels and AC6’s layout/validation still require page checks. Invalid existing bookings, nonfinite times, and fractional minutes remain unspecified.

Save the improved file as `week-07/app/src/booking.test.ts`. Preserve `week-07/suites/first/booking.test.ts` unchanged. From `week-07/app`, run: npx vitest run

The improved suite has been statically reviewed but **has not been run**.
```


Accepted changes: retain the 16 original T01–T14 / X1 / X2 test bodies, strengthen the dedicated AC5 scenario, and add T15–T24. No correct expectation was changed. No implementation fix was made to canBook.

The original row 4 review also proposed a future-first schedule followed by an earlier conflicting booking. T22 and T23 add useful unsorted-schedule coverage, but that exact proposed ordering is still an additional coverage opportunity; it is not claimed as a completed test.

### 6.3 The final run

Real run after all three mutants were reverted: evidence/final-run.txt. The committed working suite must contain the same 27 tests as this run.

```text

 RUN  v5.1.0 C:/Users/777/Desktop/SE/software-engineering-practice/week-07/app

 ✓ src/booking.test.ts (27 tests) 7ms

 Test Files  1 passed (1)
      Tests  27 passed (27)
   Start at  17:36:18
   Duration  536ms (import 34%, transform 24%, worker 22%, tests 19%, environment 1%)
```


---

## 7. Task 6 — deliberate defects

The improved suite passed before mutation trials. The AI-assisted run_mutants.py introduced one specified defect at a time, ran the real Vitest command, saved each complete raw output, and restored the original booking.ts bytes in finally. It also checked that both suites remained unchanged during the trials. These are local runs, not predictions from a static review.

| Trial | Intentional change | Detected / Survived | Failing test ID(s) | If it survived: why, and what you added |
| --- | --- | --- | --- | --- |
| M1 | Reject duration >= 120 instead of > 120 | Detected | T06 | Did not survive: a relevant assertion failed for exactly 120 minutes |
| M2 | Treat touching endpoints as an overlap | Detected | T01, T08, T23 | Did not survive: relevant assertions failed for touching intervals |
| M3 | Remove the blocked-room rejection | Detected | T13, T24 | Did not survive: relevant assertions failed for blocked rooms |

M1 full output, from evidence/M1.txt:

```text

 RUN  v5.1.0 C:/Users/777/Desktop/SE/software-engineering-practice/week-07/app

 ❯ src/booking.test.ts (27 tests | 1 failed) 14ms
   ❯ canBook — reviewed booking cases (27)
     ✓ T01 AC4: allows touching after an existing booking 2ms
     ✓ T02 AC1: rejects a request starting exactly now 0ms
     ✓ T03 AC1: rejects zero duration 0ms
     ✓ T04 AC1: rejects an end before the start 0ms
     ✓ T05 AC1: rejects an end past minute 1440 0ms
     × T06 AC2: allows exactly 120 minutes 6ms
     ✓ T07 AC2: rejects 121 minutes 0ms
     ✓ T08 AC4: allows touching before an existing booking 0ms
     ✓ T09 AC4: rejects a partial overlap 0ms
     ✓ T10 AC4: rejects a request containing an existing booking 0ms
     ✓ T11 AC4: rejects a request inside an existing booking 0ms
     ✓ T12 AC4: rejects an identical interval 0ms
     ✓ T13 AC3: rejects a blocked room for an otherwise valid request 0ms
     ✓ T14 AC4: allows a valid request when there are no existing bookings 0ms
     ✓ AC5: repeated Available decisions preserve unsorted booking data 0ms
     ✓ X1 AC1: allows an end exactly at minute 1440 0ms
     ✓ X2 AC4: rejects an overlap with the second booking 0ms
     ✓ T15 AC1: rejects a request starting one minute before now 0ms
     ✓ T16 AC1: allows a request starting one minute after now 0ms
     ✓ T17 AC1: rejects a negative start minute 0ms
     ✓ T18 AC1: rejects minute zero when the supplied current time is zero 0ms
     ✓ T19 AC1: allows a one-minute booking just after midnight 0ms
     ✓ T20 AC4: rejects a one-minute overlap at the existing booking end 0ms
     ✓ T21 AC4: rejects a one-minute overlap at the existing booking start 0ms
     ✓ T22 AC4: rejects an earlier conflict despite a later nonconflicting booking 0ms
     ✓ T23 AC4: allows a gap touching both bookings in an unsorted schedule 0ms
     ✓ T24 AC3: rejects a blocked room even with no existing bookings 0ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T06 AC2: allows exactly 120 minutes
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:70:30
     68|     const before = structuredClone(request.bookings);
     69|
     70|     expect(canBook(request)).toBe(true);
       |                              ^
     71|     expect(request.bookings).toEqual(before);
     72|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯


 Test Files  1 failed (1)
      Tests  1 failed | 26 passed (27)
   Start at  17:36:10
   Duration  580ms (transform 47%, import 23%, tests 20%, worker 10%)
```


M2 full output, from evidence/M2.txt:

```text

 RUN  v5.1.0 C:/Users/777/Desktop/SE/software-engineering-practice/week-07/app

 ❯ src/booking.test.ts (27 tests | 3 failed) 12ms
   ❯ canBook — reviewed booking cases (27)
     × T01 AC4: allows touching after an existing booking 6ms
     ✓ T02 AC1: rejects a request starting exactly now 0ms
     ✓ T03 AC1: rejects zero duration 0ms
     ✓ T04 AC1: rejects an end before the start 0ms
     ✓ T05 AC1: rejects an end past minute 1440 0ms
     ✓ T06 AC2: allows exactly 120 minutes 0ms
     ✓ T07 AC2: rejects 121 minutes 0ms
     × T08 AC4: allows touching before an existing booking 1ms
     ✓ T09 AC4: rejects a partial overlap 0ms
     ✓ T10 AC4: rejects a request containing an existing booking 0ms
     ✓ T11 AC4: rejects a request inside an existing booking 0ms
     ✓ T12 AC4: rejects an identical interval 0ms
     ✓ T13 AC3: rejects a blocked room for an otherwise valid request 0ms
     ✓ T14 AC4: allows a valid request when there are no existing bookings 0ms
     ✓ AC5: repeated Available decisions preserve unsorted booking data 0ms
     ✓ X1 AC1: allows an end exactly at minute 1440 0ms
     ✓ X2 AC4: rejects an overlap with the second booking 0ms
     ✓ T15 AC1: rejects a request starting one minute before now 0ms
     ✓ T16 AC1: allows a request starting one minute after now 0ms
     ✓ T17 AC1: rejects a negative start minute 0ms
     ✓ T18 AC1: rejects minute zero when the supplied current time is zero 0ms
     ✓ T19 AC1: allows a one-minute booking just after midnight 0ms
     ✓ T20 AC4: rejects a one-minute overlap at the existing booking end 0ms
     ✓ T21 AC4: rejects a one-minute overlap at the existing booking start 0ms
     ✓ T22 AC4: rejects an earlier conflict despite a later nonconflicting booking 0ms
     × T23 AC4: allows a gap touching both bookings in an unsorted schedule 0ms
     ✓ T24 AC3: rejects a blocked room even with no existing bookings 0ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 3 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T01 AC4: allows touching after an existing booking
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:30:30
     28|     const before = structuredClone(request.bookings);
     29|
     30|     expect(canBook(request)).toBe(true);
       |                              ^
     31|     expect(request.bookings).toEqual(before);
     32|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/3]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T08 AC4: allows touching before an existing booking
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:86:30
     84|     const before = structuredClone(request.bookings);
     85|
     86|     expect(canBook(request)).toBe(true);
       |                              ^
     87|     expect(request.bookings).toEqual(before);
     88|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/3]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T23 AC4: allows a gap touching both bookings in an unsorted schedule
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:254:30
    252|     const before = structuredClone(request.bookings);
    253|
    254|     expect(canBook(request)).toBe(true);
       |                              ^
    255|     expect(request.bookings).toEqual(before);
    256|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/3]⎯


 Test Files  1 failed (1)
      Tests  3 failed | 24 passed (27)
   Start at  17:36:13
   Duration  631ms (transform 45%, import 20%, tests 20%, worker 14%)
```


M3 full output, from evidence/M3.txt:

```text

 RUN  v5.1.0 C:/Users/777/Desktop/SE/software-engineering-practice/week-07/app

 ❯ src/booking.test.ts (27 tests | 2 failed) 12ms
   ❯ canBook — reviewed booking cases (27)
     ✓ T01 AC4: allows touching after an existing booking 2ms
     ✓ T02 AC1: rejects a request starting exactly now 0ms
     ✓ T03 AC1: rejects zero duration 0ms
     ✓ T04 AC1: rejects an end before the start 0ms
     ✓ T05 AC1: rejects an end past minute 1440 0ms
     ✓ T06 AC2: allows exactly 120 minutes 0ms
     ✓ T07 AC2: rejects 121 minutes 0ms
     ✓ T08 AC4: allows touching before an existing booking 0ms
     ✓ T09 AC4: rejects a partial overlap 0ms
     ✓ T10 AC4: rejects a request containing an existing booking 0ms
     ✓ T11 AC4: rejects a request inside an existing booking 0ms
     ✓ T12 AC4: rejects an identical interval 0ms
     × T13 AC3: rejects a blocked room for an otherwise valid request 5ms
     ✓ T14 AC4: allows a valid request when there are no existing bookings 0ms
     ✓ AC5: repeated Available decisions preserve unsorted booking data 0ms
     ✓ X1 AC1: allows an end exactly at minute 1440 0ms
     ✓ X2 AC4: rejects an overlap with the second booking 0ms
     ✓ T15 AC1: rejects a request starting one minute before now 0ms
     ✓ T16 AC1: allows a request starting one minute after now 0ms
     ✓ T17 AC1: rejects a negative start minute 0ms
     ✓ T18 AC1: rejects minute zero when the supplied current time is zero 0ms
     ✓ T19 AC1: allows a one-minute booking just after midnight 0ms
     ✓ T20 AC4: rejects a one-minute overlap at the existing booking end 0ms
     ✓ T21 AC4: rejects a one-minute overlap at the existing booking start 0ms
     ✓ T22 AC4: rejects an earlier conflict despite a later nonconflicting booking 0ms
     ✓ T23 AC4: allows a gap touching both bookings in an unsorted schedule 0ms
     × T24 AC3: rejects a blocked room even with no existing bookings 1ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 2 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T13 AC3: rejects a blocked room for an otherwise valid request
AssertionError: expected true to be false // Object.is equality

- Expected
+ Received

- false
+ true

 ❯ src/booking.test.ts:126:30
    124|     const before = structuredClone(request.bookings);
    125|
    126|     expect(canBook(request)).toBe(false);
       |                              ^
    127|     expect(request.bookings).toEqual(before);
    128|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/2]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T24 AC3: rejects a blocked room even with no existing bookings
AssertionError: expected true to be false // Object.is equality

- Expected
+ Received

- false
+ true

 ❯ src/booking.test.ts:262:30
    260|     const before = structuredClone(request.bookings);
    261|
    262|     expect(canBook(request)).toBe(false);
       |                              ^
    263|     expect(request.bookings).toEqual(before);
    264|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/2]⎯


 Test Files  1 failed (1)
      Tests  2 failed | 25 passed (27)
   Start at  17:36:15
   Duration  586ms (transform 45%, import 20%, tests 20%, worker 14%)
```


All three changes reverted, and the full suite run again in section 6.3: **yes**. The runner recorded module_restored = true, first_suite_unchanged = true and final_suite_unchanged_during_trials = true in evidence/mutation-summary.json. All three detections were assertion failures, not import or syntax errors.

---

## 8. Task 7 — manual UI checks

The page was checked with ?test=1, now = 09:00 and the sample booking 10:00–11:00. Supplied screenshots are evidence/ui-1.png through evidence/ui-5.png. ChatGPT inspected the screenshots to help draft the observations. A still image records the resulting state rather than the full click history.

| # | Action | Expected observation | AC | What I observed | Pass / Fail / Not testable |
| --- | --- | --- | --- | --- | --- |
| U1 | Check 11:00–12:00, unblocked | Available, with the fixed sample booking | AC5 | ui-1 shows Thesis Hall selected, now 09:00, its 10:00–11:00 Test Booking and a green Available result for 11:00–12:00 | Pass |
| U2 | Enable blocked, then check again | Unavailable replaces the earlier result | AC3, AC5 | Selecting the existing blocked Faculty Lounge and checking 11:00–12:00 produced Unavailable with a message that this room is currently blocked; ui-2 | Pass |
| U3 | Clear a required input and submit | Understandable validation feedback | AC6 | With Start empty (--:--) and End 12:00, the page showed Enter valid times in HH:MM (24-hour) format; ui-3 | Pass |
| U4 | Use a narrow (phone) width | Controls and result remain usable | AC6 | The portrait captures show a single-column layout. ui-4 shows the upper page and room cards; ui-5 shows the lower form with readable fields, button and Available result | Pass |
| U5 | Repeat the checks on the same data | Existing bookings remain unchanged | AC5 | The supplied repeat-check capture ui-5 still shows Available for Thesis Hall at 11:00–12:00 and unchanged displayed sample booking data. The dedicated AC5 unit test independently verifies two consecutive calls preserve the booking array | Pass |

The narrow-layout evidence is split across ui-4 and ui-5; ui-4 alone does not show the entire checker form. The PNG sizes are 597×1275 and 538×1177 respectively. These are screenshot pixel dimensions, not a claim that the CSS viewport was that many pixels wide.

An observed UI limitation remains: the day-range helper label displays 00:00–00:00 because minutesToTime wraps 1440 to midnight. It should distinguish the end of the day as 24:00. This label issue does not change the Boolean decisions tested by canBook, and it has not been hidden or claimed as fixed.

---

## 9. Comparison and what still fails

### 9.1 Checks I am keeping as FAIL or ERROR

This table comes from the actual local checker run. Functional limitations that do not have a checker ID are discussed in sections 8 and 9.2.

| Check | Why it stays |
| --- | --- |
| none | The current local checker reported no FAIL or ERROR |

### 9.2 Original and improved suites

| Measure | First suite | Improved suite |
| --- | --- | --- |
| Executed / passed / failed | 17 / 17 / 0 in the first run | 27 / 27 / 0 after restoring all mutants |
| Requirements with meaningful tests (AC IDs and gaps) | AC1–AC5; fixed cases and data snapshots. AC6 and visible labels require page checks | AC1–AC5 with extra current-time, midnight, small-overlap and unsorted-data coverage. AC6 and visible labels were checked separately |
| Selected mutants detected | Not measured against the first suite; no detection count is claimed | 3/3 actually detected: M1 by T06; M2 by T01, T08, T23; M3 by T13, T24 |
| Accepted / revised / rejected tests | 16 original test bodies retained unchanged; AC5 selected for revision; 0 rejected | 16 retained + 1 revised AC5 + 10 added cases = 27; 0 rejected |
| Remaining limitations | AC5 duplicated T01 on a one-booking fixture; no explicit earlier-than-now case or one-minute overlap cases | T17 does not isolate the lower-bound guard. Invalid existing bookings, nonfinite times and fractions remain unspecified. More booking orders and viewport widths could be tested |

The review was AI-assisted, including the reasons and suggested X1/X2. No independent authorship is claimed for those drafts. The original suite had no incorrect Boolean expectation; its weaknesses concerned coverage and duplication. The UI end-of-day label remains a separate known limitation.

### 9.3 What no AC decides

The real probe used start = 660, end = 720, now = 540, blocked = false and bookings = [{ start: 700, end: 650 }]. It returned true, recorded unchanged in evidence/invalid-existing.txt and as returns-true in mutation-summary.json.

For this particular reversed existing booking, the overlap comparison 660 < 650 is false, so no conflict is reported. AC1 validates the candidate request; none of the ACs specifies validation of reversed existing records. This observed result is declared, not presented as a universal policy for all malformed bookings. A production system would need an explicit rule for rejecting or cleaning invalid existing data.

---

## 10. Conclusion (120–180 words)

<!-- Write this conclusion in your own words, as the assignment requires.
Use your actual evidence:
1. The first suite had no incorrect expectations, but AC5 duplicated T01 and a start earlier than now was not covered. Explain one wrong implementation that such a gap could miss.
2. The final 27-test run and three detected mutants support the tested rules. Explain why this does not prove every input or every UI layout is correct.
3. Name one remaining limitation, such as unspecified invalid existing bookings, the non-isolated T17 lower-bound test, or the visible 00:00–00:00 label.
Do not copy these notes as the conclusion. Add 120–180 words below this comment, then rerun sync_submission.py.
-->

Passing tests provide useful evidence, but they do not prove that a program is correct. The first AI-generated suite contained 17 tests, and all of them passed. After review, the improved suite contained 27 tests with additional time boundaries, overlap cases, and checks that booking data stays unchanged.

The mutation trials provided stronger evidence. The tests detected all three deliberate defects: rejecting a booking of exactly 120 minutes, treating touching endpoints as overlapping, and accepting a blocked room. After restoring the original implementation, all 27 tests passed again.

Manual page checks also covered successful requests, blocked rooms, empty input, and a narrow layout. However, the page still displays a confusing day range, and some inputs remain outside the stated requirements. One negative-start test also violates another rule, so it does not isolate the lower-bound check.

The suite therefore supports confidence in the tested requirements. AI-generated tests still need review against the acceptance criteria, with documented gaps and honest reporting.
