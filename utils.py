# -*- coding: utf-8 -*-
"""
That module provides class and functions to provides other modules with useful
"""
import csv
import logging
import os

logging.basicConfig(filename='logs.txt', format='[%(asctime)s] %(levelname)s:%(name)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
logger = logging


class CsvTools:
    @staticmethod
    def csv_write_rows(file: str, rows: list, headers: list = None, mode: str = 'w'):
        with open(file, mode=mode, encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            if headers:
                csv_writer.writerow(headers)
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
        file = open(filename, mode=mode, encoding='utf-8', newline='')
        csv_writer = csv.writer(file)
        return csv_writer

    @staticmethod
    def sort_row_by(field_name: str, rows: list) -> list:
        if field_name not in rows[0]:
            raise ValueError(f'There is "{field_name}" field in rows')
        col = rows[0].index(field_name)
        sorted_col = sorted([field[col] for field in rows])
        sorted_rows = []
        for field_value in sorted_col:
            for row in rows:
                if field_value in row:
                    sorted_rows += [row]
                    break
        return sorted_rows


def clean_logs():
    if os.path.exists('logs.txt'):
        os.remove('logs.txt')


def script_place(magic_file) -> str:
    return os.path.dirname(magic_file) + '/'
