# -*- coding: utf-8 -*-
"""
That module provides class and functions to run unit-tests to check if all work right
"""
import unittest

from google_sheets.google_sheets import (Spreadsheet, SpreadsheetManager)


TEST_SPREADSHEET_ID = '1ue2DuDOvhDCmUxkDh6Yk805VlfOdJxyb1fImOvySz_Q'
easy_test_data = [
    ['test', 5],
    [8, 'test2']
]


class GoogleSheetsTest(unittest.TestCase):
    spreadsheet = Spreadsheet()
    manager = SpreadsheetManager(spreadsheet)

    def test_basic_functions(self):
        print('test_basic_functions()')

        print('Creating new spreadsheet...', end=' ')
        self.spreadsheet.create_spreadsheet()
        # print(f'done. (Spreadsheet ID: {self.spreadsheet.spreadsheetId})')

        print('Loading data there...', end=' ')
        self.spreadsheet.update_data(data=easy_test_data, range_name='A1:B2')
        # print('done.')

        print('Getting values...', end=' ')
        self.spreadsheet.get_data_by_range('A1:B2')
        # print('done.')

        print('Clearing values...', end=' ')
        self.spreadsheet.clear_data('A1:B2')
        print('done.')

        print('Deleting spreadsheet...', end=' ')
        self.spreadsheet.delete_spreadsheet(self.spreadsheet.spreadsheetId)
        print('done.')

    def test_manager_functions(self):
        print('test_manager_functions()')

        print('Creating new spreadsheet...', end=' ')
        self.spreadsheet.create_spreadsheet()

        print('Uploading CSV file...', end=' ')
        self.manager.upload_csv('test_data.csv')

        print('Deleting spreadsheet...', end=' ')
        self.spreadsheet.delete_spreadsheet(self.spreadsheet.spreadsheetId)
        print('done.')


if __name__ == '__main__':
    unittest.main()
