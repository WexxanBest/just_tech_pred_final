# -*- coding: utf-8 -*-
"""
Main script where all functions called from
"""
from pprint import pprint
import os

from google_sheets.google_sheets import (Spreadsheet, SpreadsheetManager, Types)
from we_study.api import (ApiManager)

API_KEY = 'b540bd407852678c0af5b11105dcde14'
SPREADSHEET_ID = '17bYk2QPRsuW6cP5kBpKzU5h6aE_RS1Vw1LPadnII0ms'


def spreadsheet_test():
    print(spreadsheet.get_data_by_range('A1:B2'))


def we_study_test():
    api = ApiManager(API_KEY)
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

    for student_file in student_files:
        if not student_file.endswith('.csv'):
            continue

        sheet_name = student_file[:-4]

        try:
            spreadsheet.add_sheet(title=sheet_name)
        except:
            pass

        spreadsheet.clear_data('A1:E26', sheet_name=sheet_name)
        manager.upload_csv(folder + student_file, sheet_name=sheet_name)


def download_students_from_google_sheet():
    folder = 'we_study/generated_students/'

    student_files = os.listdir(folder)
    range_name = 'A1:E26'

    for student_file in student_files:
        if not student_file.endswith('.csv'):
            continue

        sheet_name = student_file[:-4]

        manager.download_as_csv(folder + student_file, range_name=range_name, sheet_name=sheet_name)


def clean_and_delete_sheets():
    for i in range(1, 12):
        try:
            spreadsheet.delete_sheet(i)
        except:
            pass


if __name__ == '__main__':
    spreadsheet = Spreadsheet(SPREADSHEET_ID)
    manager = SpreadsheetManager(spreadsheet)
    manager.upload_csv('we_study/data/students_at_courses.csv', sheet_name='Students')
    # download_students_from_google_sheet()
