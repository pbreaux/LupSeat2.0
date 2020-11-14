import random
from models.student import *
from models.room import *

def choose_seat(seat_inds):
    '''Randomly choose seat from list and remove it.'''
    ele = random.choice(seat_inds)
    seat_inds.remove(ele)
    return ele

def assign_empty_seats(rm, stdts):
    '''Disables empty seats by distributing it evenly amongst room.
    Args:
        stdts (dict{Student}): dictionary of students, identified by SID
    '''
    chunks = rm.split_to_chunks()
    max_chunk_size = rm.get_max_chunk_size(chunks, len(stdts))

    for chunk in chunks:
        empty_inds = chunk.get_empty_seats_inds(max_chunk_size)

        for empty_ind in empty_inds:
            rm.seats[empty_ind[0]][empty_ind[1]].enable = False

def assign_seats(rm, stdts):
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
        spec_stdts = Student.get_specified_students(stdts, left_hand=param['left_hand'], special_needs=param['special_needs'])
        seat_inds = rm.get_spec_seats(left_hand=param['left_hand'], special_needs=param['special_needs'])

        # Add list of students with previously unseated students
        spec_and_carry_stdts = carry_over_stdts + spec_stdts
        carry_over_stdts = []

        # Add student to room
        for index, stdt_id in enumerate(spec_and_carry_stdts):
            if len(seat_inds) == 0:
                carry_over_stdts = spec_and_carry_stdts[index:]
                break

            rm.add_student(choose_seat(seat_inds), stdt_id)

    # Not enough seats for all students
    if len(carry_over_stdts) > 0:
        raise Exception("Not enough seats in room for students")

