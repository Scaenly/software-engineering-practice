# Acceptance Criteria

## Open Questions Decisions & System Assumptions
* Rule R2 Boundary: A booking duration of exactly two hours is allowed (<= 2 hours). A duration exceeding two hours is rejected.
* Rule R3 Boundary: A booking that ends exactly when another begins does NOT overlap (e.g., Slot 10:00–11:00 and Slot 11:00–12:00 do not overlap).
* System Assumption: All booking operations must reference time slots in the future relative to the system's current time.

---

## US-01: View Available Study Rooms

### AC-01-01: Successful Viewing of Free Time Slots (Happy Path)
Given the student selects a valid future date and a specific study room,
When the student requests room availability,
Then the system displays all time slots currently marked as free for that room on that date.

### AC-01-02: Viewing Blocked or Booked Rooms (Validation Path)
Given a study room is blocked by an Administrator or already reserved for a specific time slot,
When the student views availability for that time slot,
Then the system marks that specific time slot as unavailable and hides the option to book it.

### AC-01-03: Invalid Date Request (Error / Alternative Case)
Given the student selects a date or time in the past,
When the student submits the availability search request,
Then the system rejects the request and displays an error message stating that availability can only be checked for future time slots.

---

## US-02: Book a Study Room

### AC-02-01: Successful Room Reservation (Happy Path)
Given a study room is free for a 1-hour time slot starting in the future,
When the student submits a booking request for that room and time slot,
Then the system reserves the room, updates its status to booked, and triggers a booking confirmation.

### AC-02-02: Back-to-Back Booking at Boundary (Boundary Case - R3)
Given Room A is already booked from 10:00 to 11:00 on a future date,
When another student submits a booking request for Room A from 11:00 to 12:00 on the same date,
Then the system accepts the booking without detecting an overlap error.

### AC-02-03: Exceeding Maximum Duration (Validation / Error Case - R2)
Given a student selects a free room starting in the future,
When the student attempts to request a single booking duration of 2 hours and 15 minutes,
Then the system rejects the booking request with an error message stating that the maximum allowed booking duration is 2 hours.

### AC-02-04: Booking Overlap Conflict (Error Case - R3)
Given Room B is booked from 14:00 to 16:00,
When a student attempts to book Room B from 15:00 to 16:00 on the same date,
Then the system rejects the booking and displays a conflict notification stating the room is already reserved.

### AC-02-05: Booking Blocked Room Attempt (Error Case - R4)
Given Room C is marked as blocked by an Administrator,
When a student attempts to book Room C for any future time slot,
Then the system prevents the booking with a message stating the room is currently out of service.

---

## US-03: Cancel an Existing Booking

### AC-03-01: Successful Booking Cancellation (Happy Path)
Given a student has an active future booking for Room A,
When the student submits a cancellation request for this booking,
Then the system releases the reservation, marks the time slot as free, and triggers a cancellation confirmation.

### AC-03-02: Attempting to Cancel Past Booking (Error Case - R1)
Given a reservation was made for a time slot that has already passed,
When the student attempts to cancel the reservation,
Then the system denies the request and displays an error message stating past bookings cannot be cancelled.

### AC-03-03: Cancellation of Unowned or Invalid Booking (Validation / Error Case)
Given a booking ID does not belong to the requesting student or does not exist,
When the student attempts to submit a cancellation request,
Then the system denies the action and displays an unauthorized or invalid booking error message.