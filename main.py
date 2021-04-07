from pprint import pprint

from google_sheets.google_sheets import (Spreadsheet, SpreadsheetManager, Types)
from we_study.api import (API)

API_KEY = 'b540bd407852678c0af5b11105dcde14'
SPREADSHEET_ID = '17bYk2QPRsuW6cP5kBpKzU5h6aE_RS1Vw1LPadnII0ms'


def spreadsheet_test():
    data = [
        ['DOG', 3],
        [2, 1]
    ]
    spreadsheet = Spreadsheet(SPREADSHEET_ID)

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


if __name__ == '__main__':
    # we_study_test()
    spreadsheet_test()
