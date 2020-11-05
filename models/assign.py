import random
from models.student import *
from models.room import *

def choose_seat(seat_inds):
    '''Randomly choose seat from list and remove it.
    '''
    ele = random.choice(seat_inds)
    seat_inds.remove(ele)
    return ele

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
        spec_stdts = Student.get_specified_students(stdts, left_hand=param['left_hand'], special_needs=param['special_needs'])
        seat_inds = rm.get_spec_seats(left_hand=param['left_hand'], special_needs=param['special_needs'])

        spec_and_carry_stdts = carry_over_stdts + spec_stdts
        carry_over_stdts = []
        for index, stdt_id in enumerate(spec_and_carry_stdts):
            if len(seat_inds) == 0:
                carry_over_stdts = spec_and_carry_stdts[index:]
                break

            rm.add_student(choose_seat(seat_inds), stdt_id)

    # Not enough seats for all students
    if len(carry_over_stdts) > 0:
        raise Exception("Not enough seats in room for students")

