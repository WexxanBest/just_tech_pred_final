# -*- coding: utf-8 -*-
"""
That module provides class and functions to work with Google Sheets API
"""
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
    That class provides with basic functions to work with google sheets. It can:
        - Create new spreadsheet or connect to existed ones
        - Get, update, clear data of the spreadsheet
        - Add/delete sheets
    """
    def __init__(self, spreadsheet_id=None):
        if spreadsheet_id is None:
            self.spreadsheetId = None
        else:
            self.get_spreadsheet_by_id(spreadsheet_id)

        self.sheet_list = []

    def create_spreadsheet(self, sheets=None):
        """
        It creates spreadsheet

        :param sheets: list of sheets properties to create with spreadsheet creation
        """
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
        """
        It connects to Google Sheet spreadsheet by its Spreadsheet ID

        :param spreadsheet_id: id of Google Sheet spreadsheet
        """
        self.spreadsheetId = spreadsheet_id
        self.check_connection()

        print('Spreadsheet at https://docs.google.com/spreadsheets/d/' + self.spreadsheetId)
        return self

    def get_spreadsheet_by_url(self, sheet_url: str):
        """
        It connects to Google Sheet spreadsheet by its url. It just retrieves Spreadsheet ID from url

        :param sheet_url: url of Google Sheet spreadsheet
        """
        sheet_url_list = sheet_url.split('/')
        if 'd' not in sheet_url_list:
            raise ValueError('wrong url. Should be like https://docs.google.com/spreadsheets/d/{spreadsheet_id}')

        index = sheet_url_list.index('d') + 1
        self.spreadsheetId = sheet_url_list[index]
        self.check_connection()

        print('Spreadsheet at https://docs.google.com/spreadsheets/d/' + self.spreadsheetId)
        return self

    def grant_permission(self, email_address: str, role: str = 'writer'):
        """
        It give access to user to deal with Spreadsheet

        :param email_address: user email address
        :param role: could be 'writer' or 'reader'. Default is 'writer'
        """
        self.check_id_was_provided()

        try:
            access = drive_service.permissions().create(
                fileId=self.spreadsheetId,
                body={'type': 'user', 'role': role, 'emailAddress': email_address},
                fields='id'
            ).execute()
        except:
            logging.error('Error occurred!', exc_info=True)
            raise Exception("Can't grant permission. See logs.txt for more information")

        logging.info(access)

    def get_data_by_range(self, range_name, dimension: str = "ROWS", value_render_option: str = 'FORMATTED_VALUE',
                          date_time_render_option: str = 'SERIAL_NUMBER', sheet_name: str = None):
        """
        It gets data of certain range of cells of in a certain sheet

        :param range_name: can be like 'A1:B2'
        :param dimension: can be 'ROWS' or 'COLUMNS'.
        If 'ROWS' was given, it will get data row by row;
        if 'COLUMNS' was given, it will get data column by column.

        :param value_render_option:
        :param date_time_render_option:
        :param sheet_name: name of sheet to get data from

        :return: rows of data
        """

        self.check_id_was_provided()

        if sheet_name:
            range_name += f'{sheet_name}!{range_name}'

        try:
            result = sheets_service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheetId,
                majorDimension=dimension.upper(),
                range=range_name,
                valueRenderOption=value_render_option,
                dateTimeRenderOption=date_time_render_option
            ).execute()
        except:
            logging.error('Error occurred', exc_info=True)
            raise Exception("Can't get data. See logs.txt for more information")

        rows = result.get('values', [])

        logging.info(f'{len(rows)} rows retrieved.')
        print(f'{len(rows)} rows retrieved.')
        return rows

    def update_data(self, data: list, range_name: str, value_input_option: str = 'USER_ENTERED'):
        """
        It updates data in certain range of cells in certain sheet

        :param data: data to load. Should be like list of lists, row by row
        :param range_name: can be like "A1:B2" or "sheet_name!A1:B2"
        :param value_input_option: can be 'USER_ENTERED' or 'RAW'. First one will show cells like if user entered them,
        so, for example, '=5+3' would be just '8'. While 'RAW' mode will show like it is: '=5+3'
        """
        self.check_id_was_provided()

        values = data
        body = {
            'values': values
        }
        try:
            result = sheets_service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheetId,
                range=range_name,
                valueInputOption=value_input_option,
                body=body).execute()
        except:
            logging.error('Exception occurred', exc_info=True)
            raise Exception("Can't update data. See logs.txt ")

        logging.info(f'{result.get("updatedCells")} cells updated.')
        print(f'{result.get("updatedCells")} cells updated.')

    def clear_data(self, range_name: str, sheet_name: str = None):
        """
        It clears data in certain range of cells in certain sheet

        :param sheet_name: name of sheet
        :param range_name: can be like "A1:B2" or "sheet_name!A1:B2"
        """

        if sheet_name:
            range_name = f'{sheet_name}!{range_name}'

        try:
            request = sheets_service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheetId,
                range=range_name,
                body={}
            )
            response = request.execute()
            logging.info(response)
        except:
            logging.error('Exception occurred', exc_info=True)
            raise Exception("Can't clear data. See logs.txt for more information")

    def add_sheet(self, title=None):
        """
        It creates a new sheet.

        # :param title: if it's not provided, sheet title would be generated automatically
        """
        self.update_sheet_list()

        if title is None:
            title = "Sheet" + str(len(self.sheet_list) + 1)

        body = {'requests': [
                {"addSheet": {"properties": {'sheetId': len(self.sheet_list), 'title': title}}}]}

        try:
            sheet = sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheetId,
                body=body
            ).execute()
        except Exception as e:
            logging.error('Exception occurred', exc_info=True)
            raise Exception("Can't create a sheet. See logs.txt for more details")

        logging.info(sheet)
        self.update_sheet_list()

    def delete_sheet(self, sheet_id: int):
        """
        It deletes sheet from Spreadsheet

        :param sheet_id: id of concrete sheet
        """
        self.update_sheet_list()

        for sheet in self.sheet_list:
            if sheet['properties']['sheetId'] == sheet_id:
                break
        else:
            raise ValueError('There is no sheet with that id')

        body = {'requests': [
            {"deleteSheet":  {'sheetId': sheet_id}}]}

        try:
            sheet = sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheetId,
                body=body
            ).execute()
        except Exception as e:
            logging.error('Exception occurred', exc_info=True)
            raise Exception("Can't delete a sheet. See logs.txt for more details")

        logging.info(sheet)
        self.update_sheet_list()

    def update_sheet_list(self):
        """
        It updates list of sheets with their information
        """
        spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        sheet_list = spreadsheet.get('sheets')
        self.sheet_list = sheet_list

    def check_id_was_provided(self):
        """
        It will raise a Value Error, if Spreadsheet ID was not provided
        """
        if not self.spreadsheetId:
            raise ValueError('Spreadsheet ID was not provided!')

    def check_connection(self):
        """
        It will raise a Connection Error, if can't connect to Spreadsheet. Otherwise, it will just pass.
        """
        if not self.is_connected():
            raise ConnectionError("Sheet is not connected. See logs.txt for more info")

    def is_connected(self):
        """
        Check if it can get sheets of given Spreadsheet. There is at least one sheet in any Spreadsheet, so it is a good
        way to check connection. If it raise some error, it will mean that wrong Spreadsheet ID was given or there is
        a some HTTP error or some other error.

        :return: True if can connect to Spreadsheet. Otherwise it returns False
        """
        try:
            spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
            sheet_list = spreadsheet.get('sheets')
            sheet_id_test = sheet_list[0]['properties']['sheetId']
            self.sheet_list = sheet_list
            return True
        except KeyError:
            logging.error('Invalid url')
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
        """
        :param spreadsheet: should be given
        """
        if isinstance(spreadsheet, Spreadsheet):
            self.spreadsheet = spreadsheet
        else:
            raise TypeError(f'expected {type(Spreadsheet())}, but got {type(spreadsheet)}')

    def upload_csv(self, csv_file, left_corner_cell='A1', sheet_name=None, create_new_sheet=False):
        """
        It is upload a csv file to Google Sheet spreadsheet. It just updates cells

        :param csv_file: relative or absolute path to csv file
        :param left_corner_cell: cell name to start creating the table in sheet
        :param sheet_name: name of sheet to upload csv to. If sheet doesn't exist it will raise error. Default is None
        :param create_new_sheet: if True, it will create a new sheet with "sheet_name" name. If sheet already exists
        it will raise an error. Default is False

        :return: updated range
        """
        if create_new_sheet:
            self.spreadsheet.add_sheet(title=sheet_name)

        rows = CsvTools.csv_read_rows(csv_file)
        rows_amount, col_amount = len(rows), len(rows[0])

        range_name = self._get_range(left_corner_cell, rows_amount, col_amount)

        if sheet_name:
            range_name = f'{sheet_name}!{range_name}'

        self.spreadsheet.update_data(rows, range_name)

        return range_name

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
