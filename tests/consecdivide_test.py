import unittest
from models.assign import *
from models.seat import *

class ConsecDivideMethods(unittest.TestCase):
    def test_total_chunk_size(self):
         sgl = [
             SeatGroups(('a', 4), ('a', 10)),
             SeatGroups(('b', 4), ('b', 10)),
             SeatGroups(('c', 4), ('c', 10)),
         ]
         chunk_size = ConsecDivide.total_chunk_size(sgl)
         self.assertEqual(chunk_size, 21)

         sgl = [
             SeatGroups(('a', 4), ('a', 10)),
             SeatGroups(('b', 2), ('b', 2)),
             SeatGroups(('c', 9), ('c', 12)),
         ]
         chunk_size = ConsecDivide.total_chunk_size(sgl)
         self.assertEqual(chunk_size, 12)

    def test_get_subchunk_empty(self):
        ll = ConsecDivide.get_subchunk_empty(5, 3, 1, 3)
        self.assertEqual(ll, [4 + 3, 8 + 3, 12 + 3, 16 + 3])

        ll = ConsecDivide.get_subchunk_empty(6, 5, 3, 12)
        self.assertEqual(ll, [6 + 12, 13 + 12, 20 + 12, 26 + 12, 32 + 12])

        ll = ConsecDivide.get_subchunk_empty(2, 3, 0, 0)
        self.assertEqual(ll, [3])


