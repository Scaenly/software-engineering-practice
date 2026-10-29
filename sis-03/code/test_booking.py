import unittest
from booking import can_book


class BookingTests(unittest.TestCase):
    def check(self, start, end, expected, now=540, blocked=False, existing=None):
        if existing is None:
            existing = [(600, 660)]
        result = can_book(start, end, now, blocked, existing)
        self.assertIs(result, expected)

    def test_t1_touching_end(self):
        self.check(660, 720, True)

    def test_t2_overlap(self):
        self.check(630, 690, False)

    def test_t3_blocked(self):
        self.check(660, 720, False, blocked=True)

    def test_t4_exactly_120(self):
        self.check(720, 840, True)

    def test_t5_121_minutes(self):
        self.check(720, 841, False)

    def test_t6_starts_now(self):
        self.check(540, 570, False)

    def test_t7_reversed(self):
        self.check(720, 660, False)

    def test_t8_midnight_end(self):
        self.check(1380, 1440, True)

    def test_t9_after_midnight(self):
        self.check(1380, 1441, False)

    def test_t10_second_booking_overlap(self):
        self.check(720, 780, False, existing=[(600, 660), (700, 760)])

    def test_t11_repeat_does_not_mutate(self):
        existing = [(600, 660)]
        before = existing.copy()
        self.assertIs(can_book(660, 720, 540, False, existing), True)
        self.assertIs(can_book(660, 720, 540, False, existing), True)
        self.assertEqual(existing, before)

    def test_zero_duration(self):
        self.check(700, 700, False)

    def test_negative_start(self):
        self.check(-30, 30, False)

    def test_starts_in_past(self):
        self.check(500, 530, False)

    def test_one_minute_after_now(self):
        self.check(541, 571, True)

    def test_now_zero_start_zero(self):
        self.check(0, 60, False, now=0)

    def test_now_zero_start_one(self):
        self.check(1, 61, True, now=0)

    def test_one_minute_duration(self):
        self.check(720, 721, True)

    def test_blocked_without_existing(self):
        self.check(660, 720, False, blocked=True, existing=[])

    def test_touching_at_start(self):
        self.check(570, 600, True)

    def test_between_two_bookings(self):
        self.check(660, 720, True, existing=[(600, 660), (720, 780)])

    def test_inside_booking(self):
        self.check(615, 645, False)

    def test_contains_booking(self):
        self.check(570, 690, False)

    def test_identical_booking(self):
        self.check(600, 660, False)

    def test_partial_overlap_at_start(self):
        self.check(570, 630, False)

    def test_unsorted_existing(self):
        self.check(610, 650, False, existing=[(900, 960), (600, 660)])

    def test_empty_existing(self):
        self.check(600, 660, True, existing=[])

    def test_free_between_bookings(self):
        self.check(760, 800, True, existing=[(600, 660), (700, 760), (800, 860)])

    def test_unsorted_inputs_unchanged_on_accepted(self):
        existing = [(900, 960), (600, 660), (700, 760)]
        before = existing.copy()
        self.assertIs(can_book(780, 840, 540, False, existing), True)
        self.assertEqual(existing, before)

    def test_unsorted_inputs_unchanged_on_rejected(self):
        existing = [(900, 960), (600, 660), (700, 760)]
        before = existing.copy()
        self.assertIs(can_book(610, 650, 540, False, existing), False)
        self.assertEqual(existing, before)


if __name__ == '__main__':
    unittest.main()
