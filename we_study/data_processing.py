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

    headers = ['id'] + courses
    rows = [headers]

    for student_id in students:
        student_row = [int(student_id)]
        for course in courses:
            if course in students[student_id]:
                student_row += [True]
            else:
                student_row += [False]

        rows += [student_row]

    CsvTools.csv_write_rows(script_place(__file__) + 'data/students_at_courses.csv',
                            rows=CsvTools.sort_rows_by(field_name='id', rows=rows))


if __name__ == '__main__':
    get_user_courses()
