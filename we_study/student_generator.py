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
    """
    Main class in that module that do all the stuff to generate students
    """

    def __init__(self, students_amount: int, groups: list, courses_name_list: list):
        self.students_amount = students_amount
        self.groups = groups
        self._generated_lessons(courses_name_list)
        self._generate_students()

    def main(self, headers=None):
        """
        It's the main function that generates all students and save them to CSV table

        :param headers: custom headers
        """
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

                    student_points = self._generate_student_points(group,
                                                                   course.lessons,
                                                                   course.webinars,
                                                                   course.tests)

                    lesson_attendance_percent = student_points[0]
                    webinar_attendance_percent = student_points[1]
                    tests_attendance_percent = student_points[2]
                    test_average_score = student_points[3]

                    student_row = student_row + [lesson_attendance_percent,
                                                 webinar_attendance_percent,
                                                 tests_attendance_percent,
                                                 test_average_score]

                    course_group_rows += [student_row]

                print(course.name, group.type)
                pprint(course_group_rows)
                self._write_rows(course_group_rows, course.name, group.type)

    def _generate_student_points(self, group, lessons_amount: int, webinars_amount: int, tests_amount: int):
        """
        It generates points for lessons/webinars/tests of a student according to his group type

        :param group: Group instance to generate points
        :param lessons_amount: amount of lessons of a course
        :param webinars_amount: amount of webinars of a course
        :param tests_amount: amount of tests of a course
        :return: tuple of points for lessons/webinars/tests
        """
        first_points = group.generate_points()

        lesson_attendance_percent = self._get_attendance(first_points, lessons_amount)

        webinar_attendance_percent = self._get_attendance(
            group.generate_points(last_score=first_points),
            webinars_amount)

        tests_attendance_percent = self._get_attendance(
            group.generate_points(last_score=first_points),
            tests_amount)

        # Checks if 0 tests was solved
        if tests_attendance_percent == 0:
            test_average_score = 0
        else:
            test_average_score = group.generate_points(last_score=first_points)

        return (lesson_attendance_percent,
                webinar_attendance_percent,
                tests_attendance_percent,
                test_average_score)

    def get_students_courses(self):
        pass

    @staticmethod
    def _write_rows(rows: list, course_name: str, group_type: str):
        """
        Just write students data to CSV file

        :param rows: students data in rows format (list of lists)
        :param course_name: name of the course where students are
        :param group_type: type of group where students are
        """
        CsvTools.csv_write_rows(
            script_place(__file__) + 'generated_students/' + '_'.join(course_name.split()) + '_' + group_type + '.csv',
            CsvTools.sort_rows_by('id', rows)
        )

    def _get_available_students(self, course_name: str, group_size: int) -> list:
        """
        Get all students who are not in groups yet

        :param course_name: name of the concrete course
        :param group_size: in another words it is how many students should be retrieved
        :return: list of Student instances of all available students
        """
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
        """
        It generates Students instances to work with later

        """
        self.students = []
        for student_id in range(self.students_amount):
            self.students += [Student(student_id)]

    def _generated_lessons(self, courses_name_lst):
        """
        It generates amount of lessons, tests and webinars for all courses

        :param courses_name_lst: name of course to generate lesson for
        """
        self.courses = []
        for course_name in courses_name_lst:
            self.courses += [Course(
                course_name,
                rd.randint(4, 10),
                rd.randint(2, 4),
                rd.randint(3, 7)
            )]

    def _get_attendance(self, group_points: int, lessons_amount: int) -> int:
        """
        It counts the attendance of lessons/webinar/tests

        :param group_points: random generated percent
        :param lessons_amount: amount of all lessons/webinars/tests in the course
        :return: percent of completed lessons/webinar/tests against all lessons/webinar/tests
        """
        attendance_can_be = []
        for i in range(lessons_amount + 1):
            attendance_can_be += [round((i / lessons_amount) * 100)]

        return min(attendance_can_be, key=lambda x: abs(x - group_points))

    def _get_amount_of_finished(self, group_points: int, lessons_amount: int) -> int:
        """

        :param group_points: random generated percent
        :param lessons_amount: amount of all lessons/webinars/tests in the course
        :return: exact amount of completed lessons/webinar/tests
        """
        attendance_can_be = []
        for i in range(lessons_amount + 1):
            attendance_can_be += [round((i / lessons_amount) * 100)]

        item = min(attendance_can_be, key=lambda x: abs(x - group_points))
        return attendance_can_be.index(item)


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
        self.points_range = (0, 100)

    def generate_points(self, last_score=None):
        points = rd.randint(*self.points_range)
        return points


class BadGroup(Group):
    def __init__(self):
        super().__init__('bad')
        self.points_range = (0, 50)


class GoodGroup(Group):
    def __init__(self):
        super().__init__('good')
        self.points_range = (50, 85)


class ExcellentGroup(Group):
    def __init__(self):
        super().__init__('excellent')
        self.points_range = (85, 100)


class MixedGroup(Group):
    def __init__(self):
        super().__init__('mixed')

    def generate_points(self, last_score=None):
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
