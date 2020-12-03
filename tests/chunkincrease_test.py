import unittest
from models.assign import *
from models.seat import *

class ChunkIncreaseMethods(unittest.TestCase):
    def test_distribute_empty_2pass(self):
        sg = SeatGroups(('a', 4), ('a', 10))
        _, chk_size_l = ChunkIncrease.distribute_empty(sg, 5)
        empty_inds = ChunkIncrease.distribute_empty_2pass(sg, 5, chk_size_l)
        self.assertTrue(('a', 7) in empty_inds)

        sg = SeatGroups(('a', 4), ('a', 16))
        _, chk_size_l = ChunkIncrease.distribute_empty(sg, 3)
        empty_inds = ChunkIncrease.distribute_empty_2pass(sg, 3, chk_size_l)
        self.assertTrue(('a', 6) in empty_inds)
        self.assertTrue(('a', 9) in empty_inds)
        self.assertTrue(('a', 13) in empty_inds)

    def test_distribute_empty(self):
        sg = SeatGroups(('a', 4), ('a', 10))
        empty_inds, chk_size_l = ChunkIncrease.distribute_empty(sg, 5)
        self.assertTrue(('a', 9) in empty_inds)
        self.assertEqual(chk_size_l, [5, 1])

        sg = SeatGroups(('a', 4), ('a', 10))
        empty_inds, chk_size_l = ChunkIncrease.distribute_empty(sg, 2)
        self.assertTrue(('a', 6) in empty_inds)
        self.assertTrue(('a', 9) in empty_inds)
        self.assertEqual(chk_size_l, [2, 2, 1])

        sg = SeatGroups(('a', 4), ('a', 9))
        empty_inds, chk_size_l = ChunkIncrease.distribute_empty(sg, 2)
        self.assertTrue(('a', 6) in empty_inds)
        self.assertTrue(('a', 8) in empty_inds)
        self.assertFalse(('a', 9) in empty_inds)
        self.assertEqual(chk_size_l, [2, 1, 1])

        sg = SeatGroups(('a', 4), ('a', 12))
        empty_inds, chk_size_l = ChunkIncrease.distribute_empty(sg, 3)
        self.assertTrue(('a', 7) in empty_inds)
        self.assertTrue(('a', 11) in empty_inds)
        self.assertEqual(chk_size_l, [3, 3, 1])

    def test_get_possible_seats(self):
        sg = SeatGroups(('a', 4), ('a', 10))
        seats = ChunkIncrease.get_possible_seats(sg, 5)
        self.assertEqual(seats, 6)

        sg = SeatGroups(('a', 4), ('a', 11))
        seats = ChunkIncrease.get_possible_seats(sg, 5)
        self.assertEqual(seats, 7)

        sg = SeatGroups(('a', 3), ('a', 5))
        seats = ChunkIncrease.get_possible_seats(sg, 5)
        self.assertEqual(seats, 3)

        sg = SeatGroups(('a', 1), ('a', 5))
        seats = ChunkIncrease.get_possible_seats(sg, 1)
        self.assertEqual(seats, 3)

    def test_get_max_chunk_size(self):
        sgl = [
            SeatGroups(('a', 4), ('a', 10)),
            SeatGroups(('b', 4), ('b', 10)),
            SeatGroups(('c', 4), ('c', 10)),
        ]
        chunk_size = ChunkIncrease.get_max_chunk_size(sgl, 10)
        self.assertEqual(chunk_size, 1)

        sgl = [
            SeatGroups(('a', 4), ('a', 10)),
            SeatGroups(('b', 4), ('b', 10)),
            SeatGroups(('c', 4), ('c', 10)),
        ]
        chunk_size = ChunkIncrease.get_max_chunk_size(sgl, 21)
        self.assertEqual(chunk_size, 7)

        sgl = [
            SeatGroups(('a', 4), ('a', 10)),
            SeatGroups(('b', 4), ('b', 10)),
            SeatGroups(('c', 4), ('c', 10)),
        ]
        chunk_size = ChunkIncrease.get_max_chunk_size(sgl, 14)
        self.assertEqual(chunk_size, 2)

        sgl = [
            SeatGroups(('a', 4), ('a', 10)),
            SeatGroups(('b', 4), ('b', 10)),
            SeatGroups(('c', 4), ('c', 10)),
        ]
        chunk_size = ChunkIncrease.get_max_chunk_size(sgl, 15)
        self.assertEqual(chunk_size, 2)

        sgl = [
            SeatGroups(('a', 4), ('a', 10)),
            SeatGroups(('b', 4), ('b', 10)),
            SeatGroups(('c', 4), ('c', 10)),
        ]
        chunk_size = ChunkIncrease.get_max_chunk_size(sgl, 16)
        self.assertEqual(chunk_size, 3)

        sgl = [
            SeatGroups(('a', 4), ('a', 10)),
            SeatGroups(('b', 4), ('b', 10)),
            SeatGroups(('c', 4), ('c', 10)),
        ]
        with self.assertRaises(Exception):
            ChunkIncrease.get_max_chunk_size(sgl, 22)

