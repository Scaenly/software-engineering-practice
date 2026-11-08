# Week 08 — Lab report

**Name:** Yerassyl Arystanbek
**Group:** Monday 16:00–19:00 (from Week 07 report)
**Date:** 8 November 2026

AI preparation disclosure: Codex copied the actual Week 07 project, ran the terminal commands, added the two regression tests, applied the two patches, and drafted factual report material. Student-only activities remain explicitly incomplete; no fresh-chat comparison or skill installation is claimed.

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Assistant I debugged with (tool) | |
| Exact model (with its version, or `not displayed`) | |
| Where the skill was installed (ChatGPT / Claude web / Claude Code / prompt-only simulation) | |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | |
| Vitest version (the `RUN  v…` line of a run) | |
| Language of my booking module (`ts` or `js`) — the file I copied from `buggy/` | |

---

## 2. Task 1 — baseline, buggy code, failing tests

### 2.1 My Week 07 suite on my own code

The **real** output of your Week 07 suite, run in `week-08/app/` **before** you replace
anything. It should be green. If it is not, say why under the block.

```text

 RUN  v5.1.0 /workspace/scratch/5290b5ee4677/repo/week-08/app


 Test Files  1 passed (1)
      Tests  27 passed (27)
   Start at  17:50:24
   Duration  265ms (transform 63%, import 16%, tests 14%, worker 6%, environment 1%)
```

### 2.2 The same suite on the provided canBook

You copied the whole `canBook` function from `buggy/booking.ts` (or `.js`) over yours and changed
nothing else. This is the real output:

```text

 RUN  v5.1.0 /workspace/scratch/5290b5ee4677/repo/week-08/app

 ❯ src/booking.test.ts (27 tests | 9 failed) 21ms
   ❯ canBook — reviewed booking cases (27)
     × T01 AC4: allows touching after an existing booking 7ms
     × T06 AC2: allows exactly 120 minutes 3ms
     × T08 AC4: allows touching before an existing booking 1ms
     × T14 AC4: allows a valid request when there are no existing bookings 1ms
     × AC5: repeated Available decisions preserve unsorted booking data 2ms
     × X1 AC1: allows an end exactly at minute 1440 1ms
     × T16 AC1: allows a request starting one minute after now 0ms
     × T19 AC1: allows a one-minute booking just after midnight 0ms
     × T23 AC4: allows a gap touching both bookings in an unsorted schedule 1ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 9 ⎯⎯⎯⎯⎯⎯⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/9]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T06 AC2: allows exactly 120 minutes
AssertionError: expected [ { start: 600, end: 660 }, …(1) ] to deeply equal [ { start: 600, end: 660 } ]

- Expected
+ Received

  [
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 840,
+     "start": 720,
+   },
  ]

 ❯ src/booking.test.ts:71:30
     69|
     70|     expect(canBook(request)).toBe(true);
     71|     expect(request.bookings).toEqual(before);
       |                              ^
     72|   });
     73|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/9]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/9]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T14 AC4: allows a valid request when there are no existing bookings
AssertionError: expected [ { start: 630, end: 690 } ] to deeply equal []

- Expected
+ Received

- []
+ [
+   {
+     "end": 690,
+     "start": 630,
+   },
+ ]

 ❯ src/booking.test.ts:135:30
    133|
    134|     expect(canBook(request)).toBe(true);
    135|     expect(request.bookings).toEqual(before);
       |                              ^
    136|   });
    137|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[4/9]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > AC5: repeated Available decisions preserve unsorted booking data
AssertionError: expected [ { start: 900, end: 960 }, …(2) ] to deeply equal [ { start: 900, end: 960 }, …(1) ]

- Expected
+ Received

@@ -5,6 +5,10 @@
    },
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 870,
+     "start": 810,
+   },
  ]

 ❯ src/booking.test.ts:149:30
    147|
    148|     expect(canBook(request)).toBe(true);
    149|     expect(request.bookings).toEqual(before);
       |                              ^
    150|     expect(canBook(request)).toBe(true);
    151|     expect(request.bookings).toEqual(before);

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[5/9]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > X1 AC1: allows an end exactly at minute 1440
AssertionError: expected [ { start: 600, end: 660 }, …(1) ] to deeply equal [ { start: 600, end: 660 } ]

- Expected
+ Received

  [
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 1440,
+     "start": 1380,
+   },
  ]

 ❯ src/booking.test.ts:159:30
    157|
    158|     expect(canBook(request)).toBe(true);
    159|     expect(request.bookings).toEqual(before);
       |                              ^
    160|   });
    161|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[6/9]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T16 AC1: allows a request starting one minute after now
AssertionError: expected [ { start: 600, end: 660 }, …(1) ] to deeply equal [ { start: 600, end: 660 } ]

- Expected
+ Received

  [
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 570,
+     "start": 541,
+   },
  ]

 ❯ src/booking.test.ts:188:30
    186|
    187|     expect(canBook(request)).toBe(true);
    188|     expect(request.bookings).toEqual(before);
       |                              ^
    189|   });
    190|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[7/9]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T19 AC1: allows a one-minute booking just after midnight
AssertionError: expected [ { start: 1, end: 2 } ] to deeply equal []

- Expected
+ Received

- []
+ [
+   {
+     "end": 2,
+     "start": 1,
+   },
+ ]

 ❯ src/booking.test.ts:213:30
    211|
    212|     expect(canBook(request)).toBe(true);
    213|     expect(request.bookings).toEqual(before);
       |                              ^
    214|   });
    215|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[8/9]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[9/9]⎯


 Test Files  1 failed (1)
      Tests  9 failed | 18 passed (27)
   Start at  17:50:39
   Duration  262ms (transform 42%, tests 35%, import 16%, worker 7%)
```

### 2.3 One failing test per bug

Add the two regression tests from README Part 1, step 5: one named `BUG-A` and one named `BUG-B`.
Run them **on the buggy code**. Both must fail here. That is the evidence that each test can see
its bug.

```text

 RUN  v5.1.0 /workspace/scratch/5290b5ee4677/repo/week-08/app

 ❯ src/booking.test.ts (29 tests | 11 failed) 22ms
   ❯ canBook — reviewed booking cases (29)
     × T01 AC4: allows touching after an existing booking 7ms
     × T06 AC2: allows exactly 120 minutes 2ms
     × T08 AC4: allows touching before an existing booking 1ms
     × T14 AC4: allows a valid request when there are no existing bookings 1ms
     × AC5: repeated Available decisions preserve unsorted booking data 2ms
     × X1 AC1: allows an end exactly at minute 1440 1ms
     × T16 AC1: allows a request starting one minute after now 1ms
     × T19 AC1: allows a one-minute booking just after midnight 0ms
     × T23 AC4: allows a gap touching both bookings in an unsorted schedule 0ms
     × BUG-A AC4: allows a gap touching two neighbours in a three-booking schedule 0ms
     × BUG-B AC5: a non-touching Available request leaves bookings unchanged 0ms

⎯⎯⎯⎯⎯⎯ Failed Tests 11 ⎯⎯⎯⎯⎯⎯⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/11]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T06 AC2: allows exactly 120 minutes
AssertionError: expected [ { start: 600, end: 660 }, …(1) ] to deeply equal [ { start: 600, end: 660 } ]

- Expected
+ Received

  [
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 840,
+     "start": 720,
+   },
  ]

 ❯ src/booking.test.ts:71:30
     69|
     70|     expect(canBook(request)).toBe(true);
     71|     expect(request.bookings).toEqual(before);
       |                              ^
     72|   });
     73|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/11]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/11]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T14 AC4: allows a valid request when there are no existing bookings
AssertionError: expected [ { start: 630, end: 690 } ] to deeply equal []

- Expected
+ Received

- []
+ [
+   {
+     "end": 690,
+     "start": 630,
+   },
+ ]

 ❯ src/booking.test.ts:135:30
    133|
    134|     expect(canBook(request)).toBe(true);
    135|     expect(request.bookings).toEqual(before);
       |                              ^
    136|   });
    137|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[4/11]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > AC5: repeated Available decisions preserve unsorted booking data
AssertionError: expected [ { start: 900, end: 960 }, …(2) ] to deeply equal [ { start: 900, end: 960 }, …(1) ]

- Expected
+ Received

@@ -5,6 +5,10 @@
    },
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 870,
+     "start": 810,
+   },
  ]

 ❯ src/booking.test.ts:149:30
    147|
    148|     expect(canBook(request)).toBe(true);
    149|     expect(request.bookings).toEqual(before);
       |                              ^
    150|     expect(canBook(request)).toBe(true);
    151|     expect(request.bookings).toEqual(before);

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[5/11]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > X1 AC1: allows an end exactly at minute 1440
AssertionError: expected [ { start: 600, end: 660 }, …(1) ] to deeply equal [ { start: 600, end: 660 } ]

- Expected
+ Received

  [
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 1440,
+     "start": 1380,
+   },
  ]

 ❯ src/booking.test.ts:159:30
    157|
    158|     expect(canBook(request)).toBe(true);
    159|     expect(request.bookings).toEqual(before);
       |                              ^
    160|   });
    161|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[6/11]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T16 AC1: allows a request starting one minute after now
AssertionError: expected [ { start: 600, end: 660 }, …(1) ] to deeply equal [ { start: 600, end: 660 } ]

- Expected
+ Received

  [
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 570,
+     "start": 541,
+   },
  ]

 ❯ src/booking.test.ts:188:30
    186|
    187|     expect(canBook(request)).toBe(true);
    188|     expect(request.bookings).toEqual(before);
       |                              ^
    189|   });
    190|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[7/11]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T19 AC1: allows a one-minute booking just after midnight
AssertionError: expected [ { start: 1, end: 2 } ] to deeply equal []

- Expected
+ Received

- []
+ [
+   {
+     "end": 2,
+     "start": 1,
+   },
+ ]

 ❯ src/booking.test.ts:213:30
    211|
    212|     expect(canBook(request)).toBe(true);
    213|     expect(request.bookings).toEqual(before);
       |                              ^
    214|   });
    215|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[8/11]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[9/11]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > BUG-A AC4: allows a gap touching two neighbours in a three-booking schedule
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:275:30
    273|     });
    274|
    275|     expect(canBook(request)).toBe(true);
       |                              ^
    276|   });
    277|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[10/11]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > BUG-B AC5: a non-touching Available request leaves bookings unchanged
AssertionError: expected [ { start: 600, end: 660 }, …(1) ] to deeply equal [ { start: 600, end: 660 } ]

- Expected
+ Received

  [
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 780,
+     "start": 720,
+   },
  ]

 ❯ src/booking.test.ts:284:22
    282|
    283|     expect(canBook(request)).toBe(true);
    284|     expect(bookings).toEqual(before);
       |                      ^
    285|   });
    286| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[11/11]⎯


 Test Files  1 failed (1)
      Tests  11 failed | 18 passed (29)
   Start at  17:50:57
   Duration  322ms (transform 51%, tests 28%, import 16%, worker 5%)
```

---

## 3. Defect log

One row per defect. At least **BUG-A and BUG-B**. "Suspected cause" is your hypothesis
**before** you ask any assistant: the line and why.

| Defect | Test ID | Input | Expected | Actual | Suspected cause (line and why) |
| --- | --- | --- | --- | --- | --- |
| BUG-A | | | | | |
| BUG-B | | | | | |

---

## 4. Tasks 2–3 — the skill

**The checks from the deck, before you zip it.** Answer each one yes / no:

| Check | yes / no |
| --- | --- |
| The file is plain UTF-8 text, named exactly `SKILL.md` (not `SKILL.md.txt`) | yes / no |
| The first and the closing YAML delimiter are exactly three hyphens: `---` | yes / no |
| `name` is lowercase with hyphens, and `description` says WHEN to use it | yes / no |
| I read the whole file once: no passwords, API keys or private student data | yes / no |

**The contents of `skills/bug-detector.zip`.** Paste the listing (Windows: open the ZIP and copy
the paths; macOS/Linux: `unzip -l skills/bug-detector.zip`):

```text
(paste here)
```

**Installation.** Where you uploaded it, what the upload said, and whether a new chat showed the
skill as enabled. If upload was not available, write `prompt-only simulation` and say why.
Screenshot of the result: `evidence/install.png`.

<!-- Write below this line -->

---

## 5. Task 4 — without the skill

A **fresh chat, with no skill enabled**. Paste exactly what you sent: the deck's question, then
the same input you will use in section 6 (AC1–AC6, the failing test output, the code of
`canBook`):

```text
(paste here)
```

**The assistant's answer, pasted unedited:**

```text
(paste here)
```

---

## 6. Task 5 — with the skill

**Another fresh chat, with `bug-detector` enabled.** Send exactly the same input as in section 5.
Only the question changes, to the deck's skill question:

```text
(paste here)
```

**The assistant's answer, pasted unedited:**

```text
(paste here)
```

Did the environment show that the skill was invoked? yes / no / not shown

---

## 7. Comparison — judged against the actual code

Do not assume the skill did better. Judge both answers against the code and against what your
tests showed. Write a short verdict in each cell, and give a reason where they differ.

| Criterion | No skill | With skill |
| --- | --- | --- |
| Correct root cause | | |
| Reproducible test | | |
| Minimal proposed patch | | |
| Unsupported claims | | |
| Clarity of explanation | | |

**Which bugs did each answer find?** (BUG-A, BUG-B, both, neither)

-

---

## 8. Task 6 — repair and regression

Review the proposed patch yourself, then make **one minimal change per bug**, one commit each.
Rerun the test that was failing, then the full suite.

### 8.1 The BUG-A patch

The change as a diff (`git diff`, or the old and the new line), then the real run:

```text
(paste here)
```

### 8.2 The BUG-B patch and the final run

The change as a diff, then the real output of the **full** suite. Every test must pass.

```text
(paste here)
```

---

## 9. What still fails, and what AI-assisted debugging cannot do

### 9.1 Checks I am keeping as FAIL or ERROR

Use the same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| | |

### 9.2 One limitation of AI-assisted debugging

<!-- Use something that actually happened in sections 5-8. 20 words or more. -->
-

---

## 10. Conclusion (80–150 words)

<!-- Answer both, in your own words, without the assistant (3-5 sentences, as the deck asks):
     (a) Did the skill help? Show it with one row of section 7.
     (b) What did your tests actually prove - and what did they not?
     Worthless: "The skill made the AI much better at debugging."
     Worth everything: "Both answers found BUG-A from the T01 failure. Only the skill answer
     separated BUG-B as a hypothesis instead of a fact, because step 4 told it to. BUG-B was only
     visible after the BUG-A patch: the AC5 test had been failing for the wrong reason." -->

<!-- Write your conclusion below this line -->
