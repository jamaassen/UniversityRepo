#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created 3/31/2019

@author: Jeffrey Maassen

    Tests course_repository.py

'''

import unittest
import os
from course_repository import Student, Instructor, University


class CourseRepoTest(unittest.TestCase):
    def test_repo(self):
        '''testing university data'''
        repo = University(os.path.join(os.path.dirname(__file__), 'Test Uni'))
        actual_students = {CWID: student.get_summary() for CWID, student in repo._students.items()}
        test_students = {'100': ('100', 'Baldwin, C', ['SSW 564', 'SSW 567']),
                         '101': ('101', 'Wyatt, X', ['SSW 687']),
                         '102': ('102', 'Forbes, I', ['CS 501', 'SSW 567'])}
        self.assertEqual(test_students, actual_students)

        actual_instructors = {CWID: set(inst.get_summary()) for CWID, inst in repo._instructors.items()}
        test_instructors = {'200': {('200', 'Einstein, A', 'SFEN', 'SSW 567', 2), ('200', 'Einstein, A', 'SFEN', 'SSW 687', 1), ('200', 'Einstein, A', 'SFEN', 'CS 501', 1)},
                            '201': {('201', 'Feynman, R', 'SFEN', 'SSW 564', 1)}}

        self.assertEqual(test_instructors, actual_instructors)


if __name__ == '__main__':
    # note: there is no main(). Only test cases here
    unittest.main(exit=False, verbosity=2)
