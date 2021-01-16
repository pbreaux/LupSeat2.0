import unittest
from models.student import *

class StudentMethods(unittest.TestCase):
    def test_get_spec_students(self):
        stdts = {
            1: Student(["Fname", "Lname", "1", "", ""]),
            2: Student(["Fname", "Lname", "2", "left", ""]),
            3: Student(["Fname", "Lname", "3", "", "special"]),
            4: Student(["Fname", "Lname", "4", "left", "special"]),
            5: Student(["Fname", "Lname", "5", "", ""]),
        }

        stdt_l = Student.get_spec_students(stdts, left_hand=False, special_needs=False)
        self.assertEqual(len(stdt_l), 2)
        self.assertTrue(1 in stdt_l)
        self.assertTrue(5 in stdt_l)

        stdt_l = Student.get_spec_students(stdts, left_hand=True, special_needs=False)
        self.assertEqual(len(stdt_l), 1)
        self.assertTrue(2 in stdt_l)

        stdt_l = Student.get_spec_students(stdts, left_hand=False, special_needs=True)
        self.assertEqual(len(stdt_l), 1)
        self.assertTrue(3 in stdt_l)

        stdt_l = Student.get_spec_students(stdts, left_hand=True, special_needs=True)
        self.assertEqual(len(stdt_l), 1)
        self.assertTrue(4 in stdt_l)

