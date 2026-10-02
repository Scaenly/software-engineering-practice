# Practice 04 Lab Report: Modeling the System with UML

**Author:** [Your Name]  
**Course:** AI-Driven Software Engineering  
**Date:** October 1, 2026  

---

## 1. Selected AI Assistant & Model
- **AI Tool:** ChatGPT / Claude
- **Exact Model Version:** GPT-4o (Version 2024-08-06)

---

## 2. Approved User Stories & Assumptions
See `models/approved-stories.md` for full user stories US-01 through US-06 and explicit edge-case declarations.

---

## 3. Review Findings: Use Case Diagram (§3)
- **Actor Goal Alignment:** Student and Administrator are outside the system boundary. Student is associated only with goals UC1, UC2, UC3. Administrator is associated with UC4, UC5, UC6.
- **`<<include>>` Justification:** UC2 (Book Room) includes UC7 (Validate Booking Rules) because rule checking (R1, R2, R3) is mandatory during every booking attempt.
- **Original AI Errors Identified:** The original draft lacked system boundary naming and contained unanchored validation use cases without stereotype reasons.

---

## 4. Review Findings: Class Diagram (§4)
- **Domain Focus:** Contains pure domain entities (`Student`, `Room`, `Booking`). Excluded technical artifacts like controllers or repositories.
- **Multiplicities (Read Both Ways):**
  - `Student 1 -- 0..* Booking`: One student makes zero to many bookings; each booking belongs to exactly one student.
  - `Room 1 -- 0..* Booking`: One room has zero to many bookings; each booking is tied to exactly one room.
- **Rule Representation:** R2 (overlapping check) cannot be represented as simple multiplicity; it is explicitly captured in a PlantUML `note` block attached to `Booking`.
- **Original AI Errors Identified:** AI assigned `1..*` on `Booking`, implying every room must have an existing booking upon creation. Corrected to `0..*`.

---

## 5. Review Findings: Behaviour Diagram — Sequence Diagram (§5)
- **Validation Order:** R1 (time/duration) is validated prior to database/repository query. R3 (blocked status) and R2 (overlaps) are checked before creation.
- **No Creation on Failure:** `createBooking` is called only in the innermost successful `alt` path.
- **Original AI Errors Identified:** AI skipped explicit R1 time range validation and saved bookings before checking for overlap.

---

## 6. Critique Findings (§6)

| # | Source Diagram | Identified Issue | Proposed Correction | Verdict | Reason |
|---|---|---|---|---|---|
| 1 | Use Case | Missing explicit link to R1-R4 rules in use cases | Added `<<include>>` relationship to `Validate Booking Rules` | Accepted | Ensures rule validation is explicitly represented |
| 2 | Class | `Booking` multiplicity on `Student` was `1..*` | Changed to `0..*` | Accepted | Students exist before making any bookings |
| 3 | Sequence | R1 validation skipped in sequence flow | Inserted explicit `validateTimeRange` activation | Accepted | Required by rule R1 prior to persistence |

---

## 7. Requirement Tracing Matrix (§7)

| Requirement / Story | Model Element(s) | Status |
|---|---|---|
| **R1 (Future start, 0 < duration <= 2h)** | Class: Note; Sequence: `validateTimeRange` | Covered |
| **R2 (No overlapping active bookings)** | Class: Note; Sequence: `checkRoomStatus` | Covered |
| **R3 (Blocked room accepts no booking)** | Class: `Room.isBlocked`; Sequence: `checkRoomStatus` | Covered |
| **R4 (Successful booking confirmation)** | Class: `Booking`; Sequence: `confirmation` message | Covered |
| **US-01 (View Availability)** | Use Case: `UC1` | Covered |
| **US-02 (Book Room)** | Use Case: `UC2`; Sequence Diagram | Covered |
| **US-03 (Cancel Booking)** | Use Case: `UC3`; Class: `Booking.cancel()` | Covered |
| **US-04 (Block Room)** | Use Case: `UC4`; Class: `Room.blockRoom()` | Covered |
| **US-05 (Unblock Room)** | Use Case: `UC5`; Class: `Room.unblockRoom()` | Covered |
| **US-06 (Review Usage)** | Use Case: `UC6` | Covered |

---

## 8. Change Log (§8)

- **Use Case Diagram:** Renamed system boundary to `Smart Campus System`; added explicit comment explaining `<<include>>` reason for UC7.
- **Class Diagram:** Corrected `Booking` multiplicity from `1..*` to `0..*`; added explicit domain method names and rule note.
- **Sequence Diagram:** Added R1 guard branch (`validateTimeRange`); ensured failure paths exit cleanly without calling repository creation.

---

## 9. Checker Results (§9)

### `python tests/check_models.py` Output:
```text
============================================================
Smart Campus UML Model Checker Results
============================================================
[PASS] UC-01: Use case file exists and is non-empty
[PASS] UC-02: Actor Student found
[PASS] UC-03: Actor Administrator found
[PASS] UC-04: System boundary present
[PASS] UC-05: Standard stereotyping used correctly
[PASS] CL-01: Class file exists and is non-empty
[PASS] CL-02: Class Student present
[PASS] CL-03: Class Room present
[PASS] CL-04: Class Booking present
[PASS] CL-05: Multiplicities defined on associations
[PASS] CL-06: R2 captured in note block
[PASS] SQ-01: Sequence file exists and is non-empty
[PASS] SQ-02: Student lifeline present
[PASS] SQ-03: BookingService lifeline present
[PASS] SQ-04: BookingRepository lifeline present
[PASS] SQ-05: Alt frame present for alternatives
[PASS] SQ-06: Confirmation return message present
...
------------------------------------------------------------
SUMMARY: 37 tests run, 37 PASS, 0 FAIL, 0 ERROR
============================================================