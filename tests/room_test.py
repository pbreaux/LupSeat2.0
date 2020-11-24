import unittest
from models.room import *

class RoomMethods(unittest.TestCase):
    def test_chr_to_int(self):
        self.assertEqual(chr_to_int('a'), 1)
        self.assertEqual(chr_to_int('c'), 3)

    def test_int_to_chr(self):
        self.assertEqual(int_to_chr(0), 'a')
        self.assertEqual(int_to_chr(2), 'c')

    def test_seat_inds(self):
        self.assertEqual(seat_inds(("a12")), (1, 12))
        self.assertEqual(seat_inds(("c3")), (3, 3))

        with self.assertRaises(Exception):
           seat_inds(("23"))

        with self.assertRaises(Exception):
           seat_inds(("12a"))

    def test_process_str(self):
        self.assertEqual(process_str("testing test:"), "testingtest")
        self.assertEqual(process_str("he ll o"), "hello")

    def test_get_cold_inds(self):
        self.assertEqual(get_col_inds("a2-a5"), range(2, 6))
        self.assertEqual(get_col_inds("a2-a15"), range(2, 16))

        self.assertEqual(get_col_inds("a3"), range(3, 4))

        with self.assertRaises(Exception):
            get_col_inds("b22-12")

    def test_get_spec_seats(self):
        # Create room
        rm = Room()
        rm.max_row = 3
        rm.max_col = 3
        rm.seats = [
            [Seat(), Seat(), None],
            [Seat(), None, Seat()],
            [None, Seat(), Seat()],
        ]
        rm.seats[0][0].broken = True
        rm.seats[0][1].left_handed = True
        rm.seats[1][0].special_needs = True
        rm.seats[1][2].left_handed = True
        rm.seats[1][2].special_needs = True
        rm.seats[2][1].enabled = False

        matched = rm.get_spec_seats(left_hand=True, special_needs=True)
        self.assertTrue((1, 2) in matched)

        matched = rm.get_spec_seats(left_hand=False, special_needs=True)
        self.assertTrue((1, 0) in matched)
        self.assertTrue((1, 2) in matched)

        matched = rm.get_spec_seats(left_hand=True, special_needs=False)
        self.assertTrue((0, 1) in matched)
        self.assertTrue((1, 2) in matched)

        matched = rm.get_spec_seats(left_hand=False, special_needs=False)
        self.assertTrue(len(matched), 4)
        self.assertTrue((0, 1) in matched)
        self.assertTrue((1, 0) in matched)
        self.assertTrue((1, 2) in matched)
        self.assertTrue((2, 2) in matched)

        # Assign sid, check that one less seat returned
        rm.seats[2][2].sid = 1
        matched = rm.get_spec_seats(left_hand=False, special_needs=False)
        self.assertTrue(len(matched), 3)

    def test_split_to_chunks(self):
        # Create room
        rm = Room()
        rm.max_row = 3
        rm.max_col = 3
        rm.seats = [
            [Seat(), Seat(), None],
            [Seat(), None, Seat()],
            [None, Seat(), Seat()],
        ]
        rm.seats[1][0].broken = True
        rm.row_breaks = [[], [], [1]]

        chunks = rm.split_to_chunks()
        self.assertEqual(len(chunks), 4)
