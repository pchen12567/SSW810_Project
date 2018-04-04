import os
from collections import defaultdict
from prettytable import PrettyTable


class Student:
    def __init__(self, cwid, name, major, course_grade):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course_grade = course_grade


class Instructor:
    def __init__(self, cwid, name, dept, course_numbers):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.course_numbers = course_numbers


class Major:
    def __init__(self, dept):
        self.dept = dept
        self.req_courses = []
        self.ele_courses = []


class Repository:
    def __init__(self, students, instructors, grades, majors):
        self.students = dict()
        self.instructors = dict()
        self.grades = grades
        self.majors = dict()

        for i in students:
            course_grade = {}
            for grade in grades:
                if grade[0] == i[0]:
                    course_grade[grade[1]] = grade[2]
            self.students[i[0]] = Student(i[0], i[1], i[2], course_grade)

        for j in instructors:
            course_numbers = defaultdict(int)
            for grade in grades:
                if grade[3] == j[0]:
                    course_numbers[grade[1]] += 1
            self.instructors[j[0]] = Instructor(j[0], j[1], j[2], course_numbers)

        for i in majors:
            if i[0] not in self.majors:
                self.majors[i[0]] = Major(i[0])
            if i[1] == 'R':
                self.majors[i[0]].req_courses.append(i[2])
            else:
                self.majors[i[0]].ele_courses.append(i[2])


def read_file(file_path, pattern):
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
    while True:
        path = input('Please input the path: ')
        # path = 'D:\Google\SIT\PycharmProjects\SSW810\HW09'
        # path = '/Users/ryne/Google 云端硬盘/SIT/PycharmProjects/SSW810/HW09'

        path_students = os.path.join(path, 'students.txt')
        path_instructors = os.path.join(path, 'instructors.txt')
        path_grades = os.path.join(path, 'grades.txt')
        path_majors = os.path.join(path, 'majors.txt')

        if os.path.exists(path_students) \
                and os.path.exists(path_instructors) \
                and os.path.exists(path_grades) \
                and os.path.exists(path_majors):
            students = read_file(path_students, 3)
            instructors = read_file(path_instructors, 3)
            grades = read_file(path_grades, 4)
            majors = read_file(path_majors, 3)

            stevens = Repository(students, instructors, grades, majors)

            pt1 = PrettyTable(
                field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
            valid_grade = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
            for student in stevens.students.values():
                com_courses = []
                for course, grade in student.course_grade.items():
                    if grade in valid_grade:
                        com_courses.append(course)
                for com_course in com_courses:
                    remain_req_courses = stevens.majors[student.major].req_courses.copy()
                    if com_course in remain_req_courses:
                        remain_req_courses.remove(com_course)
                    remain_ele_courses = stevens.majors[student.major].ele_courses.copy()
                    if com_course in remain_ele_courses:
                        remain_ele_courses = []

                if len(remain_ele_courses) == 0:
                    pt1.add_row(
                        [student.cwid, student.name, student.major, sorted(com_courses), sorted(remain_req_courses),
                         'None'])
                else:
                    pt1.add_row(
                        [student.cwid, student.name, student.major, sorted(com_courses), sorted(remain_req_courses),
                         sorted(remain_ele_courses)])

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
            break

        else:
            print('Error! The path is not correct, please input again!')


if __name__ == '__main__':
    main()
