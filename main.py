# -*- coding: utf-8 -*-
"""
Main file
"""
from pprint import pprint
import os

from google_sheets.google_sheets import (Spreadsheet, SpreadsheetManager, Types)
from we_study.api import (API)
from we_study.student_generator import generator

API_KEY = 'b540bd407852678c0af5b11105dcde14'
SPREADSHEET_ID = '17bYk2QPRsuW6cP5kBpKzU5h6aE_RS1Vw1LPadnII0ms'


def spreadsheet_test():
    data = [
        ['DOG', 3],
        [2, 1]
    ]

    print(spreadsheet.get_data_by_range('A1:B2'))

    spreadsheet.update_data(data=data, range_name='A1:B2')
    print(spreadsheet.get_data_by_range('A1:B2'))

    spreadsheet.clear_data(range_name='A1:B2')
    print(spreadsheet.get_data_by_range('A1:B2'))

    spreadsheet.add_sheet()


def we_study_test():
    api = API(API_KEY)
    courses = api.get_courses()
    pprint(courses)

    print("\nCOURSE DETAILS")
    details = api.get_course_details(49185)
    pprint(details)

    print("\nCOURSE GROUP STAT")
    api.get_course_group_stat(details['id'], details['groups'][0]['id'])

    print('\nGROUPS')
    api.get_groups()

    contact_id = 150439549
    print('\nUSER STAT. CONTACT ID:', contact_id)
    api.get_user_stat(api.get_user_id(contact_id))


def load_gen_students_to_spreadsheet():
    folder = 'we_study/generated_students/'

    student_files = os.listdir(folder)

    manager.upload_csv(folder + student_files[0])
    student_files.pop(0)

    for student_file in student_files:
        sheet_name = student_file[:-4]
        try:
            spreadsheet.add_sheet(title=sheet_name)
        except:
            pass
        manager.upload_csv(folder + student_file, sheet_name=sheet_name)


def clean_sheets():
    for i in range(1, 12):
        try:
            spreadsheet.delete_sheet(i)
        except:
            pass

    spreadsheet.clear_data('A1:F100')


if __name__ == '__main__':
    spreadsheet = Spreadsheet(SPREADSHEET_ID)
    manager = SpreadsheetManager(spreadsheet)

    clean_sheets()
    load_gen_students_to_spreadsheet()
