#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created 3/31/2019

@author: Jeffrey Maassen

    Implements Hw 9: A framework for a data repository of courses, students, and instructors

'''

import os
from prettytable import PrettyTable
from collections import defaultdict


def file_reader(path, num_fields, sep=',', header=False):
    '''This generator opens a delimiter separated file for reading returns all of the values on a single line as a sequence on each call to next()
    -file errors are passed to caller
    -raises ValueError on incorrectly formatted dsv file
    -strips whitespace from outer edges of all returned fields
    '''
    with open(path, 'r') as fp:  # intenionally avoiding try/except so that file exceptions are raised to caller
        fp_it = iter(enumerate(fp))
        if header:
            try:
                next(fp_it)
            except:
                raise ValueError(f'{os.path.abspath(path)} has no lines but expected at least a header')
        for i, line in fp_it:
            fields = line.rstrip('\n').split(sep)
            if len(fields) != num_fields:
                raise ValueError(f'{os.path.abspath(path)} has {len(fields)} fields on line {i} but expected {num_fields}')
            else:
                yield map(str.strip, fields)


class Student:
    ''' this class stores information about a student'''
    def __init__(self, CWID, name, major):
        '''Student Constructor'''
        self._CWID = CWID
        self._name = name
        self._major = major
        self._classes = {}  # key = UPPER course string, value = grade string

    def __eq__(self, other):
        ''' return True/False if the two Students are equivalent '''
        return self._CWID == other._CWID

    @staticmethod
    def get_field_names():
        '''This function provides the labels for the fields that are returned in get_summary()'''
        return ('CWID', 'Name', 'Completed Courses')

    def get_summary(self):
        '''This function provides a summary of student information. Fields are as defined in get_field_names()'''
        return (self._CWID, self._name, sorted(self._classes.keys()))

    def add_course(self, course, grade):
        '''adds a course and grade to the student's course list. Returns True if this is new course for the student, False if they already had it'''
        if course in self._classes:
            self._classes[course] = grade
            return False
        else:
            self._classes[course] = grade
            return True


class Instructor:
    ''' this class stores information about an instructor'''
    def __init__(self, CWID, name, dept):
        '''Instructor Constructor'''
        self._CWID = CWID
        self._name = name
        self._dept = dept
        self._courses = defaultdict(int)  # key = UPPER course string, value = number of students

    def __eq__(self, other):
        ''' return True/False if the two Instructors are equivalent '''
        return self._CWID == other._CWID

    @staticmethod
    def get_field_names():
        '''This function provides the labels for the fields that are returned in get_summary()'''
        return ('CWID', 'Name', 'Dept', 'Course', 'Students')

    def get_summary(self):
        '''This generator provides a summary of instructor information per course they teach, fields are as defined in get_field_names()'''
        for course, num_stu in self._courses.items():
                yield (self._CWID, self._name, self._dept, course, num_stu)

    def add_student(self, course, count=1):
        '''adds a student count to a specified course'''
        self._courses[course] += count


class University:
    '''This class stores information about a particular University'''
    def __init__(self, path, name='Default_University_Name'):
        '''University Constructor. Expects path of the directory that contains
        students.txt, instructors.txt, and grades.txt so that it can parse them.
        University name is optional, uses directory name by default'''
        if name == 'Default_University_Name':
            self.name = os.path.basename(os.path.abspath(path))
        else:
            self.name = name
        self.path = path
        self._students = {}  # key = CWID, value = Student instances
        self._instructors = {}  # key = CWID, value = Instructor instances

        if not os.path.isdir(path):
            raise FileNotFoundError(f"{os.path.abspath(path)} is not a valid directory")

        self.import_students()
        self.import_instructors()
        self.import_grades()

    def import_students(self):
        '''this function scans students.txt in the given path of the univeristy for valid students and adds them to the repository'''
        for CWID, name, major in file_reader(os.path.join(self.path, 'students.txt'), 3, '\t'):
            self._students[CWID] = Student(CWID, name.title(), major.upper())

    def import_instructors(self):
        '''this function scans instructors.txt in the given path of the univeristy for valid instructors and adds them to the repository'''
        for CWID, name, dept in file_reader(os.path.join(self.path, 'instructors.txt'), 3, '\t'):
            self._instructors[CWID] = Instructor(CWID, name.title(), dept.upper())

    def import_grades(self):
        '''this function scans grades.txt in the given path of the univeristy for valid sets of grade information and adds them to the repository'''
        for stu_CWID, course, grade, inst_CWID in file_reader(os.path.join(self.path, 'grades.txt'), 4, '\t'):
            course = course.upper()
            if self._students[stu_CWID].add_course(course, grade):
                self._instructors[inst_CWID].add_student(course)  # in case of duplicate or updated student grade entries

    def student_pt(self):
        '''This function provides a PrettyTable summary of all student data'''
        stu_sum = PrettyTable(field_names=Student.get_field_names())
        for stu in self._students.values():
            stu_sum.add_row(stu.get_summary())
        return stu_sum

    def instructor_pt(self):
        '''This function provides a PrettyTable summary of all instructor data'''
        inst_sum = PrettyTable(field_names=Instructor.get_field_names())
        for inst in self._instructors.values():
            for line in inst.get_summary():
                inst_sum.add_row(line)
        return inst_sum

    def __str__(self):
        results = [f'Summary for {self.name}']
        results.append('Student Summary')
        results.append(self.student_pt().get_string())
        results.append('Instructor Summary')
        results.append(self.instructor_pt().get_string())
        return '\n'.join(results)


if __name__ == '__main__':
    path = input('University directory should contain students.txt, instructor.txt, and grades.txt\nPlease provide the directory for the university: ')
    if not os.path.isdir(os.path.abspath(path)):
        print(f"{os.path.abspath(path)} is not a valid directory")
    else:
        name = input(f'Please provide the University name or hit enter to accept "{os.path.basename(os.path.abspath(path))}" as the name')
        try:
            repo = University(os.path.abspath(path))
        except FileNotFoundError as e:
            print(f'File Error: Could not read/find "{os.path.basename(e.filename)}" in "{os.path.dirname(os.path.abspath(path))}"')
        except ValueError as e:
            print(f'File format error: ' + str(e))
        else:
            print(repo)
