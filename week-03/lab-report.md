

Below is a scenario-bounded requirements artifact for the **Smart Campus Study Room Booking System**.

### Student Goals

* Find available study rooms.
* Book a suitable room for studying.
* View and manage personal bookings.
* Cancel a booking when the room is no longer needed.

### Administrator Goals

* Manage study room availability.
* Monitor and manage bookings.
* Ensure booking rules are followed.

### User Stories

| ID    | User Story                                                                                                             | Priority | Assumption                                                           |
| ----- | ---------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------- |
| US-01 | **As a Student, I want to view available study rooms, so that I can choose a room for studying.**                      | High     | Room availability information is maintained by the system.           |
| US-02 | **As a Student, I want to book an available study room, so that I can reserve it for my study session.**               | High     | Students can only book rooms that are currently available.           |
| US-03 | **As a Student, I want to view my bookings, so that I can check my upcoming study room reservations.**                 | Medium   | The system stores each student's confirmed bookings.                 |
| US-04 | **As a Student, I want to cancel my booking, so that the room becomes available when I no longer need it.**            | Medium   | A student can cancel only their own booking.                         |
| US-05 | **As an Administrator, I want to manage study room availability, so that students can see which rooms can be booked.** | High     | Administrators are authorized to update room availability.           |
| US-06 | **As an Administrator, I want to view study room bookings, so that I can monitor reservations across the campus.**     | High     | Administrators can access booking information for managed rooms.     |
| US-07 | **As an Administrator, I want to manage bookings, so that I can maintain an accurate booking schedule.**               | High     | Administrators are authorized to modify or manage existing bookings. |
| US-08 | **As an Administrator, I want to enforce booking rules, so that study rooms are used according to campus policies.**   | High     | The system has defined booking rules provided by the campus.         |

**Priority meaning:**

* **High** — essential for the core booking system.
* **Medium** — useful for managing existing bookings but not the basic booking operation.



## 3. Review of user stories

### US-01
**Decision:** Keep.

**Reason:** The story names the Student actor, describes one valuable outcome,
is testable, and directly matches UC-01 View availability.

### US-02
**Decision:** Keep.

**Reason:** The story names the Student actor, describes the booking goal,
and directly matches UC-02 Book room. The booking business rules can be tested
through acceptance criteria.

### US-03
**Decision:** Delete.

**Reason:** "View my bookings" is not one of the six fixed use cases in the
scenario. The scenario does not define a separate use case for viewing personal
bookings.

### US-04
**Decision:** Keep.

**Reason:** The story describes the Student goal of cancelling a booking and
matches UC-03 Cancel booking.

### US-05
**Decision:** Rewrite.

**Reason:** "Manage study room availability" is too broad. The scenario defines
the specific administrator function UC-04 Block or unblock room. The revised
story uses that exact business goal.

### US-06
**Decision:** Rewrite.

**Reason:** "View study room bookings" does not directly match UC-05 Review usage,
which is specifically about seeing how rooms are being used over a period. The
story was rewritten to match the fixed use case.

### US-07
**Decision:** Delete.

**Reason:** "Manage bookings" is not one of the six fixed use cases and is too
broad to be a single testable requirement within the supplied scenario.

### US-08
**Decision:** Delete.

**Reason:** "Enforce booking rules" describes general system behavior rather than
a distinct goal of the Student or Administrator. The four business rules are
constraints on the booking behavior and should be tested through acceptance
criteria rather than treated as a separate use case.



Open Questions Decisions & System AssumptionsRule R2 Boundary: A booking duration of exactly two hours is allowed ($\le 2$ hours). A duration exceeding two hours is rejected.   Rule R3 Boundary: A booking that ends exactly when another begins does NOT overlap (e.g., Slot 10:00–11:00 and Slot 11:00–12:00 do not overlap).   All booking operations must reference time slots in the future relative to the system's current time.   Acceptance CriteriaUS-01: View Available Study RoomsAC-01-01: Successful Viewing of Free Time Slots (Happy Path)Given the student selects a valid future date and a specific study room,   When the student requests room availability,   Then the system displays all time slots currently marked as free for that room on that date.   AC-01-02: Viewing Blocked or Booked Rooms (Validation Path)Given a study room is blocked by an Administrator or already reserved for a specific time slot,   When the student views availability for that time slot,   Then the system marks that specific time slot as unavailable and hides the option to book it.   AC-01-03: Invalid Date Request (Error / Alternative Case)Given the student selects a date or time in the past,   When the student submits the availability search request,   Then the system rejects the request and displays an error message stating that availability can only be checked for future time slots.   US-02: Book a Study RoomAC-02-01: Successful Room Reservation (Happy Path)Given a study room is free for a 1-hour time slot starting in the future,   When the student submits a booking request for that room and time slot,   Then the system reserves the room, updates its status to booked, and triggers a booking confirmation.   AC-02-02: Back-to-Back Booking at Boundary (Boundary Case - R3)Given Room A is already booked from 10:00 to 11:00 on a future date,   When another student submits a booking request for Room A from 11:00 to 12:00 on the same date,   Then the system accepts the booking without detecting an overlap error.   AC-02-03: Exceeding Maximum Duration (Validation / Error Case - R2)Given a student selects a free room starting in the future,   When the student attempts to request a single booking duration of 2 hours and 15 minutes,   Then the system rejects the booking request with an error message stating that the maximum allowed booking duration is 2 hours.   AC-02-04: Booking Overlap Conflict (Error Case - R3)Given Room B is booked from 14:00 to 16:00,   When a student attempts to book Room B from 15:00 to 16:00 on the same date,   Then the system rejects the booking and displays a conflict notification stating the room is already reserved.   AC-02-05: Booking Blocked Room Attempt (Error Case - R4)Given Room C is marked as blocked by an Administrator,   When a student attempts to book Room C for any future time slot,   Then the system prevents the booking with a message stating the room is currently out of service.   US-03: Cancel an Existing BookingAC-03-01: Successful Booking Cancellation (Happy Path)Given a student has an active future booking for Room A,   When the student submits a cancellation request for this booking,   Then the system releases the reservation, marks the time slot as free, and triggers a cancellation confirmation.   AC-03-02: Attempting to Cancel Past Booking (Error Case - R1)Given a reservation was made for a time slot that has already passed,   When the student attempts to cancel the reservation,   Then the system denies the request and displays an error message stating past bookings cannot be cancelled.   AC-03-03: Cancellation of Unowned or Invalid Booking (Validation / Error Case)Given a booking ID does not belong to the requesting student or does not exist,   When the student attempts to submit a cancellation request,   Then the system denies the action and displays an unauthorized or invalid booking error message. 

# Диаграмма PlantUML
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Student" as student
actor "Administrator" as admin

rectangle "Smart Campus Study Room Booking System" {
  usecase "View Availability" as UC_View
  usecase "Book Room" as UC_Book
  usecase "Cancel Booking" as UC_Cancel
  usecase "Block or Unblock Room" as UC_Block
  usecase "Review Usage" as UC_Review
  usecase "Send Confirmation" as UC_Confirm

  ' Include relationship: Booking a room always triggers a confirmation
  UC_Book .> UC_Confirm : <<include>>
}

' Student Associations
student -- UC_View
student -- UC_Book
student -- UC_Cancel

' Administrator Associations
admin -- UC_Block
admin -- UC_Review
@enduml