# Week 08 — Lab report

**Name:** Yerassyl Arystanbek
**Group:** Monday 16:00–19:00 (from Week 07 report)
**Date:** 8 November 2026

AI preparation disclosure: Codex copied the actual Week 07 project, ran the terminal commands, added the two regression tests, applied the two patches, and drafted factual report material. The student subsequently supplied two fresh-chat diagnostic replies and a screenshot of the acknowledged prompt-only simulation. The comparison is an AI-assisted draft for student review; no installed skill is claimed.

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Assistant I debugged with (tool) | ChatGPT for both fresh diagnostic chats; Codex assisted preparation and report drafting |
| Exact model (with its version, or `not displayed`) | not displayed |
| Where the skill was installed (ChatGPT / Claude web / Claude Code / prompt-only simulation) | Prompt-only simulation in a separate ChatGPT chat; no installed skill |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | Codex Linux workspace for the baseline and initial reproduction; the student's Windows computer, VS Code/CMD, for local reproduction and both repair runs |
| Vitest version (the `RUN  v…` line of a run) | 5.1.0 |
| Language of my booking module (`ts` or `js`) — the file I copied from `buggy/` | ts |

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

Process disclosure: AI assistance began before a personal hypothesis was written. These are factual test observations drafted by Codex, not a claim of an independent pre-AI hypothesis.

One row per defect. At least **BUG-A and BUG-B**. "Suspected cause" is your hypothesis
**before** you ask any assistant: the line and why.

| Defect | Test ID | Input | Expected | Actual | Suspected cause (line and why) |
| --- | --- | --- | --- | --- | --- |
| BUG-A | T01, T08, T23; BUG-A | now 540; request 780–840; bookings 840–900, 600–660, 720–780 | true (AC4) | false at the Boolean assertion | Personal pre-AI hypothesis was not captured. AI-reviewed cause: inclusive comparisons count endpoint equality as a conflict; AC4 requires strict comparisons. | |
| BUG-B | T06, AC5; BUG-B | now 540; request 720–780; bookings 600–660 | true and original array unchanged (AC5) | true, then deep equality fails because 720–780 was appended | Personal pre-AI hypothesis was not captured. AI-reviewed cause: bookings.push appends a request during an availability check; the non-touching fixture reaches it independently of BUG-A. | |

---

## 4. Tasks 2–3 — the skill

The source file and the committed ZIP were checked locally by update_diagnosis.py. The fourth answer records the student's --skill-reviewed declaration, after personally reading the complete file.

| Check | yes / no |
| --- | --- |
| The file is plain UTF-8 text, named exactly `SKILL.md` (not `SKILL.md.txt`) | yes |
| The first and the closing YAML delimiter are exactly three hyphens: `---` | yes |
| `name` is lowercase with hyphens, and `description` says WHEN to use it | yes |
| I read the whole file once: no passwords, API keys or private student data | yes |

**The contents of `skills/bug-detector.zip`**, read from the actual local ZIP:

```text
bug-detector/.gitkeep (0 bytes)
bug-detector/SKILL.md (582 bytes)
```

**Installation.**

<!-- Write below this line -->

The declared environment is a prompt-only simulation, not an installed skill. In a fresh ChatGPT chat, the student first supplied the complete hand-typed procedure with an explicit simulation statement. The assistant acknowledged: "I'll follow the procedure directly without searching for a skill or editing code." The student then sent the prepared diagnostic input. The supplied screenshot is evidence/install.png. No installed-skill badge is shown. An earlier unsuccessful request reported that bug-detector could not be found; it is disclosed in evidence/skill-attempt-note.md and is not used as the controlled simulation response.

## 5. Task 4 — without the skill

Fresh ChatGPT chat without a loaded bug-detector procedure. The student supplied this complete answer; the exact model is not displayed in the supplied evidence.

**The diagnostic message sent:**

```text
Find the root cause of the failed room-booking test. Propose minimal patch and regression test. Do not edit code.

Scenario: Smart Campus room availability. One room, fictional bookings, fixed time, Boolean availability; no login or database.
AC1 Reject start >= end and requests in the past.
AC2 Enforce the maximum allowed duration (120 minutes).
AC3 Reject a blocked room.
AC4 Reject overlaps; allow bookings that only touch at endpoints.
AC5 Return Available / Unavailable without changing booking data.
AC6 Preserve clear UI feedback on desktop and mobile.

Failing test fixture: start=660, end=720, now=540, blocked=false, bookings=[{start:600,end:660}].
The test first expects canBook(request).toBe(true), then expects request.bookings to equal a structuredClone taken before the call.
Observed failure (verbatim excerpt from the real run):
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


Provided canBook (unchanged):
export function canBook({ start, end, now, blocked, bookings }: {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: { start: number; end: number }[];
}): boolean {
  if (!(0 <= start && start < end && end <= 1440)) return false;
  if (!(start > now)) return false;
  if (end - start > 120) return false;
  if (blocked) return false;
  for (const b of bookings) {
    if (start <= b.end && end >= b.start) return false;
  }
  // keep the room's list current with the slot that was just found free
  bookings.push({ start, end });
  return true;
}
```

**The assistant's answer, pasted unedited:**

````markdown
The test expectation is correct. There are **two implementation defects**:

1. **AC4: touching endpoints are treated as overlaps.** For this fixture, `660 <= 660 && 720 >= 600` is `true`, so `canBook` returns `false`. The intervals only touch at 660; overlap comparisons must be strict.
2. **AC5: successful checks mutate bookings.** `bookings.push(...)` changes the input. The current early return avoids this mutation, and the failed first assertion prevents the immutability assertion from running. Fixing only AC4 exposes AC5.

Proposed minimal patch:
```
   for (const b of bookings) {
-    if (start <= b.end && end >= b.start) return false;
+    if (start < b.end && end > b.start) return false;
   }
-  // keep the room's list current with the slot that was just found free
-  bookings.push({ start, end });
   return true;
```

Keep the existing endpoint test unchanged. Add this independent regression test for mutation, using a slot clearly separated from the existing booking:
```
it('AC5: checking a free slot leaves bookings unchanged', () => {
  const request = {
    start: 780,
    end: 840,
    now: 540,
    blocked: false,
    bookings: [{ start: 600, end: 660 }],
  };
  const before = structuredClone(request.bookings);

  const result = canBook(request);

  expect(request.bookings).toEqual(before);
  expect(result).toBe(true);
});
```

This additional test catches mutation even while the endpoint bug remains.

An isolated JavaScript reproduction confirmed:

| Implementation   | Result for reported fixture | Bookings unchanged |
| ---------------- | --------------------------- | ------------------ |
| Original         | `false`                     | Yes                |
| Overlap fix only | `true`                      | No                 |
| Both fixes       | `true`                      | Yes                |

No code was edited.
````

The corresponding complete reply is also preserved in evidence/without-skill-answer.md.

## 6. Task 5 — with the skill

A separate fresh ChatGPT chat using the explicitly declared prompt-only procedure. The student supplied this complete answer; the exact model is not displayed in the supplied evidence.

**The diagnostic message sent:**

```text
Use the bug-detector skill to diagnose the failed room-booking test.

Scenario: Smart Campus room availability. One room, fictional bookings, fixed time, Boolean availability; no login or database.
AC1 Reject start >= end and requests in the past.
AC2 Enforce the maximum allowed duration (120 minutes).
AC3 Reject a blocked room.
AC4 Reject overlaps; allow bookings that only touch at endpoints.
AC5 Return Available / Unavailable without changing booking data.
AC6 Preserve clear UI feedback on desktop and mobile.

Failing test fixture: start=660, end=720, now=540, blocked=false, bookings=[{start:600,end:660}].
The test first expects canBook(request).toBe(true), then expects request.bookings to equal a structuredClone taken before the call.
Observed failure (verbatim excerpt from the real run):
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


Provided canBook (unchanged):
export function canBook({ start, end, now, blocked, bookings }: {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: { start: number; end: number }[];
}): boolean {
  if (!(0 <= start && start < end && end <= 1440)) return false;
  if (!(start > now)) return false;
  if (end - start > 120) return false;
  if (blocked) return false;
  for (const b of bookings) {
    if (start <= b.end && end >= b.start) return false;
  }
  // keep the room's list current with the slot that was just found free
  bookings.push({ start, end });
  return true;
}
```

**The assistant's answer, pasted unedited:**

````markdown
**Two defects are confirmed** by running the supplied function in Node. The test’s expected `true` is correct.

| Defect                              | Evidence                                                                    | Root cause                                                   | Fix                                   | Test                                                                  |
| ----------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------- | --------------------------------------------------------------------- |
| AC4: touching endpoints rejected    | The supplied fixture returns `false`: `660 <= 660 && 720 >= 600` is `true`. | Inclusive comparisons treat touching as overlap.             | Use `start < b.end && end > b.start`. | Keep T01 unchanged: expect `true` and unchanged bookings.             |
| AC5: successful checks mutate input | A separate request for `[720,780]` returns `true` and appends a booking.    | `bookings.push({ start, end })` modifies the caller’s array. | Remove the push and its comment.      | Check a clearly separated slot; expect `true` and unchanged bookings. |

In the observed T01 failure, the early return prevents mutation, and the first failed assertion stops the immutability assertion from running. Fixing only AC4 exposes AC5.

Suggested minimal patch — **not applied**:
```
   for (const b of bookings) {
-    if (start <= b.end && end >= b.start) return false;
+    if (start < b.end && end > b.start) return false;
   }
-  // keep the room's list current with the slot that was just found free
-  bookings.push({ start, end });
   return true;
```

Keep the existing endpoint test and add this independent regression:
```
it('AC5: checking a free slot leaves bookings unchanged', () => {
  const request = {
    start: 720,
    end: 780,
    now: 540,
    blocked: false,
    bookings: [{ start: 600, end: 660 }],
  };
  const before = structuredClone(request.bookings);

  const result = canBook(request);

  expect(request.bookings).toEqual(before);
  expect(result).toBe(true);
});
```

This regression fails on the supplied implementation and should pass after the proposed patch. AC6 requires separate UI evidence; it cannot be assessed from this function.
````

The corresponding complete reply is also preserved in evidence/with-skill-answer.md.

Did the environment show that the skill was invoked? **not shown** as an installed skill. The chat explicitly acknowledged the pasted procedure; the declared mode is prompt-only.

## 7. Comparison — judged against the actual code

AI-assisted comparison draft: each judgement below is checked against the provided code and the existing real test failures. The student must review this table before accepting the patches.

| Criterion | No skill | With skill |
| --- | --- | --- |
| Correct root cause | Correct for both BUG-A/AC4 and BUG-B/AC5. The inclusive overlap condition rejects equality; bookings.push changes the caller's array. The real T01 failure and non-touching BUG-B failure support these explanations. | Correct for the same two defects and the same expressions. The table names evidence separately; it does not identify an additional implementation defect. |
| Reproducible test | Proposes 780–840 with now 540 and existing 600–660. It is a deterministic free slot and isolates mutation from endpoint rejection; it asserts deep equality and exact true. | Proposes 720–780 with the same now and existing booking. This also isolates BUG-B, asserts the preserved array and exact true, and matches the new BUG-B fixture already in the suite. |
| Minimal proposed patch | Strict comparators fix BUG-A. Deleting bookings.push fixes BUG-B, but deleting its comment as well is unnecessary for this lab's one-line-per-bug rule. Modify that proposal: retain the comment and delete only the push. | The same judgement: accept strict comparisons, delete only bookings.push, and retain the comment. The skill does not prevent this unnecessary extra deletion. Do not add a duplicate AC5 test because the committed BUG-B regression already supplies it. |
| Unsupported claims | Reports an isolated JavaScript reproduction, but the supplied reply contains no raw terminal output. Treat that as an assistant claim; only saved project Vitest logs establish project results. No claim that AC6 was verified is made. | States that the function was run in Node, but supplies no raw terminal output for that execution. This does not establish that the project suite passes. It correctly states that AC6 cannot be assessed from the function. |
| Clarity of explanation | Clearly explains that T01 returns early and its first failed assertion masks the later mutation assertion. The small result table illustrates why fixing BUG-A alone exposes BUG-B. | Clearly explains the same masking. The required defect/evidence/root-cause/fix/test columns make the mapping easier to scan, while the technical diagnosis remains the same. |

**Which bugs did each answer find?** Both answers found BUG-A and BUG-B. Neither changed project files as part of the diagnostic reply. The suggested overall verdict is no-difference for diagnostic correctness; the simulation improved the visible structure. This is a single comparison and does not measure a general model-performance improvement.

**Patch review for the next step:** change the one overlap-condition line for BUG-A; delete only the single bookings.push line for BUG-B. The existing 27 Week 07 tests and the two new BUG-A/BUG-B regressions remain unchanged.

## 8. Task 6 — repair and regression

Review the proposed patch yourself, then make **one minimal change per bug**, one commit each.
Rerun the test that was failing, then the full suite.

### 8.1 The BUG-A patch

The helper applied the reviewed one-line BUG-A patch. The full run still exposes BUG-B.

```diff
warning: in the working copy of 'week-08/app/src/booking.ts', LF will be replaced by CRLF the next time Git touches it
diff --git a/week-08/app/src/booking.ts b/week-08/app/src/booking.ts
index e0f046d..4ea478a 100644
--- a/week-08/app/src/booking.ts
+++ b/week-08/app/src/booking.ts
@@ -26,7 +26,7 @@ export function canBook({ start, end, now, blocked, bookings }: {
   if (end - start > 120) return false;
   if (blocked) return false;
   for (const b of bookings) {
-    if (start <= b.end && end >= b.start) return false;
+    if (start < b.end && end > b.start) return false;
   }
   // keep the room's list current with the slot that was just found free
   bookings.push({ start, end });
```

```text

 RUN  v5.1.0 C:/Users/777/Desktop/SE/software-engineering-practice/week-08/app

 ✓ src/booking.test.ts (29 tests | 28 skipped) 2ms

 Test Files  1 passed (1)
      Tests  1 passed | 28 skipped (29)
   Start at  22:54:08
   Duration  1.30s (transform 53%, import 32%, worker 11%, tests 4%)
```

```text

 RUN  v5.1.0 C:/Users/777/Desktop/SE/software-engineering-practice/week-08/app

 ❯ src/booking.test.ts (29 tests | 10 failed) 15ms
   ❯ canBook — reviewed booking cases (29)
     × T01 AC4: allows touching after an existing booking 6ms
     ✓ T02 AC1: rejects a request starting exactly now 0ms
     ✓ T03 AC1: rejects zero duration 0ms
     ✓ T04 AC1: rejects an end before the start 0ms
     ✓ T05 AC1: rejects an end past minute 1440 0ms
     × T06 AC2: allows exactly 120 minutes 1ms
     ✓ T07 AC2: rejects 121 minutes 0ms
     × T08 AC4: allows touching before an existing booking 1ms
     ✓ T09 AC4: rejects a partial overlap 0ms
     ✓ T10 AC4: rejects a request containing an existing booking 0ms
     ✓ T11 AC4: rejects a request inside an existing booking 0ms
     ✓ T12 AC4: rejects an identical interval 0ms
     ✓ T13 AC3: rejects a blocked room for an otherwise valid request 0ms
     × T14 AC4: allows a valid request when there are no existing bookings 1ms
     × AC5: repeated Available decisions preserve unsorted booking data 1ms
     × X1 AC1: allows an end exactly at minute 1440 0ms
     ✓ X2 AC4: rejects an overlap with the second booking 0ms
     ✓ T15 AC1: rejects a request starting one minute before now 0ms
     × T16 AC1: allows a request starting one minute after now 1ms
     ✓ T17 AC1: rejects a negative start minute 0ms
     ✓ T18 AC1: rejects minute zero when the supplied current time is zero 0ms
     × T19 AC1: allows a one-minute booking just after midnight 0ms
     ✓ T20 AC4: rejects a one-minute overlap at the existing booking end 0ms
     ✓ T21 AC4: rejects a one-minute overlap at the existing booking start 0ms
     ✓ T22 AC4: rejects an earlier conflict despite a later nonconflicting booking 0ms
     × T23 AC4: allows a gap touching both bookings in an unsorted schedule 0ms
     ✓ T24 AC3: rejects a blocked room even with no existing bookings 0ms
     ✓ BUG-A AC4: allows a gap touching two neighbours in a three-booking schedule 0ms
     × BUG-B AC5: a non-touching Available request leaves bookings unchanged 1ms

⎯⎯⎯⎯⎯⎯ Failed Tests 10 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T01 AC4: allows touching after an existing booking
AssertionError: expected [ { start: 600, end: 660 }, …(1) ] to deeply equal [ { start: 600, end: 660 } ]

- Expected
+ Received

  [
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 720,
+     "start": 660,
+   },
  ]

 ❯ src/booking.test.ts:31:30
     29|
     30|     expect(canBook(request)).toBe(true);
     31|     expect(request.bookings).toEqual(before);
       |                              ^
     32|   });
     33|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/10]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/10]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T08 AC4: allows touching before an existing booking
AssertionError: expected [ { start: 600, end: 660 }, …(1) ] to deeply equal [ { start: 600, end: 660 } ]

- Expected
+ Received

  [
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 600,
+     "start": 570,
+   },
  ]

 ❯ src/booking.test.ts:87:30
     85|
     86|     expect(canBook(request)).toBe(true);
     87|     expect(request.bookings).toEqual(before);
       |                              ^
     88|   });
     89|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/10]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[4/10]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[5/10]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[6/10]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[7/10]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[8/10]⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > T23 AC4: allows a gap touching both bookings in an unsorted schedule
AssertionError: expected [ { start: 720, end: 780 }, …(2) ] to deeply equal [ { start: 720, end: 780 }, …(1) ]

- Expected
+ Received

@@ -5,6 +5,10 @@
    },
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 720,
+     "start": 660,
+   },
  ]

 ❯ src/booking.test.ts:255:30
    253|
    254|     expect(canBook(request)).toBe(true);
    255|     expect(request.bookings).toEqual(before);
       |                              ^
    256|   });
    257|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[9/10]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[10/10]⎯


 Test Files  1 failed (1)
      Tests  10 failed | 19 passed (29)
   Start at  22:54:10
   Duration  487ms (tests 38%, import 28%, transform 18%, worker 16%)
```

### 8.2 The BUG-B patch and the final run

The helper deleted the single bookings.push line for BUG-B. Actual targeted and full runs follow.

```diff
warning: in the working copy of 'week-08/app/src/booking.ts', LF will be replaced by CRLF the next time Git touches it
diff --git a/week-08/app/src/booking.ts b/week-08/app/src/booking.ts
index 4ea478a..64e9a4b 100644
--- a/week-08/app/src/booking.ts
+++ b/week-08/app/src/booking.ts
@@ -29,6 +29,5 @@ export function canBook({ start, end, now, blocked, bookings }: {
     if (start < b.end && end > b.start) return false;
   }
   // keep the room's list current with the slot that was just found free
-  bookings.push({ start, end });
   return true;
 }
```

```text

 RUN  v5.1.0 C:/Users/777/Desktop/SE/software-engineering-practice/week-08/app

 ✓ src/booking.test.ts (29 tests | 28 skipped) 3ms

 Test Files  1 passed (1)
      Tests  1 passed | 28 skipped (29)
   Start at  22:54:11
   Duration  472ms (transform 55%, import 26%, worker 12%, tests 6%)
```

```text

 RUN  v5.1.0 C:/Users/777/Desktop/SE/software-engineering-practice/week-08/app

 ✓ src/booking.test.ts (29 tests) 5ms

 Test Files  1 passed (1)
      Tests  29 passed (29)
   Start at  22:54:12
   Duration  415ms (import 35%, transform 27%, worker 20%, tests 17%)
```

## 9. What still fails, and what AI-assisted debugging cannot do

### 9.1 Checks I am keeping as FAIL or ERROR

Current real checker results; unfinished work is declared below.

| Check | Why it stays |
| --- | --- |
| none | No FAIL or ERROR in the current run. |

### 9.2 One limitation of AI-assisted debugging

<!-- Use something that actually happened in sections 5-8. 20 words or more. -->
I see that some problems of AI on the promts 01 without skill after that trying 02 with skill its work.
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
Authorship disclosure: this is AI-assisted writing requested by the student, not an independent personal reflection.

In this comparison, the bug-detector procedure made the response easier to scan, but it did not improve diagnostic correctness because both answers identified BUG-A and BUG-B. Both answers also proposed removing an unnecessary comment, so the reviewed repair kept that comment and changed only the overlap condition and the push line in separate commits. The 29 passing tests support correct decisions for the tested time boundaries, blocked rooms, overlaps and endpoint-touching cases, and they check that availability decisions preserve the original bookings. They do not verify desktop or mobile feedback under AC6, establish behavior for every possible input, or prove that an AI claim of isolated execution is reliable.
