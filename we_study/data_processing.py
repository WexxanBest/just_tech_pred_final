# -*- coding: utf-8 -*-
"""
That module provides functions to process generated students data
"""
import os
from pprint import pprint

from utils import (CsvTools, logger, script_place)


def get_user_courses():
    """
    It
    :return: nothing
    """
    students = {}
    courses = []
    files = os.listdir(script_place(__file__) + 'generated_students/')
    for file in files:
        if not file.endswith('.csv'):
            continue

        students_of_course = CsvTools.csv_read_rows(script_place(__file__) + 'generated_students/' + file)[1:]
        students_ids = sorted([id[0] for id in students_of_course])
        course_name = ' '.join(file.split('_')[:-1])

        if course_name not in courses:
            courses += [course_name]

        for student_id in students_ids:
            if student_id not in students:
                students[student_id] = [course_name]
            else:
                students[student_id] += [course_name]

    pprint(students)

    writer = CsvTools.csv_writer(script_place(__file__) + 'data/students_at_courses.csv')
    headers = ['id'] + courses
    writer.writerow(headers)

    for student_id in students:
        student_row = [student_id]
        for course in courses:
            if course in students[student_id]:
                student_row += [True]
            else:
                student_row += [False]

        writer.writerow(student_row)


if __name__ == '__main__':
    get_user_courses()
