US-01
As a Student, I want to view available study rooms, so that I can choose a room for studying.

Priority: High
Assumption: Availability information reflects whether a room is free for a requested time slot.


US-02
As a Student, I want to book an available study room, so that I can reserve it for my study session.

Priority: High
Assumption: A student can book a room only when the selected time slot is available and the booking satisfies the business rules.
UC-02 Book room

US-03
As a Student, I want to cancel my booking, so that the room becomes available when I no longer need it.

Priority: Medium
Assumption: A student can cancel only a booking that they made.
UC-03 Cancel booking

US-04
As an Administrator, I want to block or unblock a study room, so that I can control whether the room is available for booking.

Priority: High
Assumption: An Administrator can change a room between blocked and available states.
Это наша rewritten US-05.
Причина rewrite:

manage study room availability was too broad; the scenario defines the specific function UC-04 Block or unblock room.


US-05
As an Administrator, I want to review study room usage over a period, so that I can monitor how the rooms are being used.

Priority: Medium
Assumption: Usage information is available for the selected period.

Это rewrite исходной US-06.
Почему?

Потому что scenario говорит именно:

UC-05 Review usage
See how rooms are being used over a period.


А AI написал:

view study room bookings

Это не обязательно то же самое, что review usage.



US-06
US-06
As a Student, I want to receive a confirmation when my booking or cancellation is completed, so that I know the action was confirmed.

Priority: Medium
Assumption: The system sends a confirmation after a successful booking or cancellation.
Это соответствует:

UC-06 Send confirmation
Здесь важно: мы не добавляем SMS/push/reminders. Scenario разрешает confirmation через UC-06, но out-of-scope запрещает дополнительные notification types.




