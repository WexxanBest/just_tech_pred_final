# -*- coding: utf-8 -*-
"""
That module provides class and functions to generate students with defined parameters to illustrate different
kind of groups of some courses
"""
import random as rd

from utils import (CsvTools, logger, script_place)

default_headers = ['id', 'lesson_completion', 'webinar_completion', 'test_completion', 'average_points_for_tests']
group_types = ['bad', 'good', 'excellent', 'mixed']
default_courses_name = ['Русский язык Гр1', 'Математика Гр1', 'Математика Гр2']


def generate_points(group_type, last_student_score: int = None, bad_results: tuple = (0, 50),
                    good_results: tuple = (50, 85), excellent_results: tuple = (85, 100)):

    if group_type == 'bad':
        return rd.randint(*bad_results)
    elif group_type == 'good':
        return rd.randint(*good_results)
    elif group_type == 'excellent':
        return rd.randint(*excellent_results)

    elif group_type == 'mixed':
        worse_result = (0, 15)
        average_result = (15, 90)
        excellent_result = (90, 100)

        if last_student_score:
            if last_student_score in list(range(*worse_result)):
                return rd.randint(*worse_result)
            elif last_student_score in list(range(*average_result)):
                return rd.randint(*average_result)
            else:
                return rd.randint(*excellent_result)

        return rd.choice([rd.randint(*worse_result),
                          rd.randint(*average_result),
                          rd.randint(*excellent_result)])


def generate_student_id(used_ids: list, all_students_ids: list) -> int:
    available_ids = set(all_students_ids) - set(used_ids)
    return rd.choice(list(available_ids))


def generator(students: list, courses_name: list = None, headers: list = None):
    if courses_name is None:
        courses_name = default_courses_name
    if headers is None:
        headers = default_headers

    for course in courses_name:
        already_in_group = []
        for group_type in group_types:
            print(f'COURSE: {course} ({group_type} group type)')

            writer = CsvTools.csv_writer(script_place(__file__) + 'generated_students/' + '_'.join(course.split())
                                         + '_' + group_type + '.csv')
            writer.writerow(headers)

            for _ in range(rd.randint(10, 25)):  # the amount of students in a group

                student_id = generate_student_id(already_in_group, students)
                already_in_group += [student_id]

                student_row = [student_id]
                print('STUDENT ID:', student_id)

                for header in headers[1:]:
                    last_point = None
                    if len(student_row) > 1:
                        last_point = student_row[1]
                    student_row += [generate_points(group_type, last_student_score=last_point)]
                    print(f'{header}:', student_row[-1])

                writer.writerow(student_row)
                print()


if __name__ == '__main__':
    students = list(range(100))
    generator(students=students)
