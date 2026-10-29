# SIS #03 — Report: Smart Campus Room Availability Checker

> **Provenance:** This draft was AI-assisted on 2026-10-29. Verify every row and disclose the assistance. Section 2 must reflect your own original work; Section 10 must be written by you. Section 11 is incomplete without original full exchanges. Screenshots and test output cited below are from observed material, not newly generated.

## 1. Setup and reuse

| Item | Value |
| --- | --- |
| Coding assistant (tool) | ChatGPT (web) |
| Coding assistant model | GPT-6 |
| Bolt.new model | not displayed |
| Bolt project link | not-shared |
| Language | Python |
| Path | A |
| Python v1 from | week-05 |
| Web v1 from | week-06 |

The Python v1 was copied from `week-05/code/original/booking_v1.py`. The first web export came from `week-06/original/`. Both source versions are retained as original evidence. The initial SIS 03 commit was `75fcd6d` and a later commit was `5693413`. The first baseline section was discussed with ChatGPT; that use must be disclosed rather than described as AI-free work.

## 2. Baseline — before any new AI exchange

> **Personal-authorship notice:** The text below follows the Section 2 draft previously edited with AI assistance. Check it against your original first commit and revise it in your own words before submitting. Do not claim it was written without AI.

### 2.1 Scope in my own words

**Scope:** The Smart Campus Room Availability Checker helps students check if a study room is available for a selected time. The system checks the time, room status and existing bookings. It only shows availability and does not create new bookings. It does not need login, backend or database.

### 2.2 The acceptance criteria in my own words

| AC | In my own words |
| --- | --- |
| AC1 | The start and end times must be valid integer minutes between 0 and 1440. The start must be earlier than the end and strictly later than the current time. |
| AC2 | Students can select a time period of up to 120 minutes. Exactly 120 minutes is allowed. |
| AC3 | If the room is blocked, the system must show that it is unavailable. |
| AC4 | A new time must not overlap with existing bookings. If one booking ends exactly when another starts, it is allowed. |
| AC5 | The system must clearly show Available or Unavailable. Existing bookings must not be changed. |
| AC6 | The system must show understandable error messages and work correctly on mobile screens. |

### 2.3 Likely failure points

| # | Failure point | AC | How I will check it |
| --- | --- | --- | --- |
| 1 | The system may reject a booking that starts exactly when another booking ends. | AC4 | Check 660–720 when an existing booking is 600–660. Expected result: Available. |
| 2 | The system may allow a booking that starts at the current time. | AC1 | Set now to 540 and check 540–570. Expected result: Unavailable. |

### 2.4 The contract

| Parameter | Meaning | Type and allowed values |
| --- | --- | --- |
| `start` | Start of the requested booking. | Integer minutes, 0–1440; earlier than end and later than now. |
| `end` | End of the requested booking. | Integer minutes, 0–1440; greater than start. |
| `now` | Current time after midnight. | Integer minutes in 0–1439, assumed valid. |
| `blocked` | Whether the room is blocked. | Boolean, True or False. |
| `existing` | Existing bookings. | Collection of `(start, end)` integer pairs. |
| returns | Whether the request meets the contract. | Boolean; True only if AC1–AC4 pass, otherwise False. |

### 2.5 Initial assumptions and manual checks

**Assumptions:**

1. All times are represented as integer minutes after midnight, and `now` is valid.
2. The system checks only one selected room using fictional booking data.
3. Existing bookings are valid intervals and must not be modified.

**Checked manually:**

- T1 (660–720 against 600–660) was observed in the final browser test mode as Available.
- T2 (630–690 against 600–660) was observed in the final browser test mode as Unavailable.
- T4 (720–840, exactly 120 minutes) was observed in the final browser test mode as Available.

## 3. Python v1 review

| Branch in v1 (quoted) | AC | Satisfies it? | Why |
| --- | --- | --- | --- |
| `if isinstance(item, (tuple, list)):` | AC4 | Partial | The helper extracts booking bounds, but the original signature and data model do not match the SIS contract. |
| `if booking_start >= booking_end:` | AC1 | Partial | It rejects reversed intervals but uses datetimes, does not check integer day bounds, and ignores now. |
| `if min_duration and duration < min_duration:` | AC2 | No | An optional minimum duration is not required by AC2. |
| `if max_duration and duration > max_duration:` | AC2 | Partial | It checks a maximum only when provided, not an unconditional 120-minute maximum. |
| `if booking_start < slot_start or booking_end > slot_end:` | AC1 | Partial | It checks a slot range, but not the required minute range 0–1440 and future start rule. |
| `if step_minutes and step_minutes > 0:` | AC3 | No | Step alignment is unrelated to rejecting blocked rooms; no blocked parameter exists. |
| `if start_delta % step_minutes != 0 or end_delta % step_minutes != 0:` | AC3 | No | It can reject nonaligned durations even when all required room rules pass. |
| `if max(buffered_start, ex_start) < min(buffered_end, ex_end):` | AC4 | Partial | The half-open overlap formula is correct with zero buffer; a nonzero optional buffer would reject touching endpoints. |

The original v1 has the wrong signature and uses `datetime`; the final `code/booking.py` uses `can_book(start, end, now, blocked, existing)` with integer minutes, a mandatory 120-minute limit, a blocked-room check, and the half-open overlap rule. The v1 stays untouched.

## 4. Prototype v1 in Bolt.new

**Prompt as sent:**

~~~~text
Build a small responsive Smart Campus Room Availability Checker. Requirements: AC1: Accept a candidate interval only when 0 ≤ start < end ≤ 1440 and start is after the supplied current time.
AC2: Reject a booking longer than 120 minutes.
AC3: Reject the request when the selected room is blocked.
AC4: Reject any interval that overlaps an existing booking; touching endpoints are allowed.
AC5: Show a clear Available / Unavailable decision without changing the existing booking data.
AC6: The page remains usable at desktop and narrow/mobile width and gives understandable validation feedback.
Use fictional sample data only. Keep the implementation simple and within one-page scope. Do not add authentication, backend services, analytics, or unrelated features. After building, briefly list the main files/components you created.
~~~~

| Generated file or component | Path | Its role |
| --- | --- | --- |
| Main application | src/App.tsx | Renders the page and handles time inputs and result feedback. |
| Availability checker | src/availability.ts | Converts times and applies availability rules. |
| Room list | src/components/RoomList.tsx | Displays the rooms, statuses and selection behavior. |

**What v1 does:**

- Displays five fictional rooms, their locations, seat counts and booked intervals.
- Lets students enter a start and end time and check one selected room.
- Shows Available or Unavailable feedback.
- Uses real current time rather than a fixed 09:00 test clock; screenshots from v1 were taken around 18:49–18:56.
- Faculty Lounge is labeled BLOCKED but cannot be selected for a direct blocked-room feedback check. The original export also contained some out-of-scope code reported by the checker.

## 5. Test cases — executed on both artifacts

Base for Python T1–T11: `now = 540`, `blocked = False`, `existing = [(600, 660)]` except where stated. The Python results below are exactly those printed by `tests/check_sis.py`. The v1 browser observations used its *actual current time* around 18:49–18:56 and different sample bookings; therefore they are recorded as observations, not as matched controlled test conditions. Final page tests used `?test=1` with 09:00 and test booking 10:00–11:00; T10 used `?test=1&case=t10` and added booking 11:40–12:40.

| Case | Name | Input | Expected | Python v1 | Python final | Page v1 | Page final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | Touching | 660–720 | Available | False | True | Unavailable | Available |
| T2 | Overlap | 630–690 | Unavailable | False | False | Unavailable | Unavailable |
| T3 | Blocked | 660–720, blocked | Unavailable | False | False | Not testable | Unavailable |
| T4 | Exactly 120 min | 720–840 | Available | False | True | Unavailable | Available |
| T5 | 121 min | 720–841 | Unavailable | False | False | Unavailable | Unavailable |
| T6 | Starts now | 540–570 | Unavailable | False | False | Unavailable | Unavailable |
| T7 | Reversed | 720–660 | Unavailable | False | False | Unavailable | Unavailable |
| T8 | Ends at midnight | 1380–1440 | Available | False | True | Not testable | Not testable |
| T9 | Past midnight | 1380–1441 | Unavailable | False | False | Not testable | Not testable |
| T10 | Second booking | 720–780, existing (600–660), (700–760) | Unavailable | False | False | Not testable | Unavailable |
| T11 | Same check twice | 660–720, twice | Available | False | True | Unavailable | Available |
| T12 | Narrow screen | T1 at ~375 px wide | Available | n/a | n/a | Unavailable | Available |

**Important observation limits:** In v1, T1–T7, T11 and T12 were affected by the real time (around 18:49–18:56); the displayed result did not isolate the requested rule. T3 could not be reproduced because the blocked room was not selectable. T8/T9 were not representable in the browser's 24-hour input, and T10 lacked the extra fictional booking in unchanged v1. T11's visible captures show Unavailable on v1 and Available on final, but the images alone do not prove a second button press; verify that interaction personally before declaring a full repeatability test. T9 was explicitly reported Not testable on final. T9 on v1 is also marked Not testable because the native input cannot represent 24:01; it was not separately demonstrated in an image.

## 6. Traceability

| AC | Implementation / file | Test input | Expected | v1 actual | Final actual |
| --- | --- | --- | --- | --- | --- |
| AC1 | `code/booking.py`; `web/final/src/availability.ts` | T6, T7, T8, T9 | Reject invalid/future-start failures; allow end 1440 in Python | Python T8 False; page v1 uses real time | Python T8 True; Page T6/T7 Unavailable; T8/T9 Not testable in browser |
| AC2 | `code/booking.py`, duration condition | T4, T5 | Exactly 120 allowed, 121 rejected | Python T4 False | Python T4 True; Page T4 Available and T5 Unavailable |
| AC3 | `code/booking.py`; `web/final/src/App.tsx` | T3 | Blocked room rejected | Python False; v1 page cannot select blocked room | Python False; Page Unavailable with blocked reason |
| AC4 | `code/booking.py`, overlap; `web/final/src/availability.ts` | T1, T2, T10 | Touching allowed; conflicts rejected | Python T1 False; v1 page used real time | Python T1 True; Page T1 Available, T2/T10 Unavailable |
| AC5 | `code/booking.py`, no mutations | T11 | Same result on repeats; input unchanged | Python T11 False | Python T11 True and mutation tests OK; page shows Available |
| AC6 | `web/final/src/App.tsx`; `src/components/RoomList.tsx` | T12 at 375 px | Usable narrow layout; clear reasons | v1 showed Unavailable at real time; blocked-room selection disabled | final T12 Available at 375 px; readable form and feedback |

## 7. Issue log

| # | Issue | Reproduction | Priority | Prompt / change | Retest result |
| --- | --- | --- | --- | --- | --- |
| 1 | Blocked Faculty Lounge could not be selected to display a clear failure reason. | AC3 / T3: click Faculty Lounge on original page and try 22:00–22:30. | Medium | Week 06 focused repair suggestion: "In the current prototype, clicking the blocked Faculty Lounge room produces no selection or availability result, but AC3 requires the request to be rejected as Unavailable when the selected room is blocked. Make the smallest change that fixes this behavior. Preserve the other acceptance criteria. Explain which file/component you changed and why." Final `RoomList.tsx` permits selection while `App.tsx` reports the blocked reason. Verify the original prompt was sent before claiming it as the Bolt exchange. | Observed final selection of Faculty Lounge and Unavailable message "currently blocked" at 22:00–22:30. Screenshots before/after support this. |
| 2 | Repeated maximum-length wording and unnecessary UI clutter in the original checker. | AC6: compare original "Checking Thesis Hall · Max length 120 min" with final "Checking Thesis Hall". | Low | Week 06 focused suggestion: "Review only the validation feedback in the App.tsx component for unnecessary duplication, confusing naming, or UI feedback problems. Suggest one small cleanup. Do not add features or redesign the whole application. Implement it only if it preserves AC1–AC6." Final banner removes duplicate max-duration label while checker still rejects 121 minutes. Confirm the full Bolt transcript separately. | Observed final T5 Unavailable with explicit 121-minute error; final page banner no longer repeats max-length copy. |

**Before / after:** Issue 1 — `evidence/before-1.png` shows blocked Faculty Lounge not selectable in v1, and `evidence/after-1.png` shows the final blocked-room Unavailable reason. Issue 2 is supported by the original/final screenshots and visible component change; no separate dedicated second before/after pair is claimed.

## 8. Critique decisions

These are verified evaluations of AI statements/suggestions in the actual conversations; the original full Critique exchange still needs to be attached in Section 11.

| # | AI claim or recommendation | How I verified it | Decision | Reason (AC or case) |
| --- | --- | --- | --- | --- |
| 1 | The original Python v1 uses datetime arguments and does not implement the fixed five-argument SIS contract. | Read original `booking_v1.py`; checker returned False for all T1–T11 and final tests passed. | Accept | AC1/AC3: no `now`, no `blocked`; signature differs. |
| 2 | The final interface should allow checking a blocked room and explain why it is unavailable. | Compare before-1 and after-1 screenshots; final Faculty Lounge at 22:00–22:30 showed blocked reason. | Accept | AC3/AC6: explicit feedback, with no booking created. |
| 3 | Running T1 at 11:00–12:00 on original page is enough to evaluate touching endpoints. | v1 was using current time 18:49 and different booking data; it rejected the slot for being in the past. | Modify | AC1/AC4: this observation does not isolate endpoint logic. Record as Unavailable with a limitation, not as a valid AC4 failure. |

## 9. Coding-agent analysis

### 9.1 The loop

| Step | What happened in this assignment |
| --- | --- |
| User goal | Check study room availability under AC1–AC6 without creating reservations or storing user data. |
| Model / plan | ChatGPT suggested validation order and boundary tests; Bolt.new generated a one-page UI with sample bookings. |
| Tool call | Bolt.new visibly read six project files and performed five actions during initial generation; VS Code and the terminal ran local checks. |
| Observation | Python checker executed 30 tests successfully; browser captures showed blocked-room feedback and correct overlap results in controlled test mode. |
| Next step | Fixed the blocked-room selection/feedback, confirmed mobile layout, and compared v1 and final outputs with T1–T12. |
| Human review | The user ran Git, Python checker and browser tests, checked screenshots, and identified real-time clock confounding in original v1. |

### 9.2 Context, tools and permissions

| Tool | Context it used | Tools or permissions | Observed or assumed |
| --- | --- | --- | --- |
| ChatGPT (web) | Assignment AC1–AC6, pasted Python v1, error outputs, browser screenshots | Read messages and suggest report text, code, and commands; did not directly change the user's local repository | Observed |
| Bolt.new | Initial room availability prompt and existing React project files | Read 6 files and took 5 actions in the project as shown in its activity; generated/editable source files | Observed |
| Git and VS Code local terminal | Local `sis-03/` repository, test scripts and Vite exports | Ran `git`, `py`, `npm` commands under the user's account | Observed |
| Bolt.new internal planning | Its private intermediate reasoning and file selection criteria | Internal agent decisions beyond the visible action summary were not accessible | Assumed |

### 9.3 Checkpoint and dependability

**Safety checkpoint:** Before accepting a generated change, I checked that the web export contained no backend, database access, login form, `.env` secrets, or external API calls; I also kept the original v1 intact. I verified the changes against AC1–AC6 with repeatable cases rather than trusting the assistant's summary. This was a checkpoint on scope and safety, not a claim that every possible security issue was tested.

**Reliability, security, responsibility:** Reliability depends on correct edge cases such as 120 versus 121 minutes, touching intervals, and blocked rooms. A page using the live clock can give misleading comparison results, so the final app includes a controlled `?test=1` mode. Security risk increases if an AI adds unnecessary backend, network, or storage code; these were excluded and checker W3 previously passed. The student remains responsible for verifying output, choosing what to accept or modify, protecting credentials, and documenting any untested behavior. A passing structural checker cannot replace a human explanation and real browser testing.

## 10. Reflection

**WRITE YOUR OWN 100–200 WORDS BEFORE SUBMISSION.** In SIS 03, I used ChatGPT to help with Python code and Bolt.new to build the web page. Python was easier to test because I had 30 automatic tests. Bolt.new was faster for making the page, but I needed to check the buttons and messages myself.

I found three risks. First, AI can use the wrong time rules. Second, a page can give a bad message when a room is blocked. Third, extra backend or database code can create security problems. I checked the results with tests and real screenshots.

I changed one AI idea about test T1. The old page used the real time, so its result could not prove that touching bookings worked. I used a test mode with 09:00 for the final page. I am responsible for checking my work and keeping the project simple. Next, I want to improve testing for 24:00.

## 11. Appendix A — AI exchanges

> **Incomplete primary records:** Dates for B2 and B4 are provisional (saved file / earlier discussion), and the historical exact model names must still be verified. The original full transcript of four AI exchanges was not supplied. The entries below preserve only authentic prompts, response excerpts or code artifacts that can be recovered, and explicitly state which full responses are missing. Recover the complete prompts and answers from the original chats before claiming that this section satisfies the requirement. Do not fabricate a transcript to make the checker green.

### B1

- **Tool:** ChatGPT (web)
- **Model:** not displayed
- **Date:** 2026-10-09
- **Stage:** Plan
- **Source:** week-05

**Prompt:**

~~~~text
Propose a short implementation plan for can_book. List the checks in order and identify assumptions. Use Python 3 and the supplied rules. Do not write code yet. Suggest boundary cases that could expose an incorrect implementation.
~~~~

**Response:**

~~~~text
FULL ORIGINAL PLAN RESPONSE NOT RECOVERED. The prior discussion confirms that a validation plan was requested, but does not preserve its complete assistant answer. Retrieve the actual assistant message from the Week 05 conversation and replace this disclosure with the word-for-word full response. Do not treat this note as the transcript.
~~~~

### B2

- **Tool:** ChatGPT (web) (original assistant must be verified against Week 05 record)
- **Model:** not displayed
- **Date:** 2026-10-09
- **Stage:** Generate
- **Source:** week-05

**Prompt:**

~~~~text
ORIGINAL PYTHON V1 GENERATION PROMPT NOT RECOVERED. Retrieve the genuine prompt from Week 05 chat. The later generic implementation request should not be substituted for the original prompt because the original code has a different datetime-based function contract.
~~~~

**Response:**

~~~~text
The following is the original saved code artifact transcribed from the user's `code/original/booking_v1.py` output. It is NOT evidence of the full historical AI response; obtain that from the original conversation if available.

from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Any, Dict, Protocol

# Protocol or Dataclass-like structure assumed for type hinting:
# Existing bookings can be tuples/lists of (start, end) or objects with .start and .end attributes.

def can_book(
    booking_start: datetime,
    booking_end: datetime,
    slot_start: datetime,
    slot_end: datetime,
    existing_bookings: List[Any],
    min_duration: Optional[timedelta] = None,
    max_duration: Optional[timedelta] = None,
    step_minutes: Optional[int] = None,
    buffer_minutes: int = 0
) -> bool:
    """
    Evaluates whether a requested booking can be placed.
    Uses half-open intervals [start, end).
    """
    # Helper to pull (start, end) from objects or tuples
    def get_bounds(item: Any) -> Tuple[datetime, datetime]:
        if isinstance(item, (tuple, list)):
            return item[0], item[1]
        return getattr(item, "start"), getattr(item, "end")

    # Condition 1 (AC1): Valid Chronological Order & Duration Constraints
    if booking_start >= booking_end:
        return False

    duration = booking_end - booking_start
    if min_duration and duration < min_duration:
        return False
    if max_duration and duration > max_duration:
        return False

    # Condition 2 (AC2): Slot Boundary Enforcement
    if booking_start < slot_start or booking_end > slot_end:
        return False

    # Condition 3 (AC3): Alignment / Step Granularity Constraints
    if step_minutes and step_minutes > 0:
        start_delta = (booking_start - slot_start).total_seconds() / 60
        end_delta = (booking_end - booking_start).total_seconds() / 60
        if start_delta % step_minutes != 0 or end_delta % step_minutes != 0:
            return False

    # Condition 4 (AC4): Buffer Calculation Setup
    buffer = timedelta(minutes=buffer_minutes)
    buffered_start = booking_start - buffer
    buffered_end = booking_end + buffer

    # Condition 5 (AC5): Overlap Check against Existing Bookings
    for existing in existing_bookings:
        ex_start, ex_end = get_bounds(existing)

        # Overlap rule for half-open intervals [start, end):
        # max(start1, start2) < min(end1, end2)
        if max(buffered_start, ex_start) < min(buffered_end, ex_end):
            return False

    return True
~~~~

### B3

- **Tool:** ChatGPT (web)
- **Model:** not displayed
- **Date:** 2026-10-23
- **Stage:** Critique
- **Source:** this SIS

**Prompt:**

~~~~text
The user pasted the complete Python `booking_v1.py` with its datetime-based signature and checks for duration, slot boundaries, alignment, and overlaps, and asked for the next steps. The exact complete user prompt is visible in the original SIS 03 conversation, not reproduced here as a verified verbatim exchange.
~~~~

**Response:**

~~~~text
PARTIAL PRIOR ASSISTANT REVIEW ONLY: The assistant identified that the original uses datetime rather than integer minutes, lacks a current-time check, makes the 120-minute limit optional, has no blocked-room parameter, and may reject touching intervals when a buffer is used. The complete historical response must be copied directly from the SIS 03 chat; this summary is not a transcript.
~~~~

### B4

- **Tool:** Bolt.new (repair suggestion originally supplied through ChatGPT)
- **Model:** not displayed
- **Date:** 2026-10-21
- **Stage:** Repair
- **Source:** week-06

**Prompt:**

~~~~text
In the current prototype, clicking the blocked Faculty Lounge room produces no selection or availability result, but AC3 requires the request to be rejected as Unavailable when the selected room is blocked. Make the smallest change that fixes this behavior. Preserve the other acceptance criteria. Explain which file/component you changed and why.
~~~~

**Response:**

~~~~text
FULL ORIGINAL BOLT RESPONSE NOT RECOVERED. Observed implementation difference: the final `src/components/RoomList.tsx` allows blocked Faculty Lounge to be selected, and the final page displays Unavailable with a blocked reason. These are source and browser observations, not a word-for-word Bolt agent response. Replace this note with the full Bolt response after checking the original project history.
~~~~

## 12. Appendix B — Test output

### 12.1 Your suite

The following is the output pasted by the user from the real test run `py -m unittest discover -s code -p "test_booking.py" -v` on 2026-10-23. It is not a simulated run.

~~~~text
test_between_two_bookings (test_booking.BookingTests.test_between_two_bookings) ... ok
test_blocked_without_existing (test_booking.BookingTests.test_blocked_without_existing) ... ok
test_contains_booking (test_booking.BookingTests.test_contains_booking) ... ok
test_empty_existing (test_booking.BookingTests.test_empty_existing) ... ok
test_free_between_bookings (test_booking.BookingTests.test_free_between_bookings) ... ok
test_identical_booking (test_booking.BookingTests.test_identical_booking) ... ok
test_inside_booking (test_booking.BookingTests.test_inside_booking) ... ok
test_negative_start (test_booking.BookingTests.test_negative_start) ... ok
test_now_zero_start_one (test_booking.BookingTests.test_now_zero_start_one) ... ok
test_now_zero_start_zero (test_booking.BookingTests.test_now_zero_start_zero) ... ok
test_one_minute_after_now (test_booking.BookingTests.test_one_minute_after_now) ... ok
test_one_minute_duration (test_booking.BookingTests.test_one_minute_duration) ... ok
test_partial_overlap_at_start (test_booking.BookingTests.test_partial_overlap_at_start) ... ok
test_starts_in_past (test_booking.BookingTests.test_starts_in_past) ... ok
test_t10_second_booking_overlap (test_booking.BookingTests.test_t10_second_booking_overlap) ... ok
test_t11_repeat_does_not_mutate (test_booking.BookingTests.test_t11_repeat_does_not_mutate) ... ok
test_t1_touching_end (test_booking.BookingTests.test_t1_touching_end) ... ok
test_t2_overlap (test_booking.BookingTests.test_t2_overlap) ... ok
test_t3_blocked (test_booking.BookingTests.test_t3_blocked) ... ok
test_t4_exactly_120 (test_booking.BookingTests.test_t4_exactly_120) ... ok
test_t5_121_minutes (test_booking.BookingTests.test_t5_121_minutes) ... ok
test_t6_starts_now (test_booking.BookingTests.test_t6_starts_now) ... ok
test_t7_reversed (test_booking.BookingTests.test_t7_reversed) ... ok
test_t8_midnight_end (test_booking.BookingTests.test_t8_midnight_end) ... ok
test_t9_after_midnight (test_booking.BookingTests.test_t9_after_midnight) ... ok
test_touching_at_start (test_booking.BookingTests.test_touching_at_start) ... ok
test_unsorted_existing (test_booking.BookingTests.test_unsorted_existing) ... ok
test_unsorted_inputs_unchanged_on_accepted (test_booking.BookingTests.test_unsorted_inputs_unchanged_on_accepted) ... ok
test_unsorted_inputs_unchanged_on_rejected (test_booking.BookingTests.test_unsorted_inputs_unchanged_on_rejected) ... ok
test_zero_duration (test_booking.BookingTests.test_zero_duration) ... ok

----------------------------------------------------------------------
Ran 30 tests in 0.007s

OK
~~~~

### 12.2 Path B only — three faults you planted

| # | Line you broke | AC | Test that failed |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

## 13. Remaining limitations and known fails

The latest SIS 03 checker result is **pass=54 fail=1 error=0**. Most checks passed. The only remaining failed check is X2 because some original AI responses could not be recovered.

| Check ID or limitation | Why it stays | What I would do next |
| --- | --- | --- |
| X2: AI responses | Some full AI responses from earlier chats are missing. I kept the original prompts and available information. I did not create fake responses. | Find the original AI chats and add the full responses if they are available. |
| T8/T9: Time input | The browser does not allow 24:00 or 24:01 in the time field. | Keep these cases as Not testable for the page and use Python tests. |
| T10: Original page | The original page does not have the second test booking. | Use Not testable for the original page and explain the reason. |
| T11: Repeat check evidence | The screenshots do not prove that the button was pressed two times. | Check the same time slot twice and record both results. |
| Original page time | The original page uses real time, not fixed test time. | Use test mode in the final page for better testing. |
| Original backend code | The first web version has some extra backend or database code. | Keep the original version unchanged and use a simple client-only final page. |

I checked the Python function with 30 tests. All 30 tests passed. The final web page works on desktop and mobile. The original AI responses are the main missing evidence.