import unittest
from booking import can_book

class TestCanBook(unittest.TestCase):

    # --- 6 Base Cases from Handout ---
    def test_base_touching(self):
        # Touching endpoints allowed (660, 720) with existing [(600, 660)]
        self.assertTrue(can_book(660, 720, 540, False, [(600, 660)]))

    def test_base_overlap(self):
        # Overlaps existing [(600, 660)]
        self.assertFalse(can_book(630, 690, 540, False, [(600, 660)]))

    def test_base_blocked(self):
        # Room is blocked
        self.assertFalse(can_book(660, 720, 540, True, [(600, 660)]))

    def test_base_exactly_2_hours(self):
        # Duration exactly 120 min
        self.assertTrue(can_book(720, 840, 540, False, [(600, 660)]))

    def test_base_over_2_hours(self):
        # Duration 121 min (> 120)
        self.assertFalse(can_book(720, 841, 540, False, [(600, 660)]))

    def test_base_starts_now(self):
        # start == now (must be start > now)
        self.assertFalse(can_book(540, 570, 540, False, [(600, 660)]))

    # --- Mandatory Further Kinds ---
    def test_zero_length_time(self):
        # start == end (0 length)
        self.assertFalse(can_book(600, 600, 540, False, []))

    def test_reversed_times(self):
        # start > end
        self.assertFalse(can_book(700, 600, 540, False, []))

    def test_day_bounds_out_of_range(self):
        # end > 1440
        self.assertFalse(can_book(1400, 1441, 540, False, []))

    def test_empty_existing_bookings(self):
        # Valid booking with empty existing list
        self.assertTrue(can_book(600, 660, 540, False, []))

    def test_multiple_existing_no_overlap(self):
        # Fits neatly between existing [(600, 660), (780, 840)]
        self.assertTrue(can_book(660, 780, 540, False, [(600, 660), (780, 840)]))

    def test_existing_input_unchanged(self):
        # Verify existing list is never mutated
        existing = [(600, 660)]
        existing_copy = list(existing)
        can_book(660, 720, 540, False, existing)
        self.assertEqual(existing, existing_copy)

    # --- Additional Edge Cases to Catch M7, M8, M10 ---
    def test_overlap_enclosure(self):
        # Catches M7: Requested booking is inside existing booking (600, 720)
        self.assertFalse(can_book(630, 690, 540, False, [(600, 720)]))

    def test_overlap_partial_end(self):
        # Catches M8: Requested booking starts before existing and ends inside it
        self.assertFalse(can_book(580, 630, 540, False, [(600, 660)]))

    def test_returns_strict_boolean(self):
        # Catches M10: Verifies output is pure bool (type bool)
        result = can_book(660, 720, 540, False, [(600, 660)])
        self.assertIsInstance(result, bool)
        self.assertTrue(result is True)

if __name__ == '__main__':
    unittest.main()