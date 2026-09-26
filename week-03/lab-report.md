

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