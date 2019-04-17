#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created 3/31/2019

@author: Jeffrey Maassen

    Implements Hw 9: A framework for a data repository of courses, students, and instructors

'''

import os
from prettytable import PrettyTable, from_db_cursor
from collections import defaultdict
import sqlite3


def file_reader(path, num_fields, sep=',', header=False):
    '''This generator opens a delimiter separated file for reading returns all of the values on a single line as a sequence on each call to next()
    -file errors are passed to caller
    -raises ValueError on incorrectly formatted dsv file
    -strips whitespace from outer edges of all returned fields
    '''
    with open(path, 'r') as fp:  # intentionally avoiding try/except so that file exceptions are raised to caller
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
        self._courses = {}  # key = UPPER course string, value = grade string

    def __eq__(self, other):
        ''' return True/False if the two Students are equivalent '''
        return self._CWID == other._CWID

    @staticmethod
    def get_field_names():
        '''This function provides the labels for the fields that are returned in get_summary()'''
        return ('CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives')

    def get_summary(self):
        '''This function provides a summary of student information. Fields are as defined in get_field_names()'''
        if type(self._major) is str:
            dept = self._major
            completed = sorted(course for course, grade in self._courses.items() if grade in ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'))
            req_remain = "Unknown Major"
            elec_remain = "Unknown Major"
        else:
            dept = self._major.name
            completed = self._major.check_completed(self._courses)
            req_remain = self._major.get_required_remaining(self._courses)
            elec_remain = self._major.get_electives_remaining(self._courses)
        return (self._CWID, self._name, dept, completed, req_remain, elec_remain)

    def add_course(self, course, grade):
        '''adds a course and grade to the student's course list. Returns True if this is new course for the student, False if they already had it'''
        if course in self._courses:
            self._courses[course] = grade
            return False
        else:
            self._courses[course] = grade
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


class Major:
    ''' this class stores information about an Major'''
    def __init__(self, name, passing_grade=('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C')):
        self._name = name
        self._required = set()
        self._electives = set()
        self._passing_grade = passing_grade

    @property
    def name(self):
        return self._name

    @staticmethod
    def get_field_names():
        '''This function provides the labels for the fields that are returned in get_summary()'''
        return("Dept", "Required", "Electives")

    def add_course(self, course_type, course):
        '''this method adds the provided course to the list of courses of the provided type for the calling Major'''
        if course_type == 'R':
            self._required.add(course)
        elif course_type == 'E':
            self._electives.add(course)
        else:
            raise ValueError(f'Invalid course type "{course_type}" provided')

    def check_completed(self, course_grades):
        '''This function checks with major if the completed courses have a good enough grade to count, returns a sorted list of compelted courses'''
        return sorted(course for course, grade in course_grades.items() if grade in self._passing_grade)

    def get_required_remaining(self, course_grades):
        '''This function checks with the major what required courses are remaining to be taken'''
        remaining = self._required - {course for course, grade in course_grades.items() if grade in self._passing_grade}
        return remaining if any(remaining) else 'None'

    def get_electives_remaining(self, course_grades):
        '''This function checks with the major what Electives can be taken to fulfill requirements, or "None" if completed'''
        electives_taken = self._electives.intersection({course for course, grade in course_grades.items() if grade in self._passing_grade})
        return 'None' if any(electives_taken) else self._electives

    def get_summary(self):
        '''This function provides a summary of Major information. Fields are as defined in get_field_names()'''
        return (self.name, sorted(self._required), sorted(self._electives))


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
        self._majors = {}  # key = dept name, value = major instances

        if not os.path.isdir(path):
            raise FileNotFoundError(f"{os.path.abspath(path)} is not a valid directory")

        self.import_majors()
        self.import_students()
        self.import_instructors()
        self.import_grades()

    def import_students(self):
        '''this function scans students.txt in the given path of the univeristy for valid students and adds them to the repository'''
        for CWID, name, major in file_reader(os.path.join(self.path, 'students.txt'), 3, '\t'):
            self._students[CWID] = Student(CWID, name.title(), self._majors.get(major.upper(), major.upper()))

    def import_instructors(self):
        '''this function scans instructors.txt in the given path of the univeristy for valid instructors and adds them to the repository'''
        for CWID, name, dept in file_reader(os.path.join(self.path, 'instructors.txt'), 3, '\t'):
            self._instructors[CWID] = Instructor(CWID, name.title(), dept.upper())

    def import_grades(self):
        '''this function scans grades.txt in the given path of the univeristy for valid sets of grade information and adds them to the repository'''
        for stu_CWID, course, grade, inst_CWID in file_reader(os.path.join(self.path, 'grades.txt'), 4, '\t'):
            course = course.upper()
            if self._students[stu_CWID].add_course(course, grade.upper()) and inst_CWID in self._instructors:
                self._instructors[inst_CWID].add_student(course)  # in case of duplicate or updated student grade entries

    def import_majors(self):
        '''this function scans majors.txt in the given path of the univeristy for valid sets of major information and adds them to the repository'''
        for dept, course_type, course in file_reader(os.path.join(self.path, 'majors.txt'), 3, '\t'):
            if dept not in self._majors:
                self._majors[dept] = Major(dept)
            self._majors[dept].add_course(course_type.upper(), course.upper())

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

    def major_pt(self):
        '''This function provides a PrettyTable summary of all major data'''
        major_sum = PrettyTable(field_names=Major.get_field_names())
        for major in self._majors.values():
            major_sum.add_row(major.get_summary())
        return major_sum

    def __str__(self):
        results = [f'Summary for {self.name}']
        results.append('Majors Summary')
        results.append(self.major_pt().get_string())
        results.append('Student Summary')
        results.append(self.student_pt().get_string())
        results.append('Instructor Summary')
        results.append(self.instructor_pt().get_string())
        return '\n'.join(results)


if __name__ == '__main__':
    DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'UniversityRepo.sqlite')
    print(DB_FILE)
    db = sqlite3.connect(DB_FILE)
    with db:
        cur = db.cursor()
        cur.execute("""
                    select i.cwid, i.name, i.Dept, g.course, count(*) as students
                    from HW11_instructors as i
                    join HW11_grades as g on i.CWID=g.Instructor_CWID
                    group by i.cwid, g.course order by i.CWID desc;""")
        inst_table = from_db_cursor(cur)
    print(inst_table)
