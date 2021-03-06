# -*- coding: utf-8 -*-
"""
That module provides class and functions to provides other modules with useful methods, like:
    - logging
    - working with CSV files
    - etc...
"""
import csv
import logging
import os


class CsvTools:
    @staticmethod
    def csv_write_rows(file: str, rows: list, headers: list = None, mode='w', sort=False, sort_field: str = None):
        """
        :param file: file to write rows to
        :param rows: rows to write
        :param headers: if there are no headers in rows you can provide them. Default is None
        :param mode: can be 'a' (appends rows to existing file) or 'w' (creates new or rewrites file). Default is 'w'
        :param sort: if True it will sort rows automatically. But 'sort_field' should be provided. Default is 'w'
        :param sort_field: field to sort rows by. Default is None
        """
        with open(file, mode=mode, encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            if headers:
                csv_writer.writerow(headers)

            if sort and sort_field:
                rows = CsvTools.sort_rows_by(field_name=sort_field, rows=rows)

            csv_writer.writerows(rows)

    @staticmethod
    def csv_read_rows(file: str) -> list:
        rows = []
        with open(file, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            rows += csv_reader
        return rows

    @staticmethod
    def csv_writer(filename: str, mode: str = 'w'):
        """

        :param filename: relative/absolute path to file to work with
        :param mode: can be 'w' or 'a'. Default is 'w'

        :return: csv.writer instance
        """
        if mode not in ['w', 'a']:
            raise ValueError(f"Can't open file in that mode. Only can in 'w' or 'a', but {mode} was given")

        file = open(filename, mode=mode, encoding='utf-8', newline='')
        csv_writer = csv.writer(file)
        return csv_writer

    @staticmethod
    def sort_rows_by(field_name: str, rows: list) -> list:
        """
        It sorts list of lists (which called 'rows' in that case) by certain "field_name" in first row (header row)

        :param field_name: field/column name to sort by
        :param rows: rows to sort
        :return: sorted rows
        """
        if field_name not in rows[0]:
            raise ValueError(f'There is "{field_name}" field in rows')

        col = rows[0].index(field_name)  # get column index of "field_name"
        sorted_col = sorted([field[col] for field in rows[1:]])  # get all its members and sort them
        sorted_rows = []

        for field_value in sorted_col:
            for row in rows[1:]:
                if field_value == row[col]:
                    sorted_rows += [row]
                    break

        sorted_rows.insert(0, rows[0])

        return sorted_rows


def clean_logs():
    """
    It just deletes 'logs.txt' file

    """
    log_file = script_place(__file__) + 'logs.txt'
    if os.path.exists(log_file):
        os.remove(log_file)


def script_place(magic_file) -> str:
    """
    :param magic_file: just give __file__ to that and it will work
    :return: the absolute path to directory where the script file is placed
    """
    return os.path.dirname(magic_file) + '/'


logging.basicConfig(filename=script_place(__file__) + 'logs.txt',
                    format='[%(asctime)s] %(levelname)s:%(name)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.DEBUG)
logger = logging
