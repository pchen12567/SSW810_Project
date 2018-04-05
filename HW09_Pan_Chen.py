"""
This program prompts user to provide a directory path, and then reads the files inside to create a framework
which summarized students, instructors, grades, majors information.

Created on Apr 4 11:25:49 2018

@author: Pan Chen
"""

import os
from collections import defaultdict
from prettytable import PrettyTable


class Student:
    """ Create class Student """

    def __init__(self, cwid, name, major):
        """
        Initial Student class
        :param cwid: student ID
        :param name: student name
        :param major: student major
        """
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course_grade = {}


class Instructor:
    """ Create class Instructor """

    def __init__(self, cwid, name, dept):
        """
        Initial Instructor class
        :param cwid: instructor ID
        :param name: instructor name
        :param dept: instructor major
        """
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.course_numbers = defaultdict(int)


class Major:
    """ Create class Major """

    def __init__(self, dept):
        """
        Initial Major class
        :param dept: major name
        req_courses: required courses
        ele_courses: electives courses
        """
        self.dept = dept
        self.req_courses = set()
        self.ele_courses = set()


class Repository:
    """ Create class Repository saves information of students, instructors, grades, majors."""

    def __init__(self, path):
        """
        Initial Repository class
        :param path: directory path
        students: a dictionary saves information of students
        instructors: a dictionary saves information of instructors
        grades: a list saves information of grades
        majors: a dictionary saves information of majors
        """
        path_students = os.path.join(path, 'students.txt')
        path_instructors = os.path.join(path, 'instructors.txt')
        path_grades = os.path.join(path, 'grades.txt')
        path_majors = os.path.join(path, 'majors.txt')

        if os.path.exists(path_students) \
                and os.path.exists(path_instructors) \
                and os.path.exists(path_grades) \
                and os.path.exists(path_majors):
            students_list = read_file(path_students, 3)
            instructors_list = read_file(path_instructors, 3)
            grades_list = read_file(path_grades, 4)
            majors_list = read_file(path_majors, 3)

            self.students = dict()
            self.instructors = dict()
            self.grades = grades_list
            self.majors = dict()

            for i in students_list:
                self.students[i[0]] = Student(i[0], i[1], i[2])

            for j in instructors_list:
                self.instructors[j[0]] = Instructor(j[0], j[1], j[2])

            for g in grades_list:
                if g[0] in self.students:
                    self.students[g[0]].course_grade[g[1]] = g[2]
                if g[3] in self.instructors:
                    self.instructors[g[3]].course_numbers[g[1]] += 1

            for k in majors_list:
                if k[0] not in self.majors:
                    self.majors[k[0]] = Major(k[0])
                if k[1] == 'R':
                    self.majors[k[0]].req_courses.add(k[2])
                else:
                    self.majors[k[0]].ele_courses.add(k[2])
        else:
            raise FileNotFoundError


def read_file(file_path, pattern):
    """
    Create a function to ride files from the specified file
    :param file_path: file path
    :param pattern:
    :return: the list of content
    """
    file = open(file_path, 'r')
    with file:
        result = []
        for line in file:
            ls = line.strip().split('\t')
            if pattern == len(ls):
                result.append(ls)
            else:
                print('Warning! Lack information in file: ', file_path)
        return result


def main():
    path = input('Please input the path: ')
    # path = 'D:\Google\SIT\PycharmProjects\SSW810\HW09'
    # path = '/Users/ryne/Google 云端硬盘/SIT/PycharmProjects/SSW810/HW09'

    try:
        stevens = Repository(path)
    except FileNotFoundError:
        print('Error! File can not found!')
    else:
        pt1 = PrettyTable(
            field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        valid_grade = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        for student in stevens.students.values():
            com_courses = set()
            for course, grade in student.course_grade.items():
                if grade in valid_grade:
                    com_courses.add(course)
            remain_req_courses = stevens.majors[student.major].req_courses - com_courses
            remain_ele_courses = stevens.majors[student.major].ele_courses & com_courses
            if len(remain_ele_courses) == 0:
                pt1.add_row(
                    [student.cwid, student.name, student.major, sorted(com_courses), remain_req_courses,
                     stevens.majors[student.major].ele_courses])
            else:
                pt1.add_row(
                    [student.cwid, student.name, student.major, sorted(com_courses), remain_req_courses,
                     'None'])

        pt2 = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for instructor in stevens.instructors.values():
            for course, number in instructor.course_numbers.items():
                pt2.add_row([instructor.cwid, instructor.name, instructor.dept, course, number])

        pt3 = PrettyTable(field_names=['Dept', 'Required', 'Electives'])
        for major in stevens.majors.values():
            pt3.add_row([major.dept, major.req_courses, major.ele_courses])

        print('Majors Summary')
        print(pt3)
        print('Student Summary')
        print(pt1)
        print('Instructor Summary')
        print(pt2)


if __name__ == '__main__':
    main()
