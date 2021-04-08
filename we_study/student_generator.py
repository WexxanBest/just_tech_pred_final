# -*- coding: utf-8 -*-
"""
That module provides class and functions to generate students with defined parameters to illustrate different
kind of groups of some courses
"""
import random as rd
from pprint import pprint

from utils import (CsvTools, logger, script_place)

default_headers = ['id', 'lesson_completion', 'webinar_completion', 'test_completion', 'average_points_for_tests']
group_types = ['bad', 'good', 'excellent', 'mixed']
default_courses_name = ['Русский язык Гр1', 'Математика Гр1', 'Математика Гр2']


class StudentGenerator:
    def __init__(self, students_amount: int, groups: list, courses_name_list: list):
        self.students_amount = students_amount
        self.groups = groups
        self._generated_lessons(courses_name_list)
        self._generate_students()

    def main(self, headers=None):
        if headers is None:
            headers = default_headers
        for course in self.courses:
            for group in self.groups:
                course_group_rows = [headers]
                group.group_size = rd.randint(10, 25)
                group_size = group.group_size

                students = self._get_available_students(course.name, group_size)

                for student in students:
                    student_row = [student.student_id]

                    if group.type == 'mixed':
                        first_points = group.generate_points()
                        student_row += [self._get_attendance(first_points, course.lessons)]
                        student_row += [self._get_attendance(group.generate_points(last_score=first_points),
                                                             course.webinars)]
                        student_row += [self._get_attendance(group.generate_points(last_score=first_points),
                                                             course.tests)]
                        student_row += [group.generate_points(last_score=first_points)]

                        course_group_rows += [student_row]
                        continue

                    student_row += [self._get_attendance(group.generate_points(), course.lessons)]
                    student_row += [self._get_attendance(group.generate_points(), course.webinars)]
                    student_row += [self._get_attendance(group.generate_points(), course.tests)]
                    student_row += [group.generate_points()]

                    course_group_rows += [student_row]

                print(course.name, group.type)
                pprint(course_group_rows)
                self._write_rows(course_group_rows, course.name, group.type)

    def get_students_courses(self):
        pass

    def _write_rows(self, rows: list, course_name: str, group_type: str):
        CsvTools.csv_write_rows(
            script_place(__file__) + 'generated_students/' + '_'.join(course_name.split()) + '_' + group_type + '.csv',
            CsvTools.sort_rows_by('id', rows)
        )

    def _get_available_students(self, course_name: str, group_size: int):
        available_students = []
        students = rd.sample(self.students, k=len(self.students))
        for student in students:
            if course_name not in student.courses:
                available_students += [student]
                student.courses += [course_name]

            if len(available_students) == group_size:
                break

        return available_students

    def _generate_students(self):
        self.students = []
        for student_id in range(self.students_amount):
            self.students += [Student(student_id)]

    def _generated_lessons(self, courses_name_lst):
        self.courses = []
        for course_name in courses_name_lst:
            self.courses += [Course(
                course_name,
                rd.randint(4, 10),
                rd.randint(1, 4),
                rd.randint(3, 7)
            )]

    def _get_attendance(self, group_points: int, lessons_amount: int):
        attendance_can_be = []
        for i in range(lessons_amount + 1):
            attendance_can_be += [round((i / lessons_amount) * 100)]

        return min(attendance_can_be, key=lambda x: abs(x - group_points))


class Course:
    def __init__(self, name: str, lessons: int, tests: int, webinars: int):
        self.name = name
        self.lessons = lessons
        self.tests = tests
        self.webinars = webinars


class Student:
    def __init__(self, student_id: int):
        self.student_id = student_id
        self.courses = []


class Group:
    def __init__(self, group_type: str):
        self.type = group_type
        self.group_size = rd.randint(10, 25)

    @staticmethod
    def generate_points():
        points = rd.randint(0, 100)
        return points


class BadGroup(Group):
    def __init__(self):
        super().__init__('bad')

    @staticmethod
    def generate_points():
        points = rd.randint(0, 50)
        return points


class GoodGroup(Group):
    def __init__(self):
        super().__init__('good')

    @staticmethod
    def generate_points():
        points = rd.randint(50, 85)
        return points


class ExcellentGroup(Group):
    def __init__(self):
        super().__init__('excellent')

    @staticmethod
    def generate_points():
        points = rd.randint(85, 100)
        return points


class MixedGroup(Group):
    def __init__(self):
        super().__init__('mixed')

    @staticmethod
    def generate_points(last_score=None):
        worse_result = (0, 15)
        average_result = (15, 90)
        excellent_result = (90, 100)

        if last_score:
            if last_score in list(range(*worse_result)):
                points = rd.randint(*worse_result)
            elif last_score in list(range(*average_result)):
                points = rd.randint(*average_result)
            else:
                points = rd.randint(*excellent_result)
        else:
            points = rd.choice([rd.randint(*worse_result),
                                rd.randint(*average_result),
                                rd.randint(*excellent_result)])

        return points


if __name__ == '__main__':
    groups = [
        BadGroup(),
        GoodGroup(),
        ExcellentGroup(),
        MixedGroup()
    ]

    generator = StudentGenerator(100, groups=groups, courses_name_list=default_courses_name)
    generator.main()
