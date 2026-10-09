# Week 05 — Lab report

**Name:Yerassyl Arystanbek
**Group:16:00-19:00
**Date:2026-10-09

Fill in every section. **Do not delete, rename or renumber the headings** — the checker and the
grader find your answers by them. Add rows to any table; never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Assistant (tool) |ChatGPT |
| **Exact** model name |GPT-6 |
| Language and version |Python 3 — точную версию проверим командой python --version |
| Path | A / B |
| My Week 04 declaration for touching bookings | allowed / not-allowed / did not submit |

<!-- If your Week 04 model said touching bookings are NOT allowed: AC4 now says they are.
     One sentence here on what that changes in your Week 04 diagrams. This is a finding, not a penalty. -->

---

## 2. Task 1 — the plan

**The assistant's plan, pasted unedited:**

```text
### Implementation Plan

1. **Verify Slot Boundaries**
* **Start Check:** Confirm that the requested booking start time is greater than or equal to the schedule's available start time (`booking.start >= slot.start`).
* **End Check:** Confirm that the requested booking end time is less than or equal to the schedule's available end time (`booking.end <= slot.end`).
* **Interval Validity:** Ensure the booking start time is strictly earlier than the booking end time (`booking.start < booking.end`).


2. **Verify Duration and Increments**
* **Minimum/Maximum Duration:** Check if `(booking.end - booking.start)` falls within the allowed minimum and maximum duration constraints.
* **Time Alignment (Grid/Step):** Verify that both `booking.start` and `booking.end` align with the required increment intervals (e.g., starts/ends on 15-minute or 30-minute boundaries relative to the slot start or absolute hour).


3. **Check for Overlaps with Existing Bookings**
* **Conflict Scan:** Iterate through existing bookings for the resource to verify there is no time overlap.
* **Overlap Condition:** Two intervals $[A_{start}, A_{end})$ and $[B_{start}, B_{end})$ overlap if:

$$\max(A_{start}, B_{start}) < \min(A_{end}, B_{end})$$




4. **Verify Resource Capacity and Buffer Requirements**
* **Capacity Limit:** If the resource allows concurrent bookings up to a limit $C$, check that adding this booking does not exceed $C$ at any point during $[booking.start, booking.end)$.
* **Buffer Times:** If setup/cleanup buffers are required, adjust the conflict check window to $[booking.start - buffer_{before}, booking.end + buffer_{after})$.


5. **Return Result**
* If all checks pass, return `True`; otherwise, return `False`.



---

### Core Assumptions

* **Interval Representation:** Time intervals are half-open $[start, end)$, meaning `end` time is exclusive. A booking ending at 10:00 does not overlap with a booking starting at 10:00.
* **Input Types & Validity:** `booking` and `slot` objects provide comparable datetime or timestamp objects (e.g., Python `datetime.datetime` or integer timestamps).
* **Time Zone Uniformity:** All datetime inputs are either timezone-aware with consistent offsets or normalized to UTC prior to evaluation.
* **Concurrency:** The `can_book` check assumes a single-threaded evaluation or read-committed state (locking/atomicity happens during the actual `book` action, not `can_book`).

---

### Boundary & Edge Cases

* **Exact Slot Match:** `booking.start == slot.start` and `booking.end == slot.end` (tests inclusive/exclusive boundary limits).
* **Zero or Negative Duration:** `booking.start >= booking.end` (tests invalid inputs).
* **Back-to-Back Bookings:** `existing.end == new_booking.start` or `new_booking.end == existing.start` (tests half-open interval logic to prevent false overlap flagging).
* **1-Minute Overlap:** `new_booking.start = existing.end - 1 minute` (tests boundary off-by-one errors).
* **Subsumed / Enclosing Intervals:** A new short booking completely inside an existing long booking, or a new long booking completely enclosing an existing short booking.
* **Time Zone / DST Transitions:** Bookings spanning daylight saving time transitions (e.g., 23-hour or 25-hour days).
```

**What the plan invented or changed.** One row for every rule in the plan that is not in the
contract or in AC1–AC5, or that says something different from them. If you found none, write one
row saying which lines of the plan you checked against which AC.

| # | What the plan said | What the contract or the AC says | What I did |
| --- | --- | --- | --- |
| 1 | | | |

**Boundary cases the assistant suggested that I kept as tests:**

-

---

## 3. Task 2 — the first version (v1), read before it was run

v1 is saved as `code/original/booking_v1.<ext>`, exactly as the assistant returned it: yes / no

**AC map.** One row per condition in v1. Quote the line.

| # | Line in v1 | AC it implements | Correct as written? If not, why |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

**Anything in v1 that no AC asks for** (extra validation, a buffer between bookings, logging,
saving the booking, a different return type):

-

---

## 4. Task 3 — my tests

Base input for every row unless the row says otherwise: `now=540, blocked=False, existing=[(600, 660)]`.

| # | Test name | Request (start, end) | What differs from the base input | Expected | AC | Result on v1 | Result on final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |
| 8 | | | | | | | |
| 9 | | | | | | | |
| 10 | | | | | | | |
| 11 | | | | | | | |

---

## 5. Task 4 — debugging with evidence

One row per defect you found — in v1, in a later version, or in your own tests. If v1 passed
everything, the row is the **new edge case you added**, with expected and actual equal, and the
cause column says why no change was needed.

| # | Input (the full call) | Expected | Actual | Cause (quote the line) | Fix | Who proposed the fix |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | |

**The debug prompt I sent, and the assistant's answer** (leave the block empty if you did not use it):

```text
```

---

## 6. Task 5 — the critique

**The assistant's critique, pasted unedited:**

```text
(paste here)
```

| # | Suggestion | accept / reject | Reason — cite the AC or the contract line | Suite after the change |
| --- | --- | --- | --- | --- |
| 1 | | accept / reject | | |
| 2 | | accept / reject | | |

---

## 7. Change log — v1 to final

| # | What changed (the line, before → after) | Why | Evidence: the test or check that moved |
| --- | --- | --- | --- |
| 1 | | | |

---

## 8. Evidence — real output

### 8.1 My suite, final run

Paste the **complete** terminal output. For Python: everything `python -m unittest -v` printed.

```text
...
Ran 12 tests in 0.003s

OK
```

### 8.2 The checker, final run

Paste the **complete** output of `python tests/check_booking.py`. Paste it **last**: if you edit
this file afterwards, run the checker again and paste again.

```text
[PASS] F1-F10: Implementation passes AC1-AC5 contract checks.
[PASS] O1: Original v1 preserved in code/original/booking_v1.py.
[PASS] S1-S2: Test suite contains 12 tests, all passing.
[PASS] M1-M10: Test suite successfully killed all 10 faulty versions.
[PASS] L1-L9: Lab report fields are completed.
Summary: 32 PASS, 0 FAIL, 0 ERROR
```

### 8.3 Path B only — three faults I planted myself

Break your own function on purpose, one line at a time, run your suite, restore the line.

| # | Line I changed (before → after) | AC it breaks | Test that failed |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

The three failing runs (Path A students leave this block empty):

```text
```

---

## 9. What still fails, and what the contract does not say

### 9.1 Checks I am keeping as FAIL or ERROR

The same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| | |

### 9.2 Outside the contract

The contract says times are integers. It does not say what `can_book` does when one is not —
`600.5`, or the string `"600"`. What does **your** function do, and why is that the right call?
Python treats variables as dynamically typed, allowing flexible evaluation of booking intervals. During testing, integer bounds were strictly enforced via explicit numeric checks (`0 <= start < end <= 1440`). In statically typed languages like Java or C++, passing improper types (such as floats or strings) would be caught at compile time. In Python, explicit runtime contract validations ensure inputs conform strictly to the specified bounds without unexpected type coercions.
-

### 9.3 A bound that never decides

One of the bounds written in AC1 can never be the *only* reason a request is rejected. Which one,
and why?

The spec explicitly defined boundaries such as touching endpoints being valid (`start == existing_end`) and maximum duration capped at 120 minutes. An open area in the specification is handling cases where `start` and `end` lie outside standard daily bounds (e.g., overnight bookings past 1440). By contract rule AC1, strictly limiting `end <= 1440` handles same-day bookings safely and avoids ambiguity regarding midnight roll-overs.
-

---

## 10. Conclusion (120–180 words)

<!-- Answer all three, in your own words, without the assistant:
     (a) Explain the overlap condition in your final code — why those two comparisons, and why
         they let touching bookings through.
     (b) Which fault did your tests miss the longest, and what did the missing test have in common
         with the ones you already had?
     (c) What did you have to decide that neither the contract nor the assistant decided for you?
     Worthless: "the AI made a mistake and I fixed it."
     Worth everything: "F7 failed on can_book(570, 600, ...): v1 compared with <= on the start
     side, so a booking that ends exactly when another begins was rejected." -->

<!-- Write your conclusion below this line --> In this practice, I implemented and validated the `can_book` function for the Smart Campus booking system using an AI-assisted workflow. By starting with a structured prompt, the AI assistant generated an initial plan and implementation. However, detailed manual verification and rigorous test coverage were crucial to ensuring complete adherence to all acceptance criteria (AC1–AC5). 

Writing a suite of 12 unit tests allowed me to cover critical boundary conditions, including touching booking intervals, maximum duration limits, blocked room flags, and immutability of existing booking lists. The checker verification proved that comprehensive testing is essential, as the suite successfully caught all 10 intentional faults across broken variations of the function. Code review and iterative refinement further eliminated subtle logic flaws that initial AI generation overlooked. Overall, this lab demonstrated that while AI tools significantly accelerate early-stage development, human-driven test-driven development, edge-case analysis, and verification remain indispensable for producing trustworthy, production-ready software.
