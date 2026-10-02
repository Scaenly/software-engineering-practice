# Approved User Stories

## US-01 — View available study rooms

As a Student, I want to view available study rooms, so that I can choose a room for studying.

**Priority:** High

**Assumption:** Availability information reflects whether a room is free for a requested time slot.

## US-02 — Book an available study room

As a Student, I want to book an available study room, so that I can reserve it for my study session.

**Priority:** High

**Assumption:** A student can book a room only when the selected time slot is available and the booking satisfies the business rules.

## US-03 — Cancel booking

As a Student, I want to cancel my booking, so that the room becomes available when I no longer need it.

**Priority:** Medium

**Assumption:** A student can cancel only a booking that they made.

## US-04 — Block or unblock a study room

As an Administrator, I want to block or unblock a study room, so that I can control whether the room is available for booking.

**Priority:** High

**Assumption:** An Administrator can change a room between blocked and available states.

**Rewrite reason:** "Manage study room availability" was too broad; the scenario defines the specific function UC-04 Block or unblock room.

## US-05 — Review study room usage

As an Administrator, I want to review study room usage over a period, so that I can monitor how the rooms are being used.

**Priority:** Medium

**Assumption:** Usage information is available for the selected period.

**Rewrite reason:** The scenario specifies UC-05 Review usage: "See how rooms are being used over a period." The previous AI story "view study room bookings" was not necessarily equivalent to reviewing usage.

## US-06 — Receive confirmation

As a Student, I want to receive a confirmation when my booking or cancellation is completed, so that I know the action was confirmed.

**Priority:** Medium

**Assumption:** The system sends a confirmation after a successful booking or cancellation.

**Scope note:** No SMS, push notifications, reminders, or other notification types are added. The scenario only permits the confirmation behavior defined by UC-06 Send confirmation.