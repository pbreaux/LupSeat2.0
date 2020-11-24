import random
from models.student import *
from models.room import *
from enum import Enum

class Algorithm:
    @staticmethod
    def choose_seat(seat_inds):
        '''Randomly choose seat from list and remove it.'''
        ele = random.choice(seat_inds)
        seat_inds.remove(ele)
        return ele

    @staticmethod
    def assign_seats_rand(rm, stdts):
        '''Assign seats based on specificity, from most specific to least. 
        Room class controls which seats are available for students.
        Room class is mutated to include SID of student sitting there.
        Not all students are guaranteed a desired seat, esp if there aren't enough specified seats available.

        Args:
            rm (Room): Room instance
            stdts (Dict{Student}): Dictionary of students, specified by SID
        '''
        # In decreasing order of specificity
        params = [{'left_hand':True, 'special_needs':True},
                  {'left_hand':False, 'special_needs':True},
                  {'left_hand':True, 'special_needs':False},
                  {'left_hand':False, 'special_needs':False}]

        carry_over_stdts = []
        for param in params:
            # Get list of students and available seats
            spec_stdts = Student.get_spec_students(stdts, left_hand=param['left_hand'], special_needs=param['special_needs'])
            seat_inds = rm.get_spec_seats(left_hand=param['left_hand'], special_needs=param['special_needs'])

            # Add list of students with previously unseated students
            spec_and_carry_stdts = carry_over_stdts + spec_stdts
            carry_over_stdts = []

            # Add student to room
            for index, stdt_id in enumerate(spec_and_carry_stdts):
                if len(seat_inds) == 0:
                    carry_over_stdts = spec_and_carry_stdts[index:]
                    break

                rm.add_student(Algorithm.choose_seat(seat_inds), stdt_id)

        # Not enough seats for all students
        if len(carry_over_stdts) > 0:
            raise Exception("Not enough seats in room for students")

class ChunkIncrease(Algorithm):
    @staticmethod
    def distribute_empty(seat_group, max_chunk_size, chk_size_l):
        '''Second pass to distribute empty seat inds within seat group.
        Args:
            seat_group (SeatGroup): Single SeatGroup to distribute students
            max_chunk_size (int): Max size of students sitting together
            empty_inds (List[Tuple(int, int)]): List of empty seat indices from initial pass

        Returns:
            (List[Tuple(int, int)]): List of empty seat indices
        '''
        size = seat_group.size()
        if size <= max_chunk_size:
            return []

        # Check whether seats within chunks can be redistributed
        # TODO: This can be optimized
        chk_size_l.sort()
        while chk_size_l[0] <= chk_size_l[-1] - 2:
            chk_size_l[0] += 1
            chk_size_l[-1] -= 1
            chk_size_l.sort()

        # Get new empty inds
        empty_inds = []
        seat = 0
        for chk_size in chk_size_l:
            seat += chk_size
            cur_seat = (seat_group.chunk_begin[0], seat_group.chunk_begin[1] + seat)
            empty_inds.append(cur_seat)
            seat += 1

        # Remove last seat from empty inds
        return empty_inds[:-1]

    @staticmethod
    def get_empty_seats_inds(seat_group, max_chunk_size):
        '''Gets list of indices where empty seats should go. Prioritizes edge seats.
        Args:
            seat_group (SeatGroup): Single SeatGroup to distribute students
            max_chunk_size (int): Max size of students sitting together

        Returns:
            (List[Tuple(int, int)]): List of empty seat indices (if 2 pass not needed)
            (List[int]): List of chunk sizes separated by empty seat (used for 2 pass)
        '''
        size = seat_group.size()
        if size <= max_chunk_size:
            return []

        empty_inds = []
        chunk_list = []

        # Continue assignment linearly
        current_chunk_size = 0
        for seat in range(size):
            cur_seat = (seat_group.chunk_begin[0], seat_group.chunk_begin[1] + seat)

            # Special case: If we are at second to last seat
            # (Due to last seat already being taken)
            # If adding (this seat + last seat) to current chunk exceeds max size
            edges_assgn = size > 2
            second_last = seat == (size - 2) and edges_assgn and current_chunk_size + 2 > max_chunk_size

            if current_chunk_size == max_chunk_size or second_last:
                # Break off chunk (got too big) or second to last must be empty
                empty_inds.append(cur_seat)
                chunk_list.append(current_chunk_size)
                current_chunk_size = 0
            else:
                current_chunk_size += 1

        # Add last seat
        if current_chunk_size != 0:
            chunk_list.append(current_chunk_size)
            current_chunk_size = 0

        return empty_inds, chunk_list

    @staticmethod
    def get_possible_seats(seat_group, max_chunk_size):
        '''Determines the number of seats possible in this chunk given with some maximum chunk size.
        Args:
            seat_group (SeatGroup): SeatGroup object to specify current chunk
            max_chunk_size (int): Max size of students sitting together

        Returns:
            (int): Number of students who can be seated within this chunk
        '''
        size = seat_group.size()

        if max_chunk_size >= size:
            return size

        taken = 0
        while True:
            size -= max_chunk_size
            taken += max_chunk_size

            if size <= 0:
                # Fix overflow
                taken -= (-size)

                return taken

            # Leave space to separate chunk
            size -= 1

    @staticmethod
    def get_max_chunk_size(chunks, num_students):
        '''Find the minumum "max chunk size" needed to fit everybody.
        Args:
            chunks (List[SeatGroups]): list of prelimiinary chunks before applying empty seats
            num_students (int): Number of students who need seats

        Returns:
            int: Minimum "max size of chunk" necessary to create chunks to fit everybody in the room
        '''
        for chunk_size in range(1, num_students):
            num_seats_filled = 0
            for chunk in chunks:
                num_seats_filled += ChunkIncrease.get_possible_seats(chunk, chunk_size)
                if num_seats_filled >= num_students:
                    return chunk_size

        # Students don't fit in seats
        raise Exception("Students don't fit in seat")


    @staticmethod
    def assign_empty_seats(rm, stdts):
        '''Disables empty seats by distributing it evenly amongst room.
        Args:
            stdts (dict{Student}): dictionary of students, identified by SID
        '''
        chunks = rm.split_to_chunks()
        max_chunk_size = ChunkIncrease.get_max_chunk_size(chunks, len(stdts))

        for chunk in chunks:
            _, chk_size_l = ChunkIncrease.get_empty_seats_inds(chunk, max_chunk_size)
            empty_inds = ChunkIncrease.distribute_empty(chunk, max_chunk_size, chk_size_l)

            for empty_ind in empty_inds:
                rm.set_enable(empty_ind, False)

class ConsecDivide(Algorithm):
    @staticmethod
    def assign_empty_seats(rm, stdts):

        # Used for ConsecDivide
        # Temporary empty col numbers (for each SeatGroup)
        # empty_col = []

        # Split until all empty seats accounted for

        # Finalize empty seats
        for chunk in rm.row_breaks:
            chunk.apply_empty_seats(rm)

    @staticmethod
    def apply_empty_seats(seat_group, rm, empty_col):
        '''Finished splitting chunk, disable empty seats. Used for ChunkIncrease
        Args:
            rm (Room): Room object.
        '''

        # TODO: Fix
        row = seat_group.chunk_begin[0]
        for col in empty_col:
            rm.set_enable((row, col), False)

