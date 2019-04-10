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
        self.maxDiff = None
        repo = University(os.path.join(os.path.dirname(__file__), 'Test Uni'))
        actual_students = {CWID: student.get_summary() for CWID, student in repo._students.items()}
        test_students = {
            '100': ('100',
                    'Baldwin, C',
                    'SFEN',
                    ['CS 501', 'SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'],
                    'None',
                    'None'),
            '101': ('101',
                    'Wyatt, X',
                    'SFEN',
                    ['SSW 687'],
                    {'SSW 564', 'SSW 555', 'SSW 540', 'SSW 567'},
                    {'CS 501', 'CS 545', 'CS 513'}),
            '102': ('102',
                    'Forbes, I',
                    'SFEN',
                    ['CS 501', 'SSW 540'],
                    {'SSW 564', 'SSW 555', 'SSW 567'},
                    'None'),
            '103': ('103',
                    'Kelly, P',
                    'SFEN',
                    [],
                    {'SSW 564', 'SSW 555', 'SSW 540', 'SSW 567'},
                    {'CS 501', 'CS 545', 'CS 513'}),
            '104': ('104',
                    'Morton, A',
                    'SYEN',
                    ['SYS 612', 'SYS 671', 'SYS 800'],
                    'None',
                    {'SSW 565', 'SSW 540', 'SSW 810'})}
        self.assertEqual(test_students, actual_students)

        actual_instructors = {CWID: set(inst.get_summary()) for CWID, inst in repo._instructors.items()}
        test_instructors = {
            '200': {('200', 'Einstein, A', 'SFEN', 'CS 501', 2),
                    ('200', 'Einstein, A', 'SFEN', 'SSW 567', 1),
                    ('200', 'Einstein, A', 'SFEN', 'SSW 687', 1)},
            '201': {('201', 'Feynman, R', 'SFEN', 'SSW 540', 2),
                    ('201', 'Feynman, R', 'SFEN', 'SSW 555', 1),
                    ('201', 'Feynman, R', 'SFEN', 'SSW 564', 2),
                    ('201', 'Feynman, R', 'SFEN', 'SYS 612', 1),
                    ('201', 'Feynman, R', 'SFEN', 'SYS 671', 1),
                    ('201', 'Feynman, R', 'SFEN', 'SYS 800', 1)}}
        self.assertEqual(test_instructors, actual_instructors)

        actual_majors = {name: major.get_summary() for name, major in repo._majors.items()}
        test_majors = {
            'SFEN': ('SFEN',
                     ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'],
                     ['CS 501', 'CS 513', 'CS 545']),
            'SYEN': ('SYEN',
                     ['SYS 612', 'SYS 671', 'SYS 800'],
                     ['SSW 540', 'SSW 565', 'SSW 810'])}
        self.assertEqual(test_majors, actual_majors)


if __name__ == '__main__':
    # note: there is no main(). Only test cases here
    unittest.main(exit=False, verbosity=2)
