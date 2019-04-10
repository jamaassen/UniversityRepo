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
        repo = University(os.path.dirname(__file__))
        actual_students = {CWID: student.get_summary() for CWID, student in repo._students.items()}
        test_students = {'10103': ('10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']),
                         '10115': ('10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']),
                         '10172': ('10172', 'Forbes, I', ['SSW 555', 'SSW 567']),
                         '10175': ('10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']),
                         '10183': ('10183', 'Chapman, O', ['SSW 689']),
                         '11399': ('11399', 'Cordova, I', ['SSW 540']),
                         '11461': ('11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']),
                         '11658': ('11658', 'Kelly, P', ['SSW 540']),
                         '11714': ('11714', 'Morton, A', ['SYS 611', 'SYS 645']),
                         '11788': ('11788', 'Fuller, E', ['SSW 540'])
                         }
        self.assertEqual(test_students, actual_students)

        actual_instructors = {CWID: set(inst.get_summary()) for CWID, inst in repo._instructors.items()}
        test_instructors = {
            '98760': {('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                      ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1),
                      ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                      ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1)},
            '98761': set(),
            '98762': set(),
            '98763': {('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
                      ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1)},
            '98764': {('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                      ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                      ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                      ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3)},
            '98765': {('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                      ('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4)}}

        self.assertEqual(test_instructors, actual_instructors)


if __name__ == '__main__':
    # note: there is no main(). Only test cases here
    unittest.main(exit=False, verbosity=2)
