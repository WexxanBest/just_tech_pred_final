from pprint import pprint
import os

import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

from utils import (CsvTools, logging)


CREDENTIALS_FILE = os.path.dirname(__file__) + '/keys.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    SCOPES
)
httpAuth = credentials.authorize(httplib2.Http())
sheets_service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
drive_service = apiclient.discovery.build('drive', 'v3', http=httpAuth)


class Spreadsheet:
    """
    That class provides with basic functions to work with google sheets
    """
    def __init__(self, spreadsheet_id=None):
        if spreadsheet_id is None:
            self.spreadsheetId = None
        else:
            self.get_spreadsheet_by_id(spreadsheet_id)

        self.sheet_list = []

    def create_spreadsheet(self, sheets=None):
        if sheets is None:
            sheets = [{'properties': {'sheetType': 'GRID', 'sheetId': 0}}]

        spreadsheet = sheets_service.spreadsheets().create(body={
            'properties': {'title': 'just a document', 'locale': 'ru_RU'},
            'sheets': sheets
        }).execute()

        self.spreadsheetId = spreadsheet['spreadsheetId']

        print('Spreadsheet was created at https://docs.google.com/spreadsheets/d/' + self.spreadsheetId)
        return self

    def get_spreadsheet_by_id(self, spreadsheet_id: str):
        self.spreadsheetId = spreadsheet_id
        self.check_connection()

        print('Spreadsheet at https://docs.google.com/spreadsheets/d/' + self.spreadsheetId)
        return self

    def get_spreadsheet_by_url(self, sheet_url: str):
        sheet_url_list = sheet_url.split('/')
        if 'd' not in sheet_url_list:
            raise ValueError('wrong url. Should be like https://docs.google.com/spreadsheets/d/{spreadsheet_id}')

        index = sheet_url_list.index('d') + 1
        self.spreadsheetId = sheet_url_list[index]
        self.check_connection()

        print('Spreadsheet at https://docs.google.com/spreadsheets/d/' + self.spreadsheetId)
        return self

    def grant_permission(self, email_address: str, role: str = 'writer'):
        self.check_id_was_provided()

        access = drive_service.permissions().create(
            fileId=self.spreadsheetId,
            body={'type': 'user', 'role': role, 'emailAddress': email_address},
            fields='id'
        ).execute()

    def get_data_by_range(self, range_name, dimension: str = "ROWS", value_render_option: str = 'FORMATTED_VALUE',
                          date_time_render_option: str = 'SERIAL_NUMBER'):

        self.check_id_was_provided()

        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheetId,
            majorDimension=dimension.upper(),
            range=range_name,
            valueRenderOption=value_render_option,
            dateTimeRenderOption=date_time_render_option
        ).execute()

        rows = result.get('values', [])

        print(f'{len(rows)} rows retrieved.')
        return rows

    def update_data(self, data: list, range_name: str, value_input_option: str = 'USER_ENTERED'):
        self.check_id_was_provided()

        values = data
        body = {
            'values': values
        }
        result = sheets_service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheetId,
            range=range_name,
            valueInputOption=value_input_option,
            body=body).execute()

        print(f'{result.get("updatedCells")} cells updated.')

    def clear_data(self, range_name: str):
        request = sheets_service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheetId,
            range=range_name,
            body={}
        )
        response = request.execute()

    def add_sheet(self, title=None):
        self.get_sheets()

        if title is None:
            title = "Sheet" + str(len(self.sheet_list) + 1)

        body = {'requests': [
                {"addSheet": {"properties": {'sheetId': len(self.sheet_list), 'title': title}}}]}

        sheet = sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheetId,
            body=body
        ).execute()

        pprint(sheet)
        self.get_sheets()

    def get_sheets(self):
        spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        sheet_list = spreadsheet.get('sheets')
        self.sheet_list = sheet_list
        pprint(self.sheet_list)

    def check_id_was_provided(self):
        if not self.spreadsheetId:
            raise ValueError('Spreadsheet ID was not provided!')

    def check_connection(self):
        if not self.is_connected():
            raise ConnectionError("Sheet is not connected. See logs.txt for more info")

    def is_connected(self):
        try:
            spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
            sheet_list = spreadsheet.get('sheets')
            sheet_id_test = sheet_list[0]['properties']['sheetId']
            self.sheet_list = sheet_list
            return True
        except KeyError:
            print('Invalid url')
            return False
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            return False


class SpreadsheetManager:
    """
    That class provides with easy-to-use functions
    to deal with google sheets
    """
    def __init__(self, spreadsheet: Spreadsheet):
        if isinstance(spreadsheet, Spreadsheet):
            self.spreadsheet = spreadsheet
        else:
            raise TypeError(f'expected {type(Spreadsheet())}, but got {type(spreadsheet)}')

    def upload_csv(self, csv_file, left_corner_cell='A1'):
        rows = CsvTools.csv_read_rows(csv_file)
        rows_amount, col_amount = len(rows), len(rows[0])
        range_name = self._get_range(left_corner_cell, rows_amount, col_amount)
        self.spreadsheet.update_data(rows, range_name)

    @staticmethod
    def _get_range(left_corner_cell: str, rows: int, cols: int) -> str:
        start_cell = left_corner_cell
        end_cell = chr(ord(start_cell[0])+cols) + str(int(start_cell[1]) + rows)
        return start_cell + ':' + end_cell


class Types:
    class Dimension:
        ROWS = 'ROWS'
        COLUMNS = 'COLUMNS'

    class SheetRole:
        Writer = Editor = 'writer'
        Reader = Viewer = 'reader'

    class ValueInputOption:
        RAW = 'RAW'
        USER_ENTERED = 'USER_ENTERED'

    class ValueRenderOption:
        FORMATTED_VALUE = 'FORMATTED_VALUE'
        UNFORMATTED_VALUE = 'UNFORMATTED_VALUE'
        FORMULA = 'FORMULA'

    class DateTimeRenderOption:
        SERIAL_NUMBER = 'SERIAL_NUMBER'
        FORMATTED_STRING = 'FORMATTED_STRING'
