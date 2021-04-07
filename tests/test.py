import unittest

from google_sheets.google_sheets import Spreadsheet


class GoogleSheetsTest(unittest.TestCase):
    TEST_SPREADSHEET_ID = '1ue2DuDOvhDCmUxkDh6Yk805VlfOdJxyb1fImOvySz_Q'

    def test_spreadsheet_upload(self):
        spreadsheet = Spreadsheet(self.TEST_SPREADSHEET_ID)
        print('upload')

    def test_spreadsheet_read(self):
        spreadsheet = Spreadsheet(self.TEST_SPREADSHEET_ID)
        print('read')


if __name__ == '__main__':
    unittest.main()
