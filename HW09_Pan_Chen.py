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


class Repository:
    def __init__(self, students, instructors, grades):
        self.students = []
        self.instructors = []
        self.grades = grades

        for i in students:
            temp = {}
            for grade in grades:
                if grade[0] == i[0]:
                    temp[grade[1]] = grade[2]
            student = Student(i[0], i[1], i[2], temp)
            self.students.append(student)

        for j in instructors:
            temp = defaultdict(int)
            for grade in grades:
                if grade[3] == j[0]:
                    temp[grade[1]] += 1
            instructor = Instructor(j[0], j[1], j[2], temp)
            self.instructors.append(instructor)


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

        if os.path.exists(path_students) \
                and os.path.exists(path_instructors) \
                and os.path.exists(path_grades):
            students = read_file(path_students, 3)
            instructors = read_file(path_instructors, 3)
            grades = read_file(path_grades, 4)

            stevens = Repository(students, instructors, grades)

            pt1 = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])
            for student in stevens.students:
                pt1.add_row([student.cwid, student.name, list(sorted(student.course_grade.keys()))])

            pt2 = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
            for instructor in stevens.instructors:
                for course, number in instructor.course_numbers.items():
                    pt2.add_row(
                        [instructor.cwid, instructor.name, instructor.dept, course, number])

            print('Student Summary')
            print(pt1)
            print('Instructor Summary')
            print(pt2)
            break

        else:
            print('Error! The path is not correct, please input again!')


if __name__ == '__main__':
    main()
