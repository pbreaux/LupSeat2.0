import unittest
from models.seat import *

class SeatMethods(unittest.TestCase):
    def test_max_chunk_size(self):
        sg = SeatGroups(('a', 4), ('a', 10))
        max_size = sg.max_chunk_size()
        self.assertEqual(max_size, 7)

        sg = SeatGroups(('a', 4), ('a', 10))
        sg.empty = [6]
        max_size = sg.max_chunk_size()
        self.assertEqual(max_size, 4)

        sg = SeatGroups(('a', 4), ('a', 10))
        sg.empty = [7]
        max_size = sg.max_chunk_size()
        self.assertEqual(max_size, 3)
