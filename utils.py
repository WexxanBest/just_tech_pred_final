# -*- coding: utf-8 -*-
"""
That module provides class and functions to provides other modules with useful
"""
import csv
import logging
import os

logging.basicConfig(filename='logs.txt', format='[%(asctime)s] %(levelname)s:%(name)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)


class CsvTools:
    @staticmethod
    def csv_write_rows(file: str, rows: list, headers: list = None, mode: str = 'w'):
        with open(file, mode=mode, encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            if headers:
                csv_writer.writerow(headers)
            csv_writer.writerows(rows)

    @staticmethod
    def csv_read_rows(file: str):
        rows = []
        with open(file, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                rows += [row]
        return rows

    @staticmethod
    def csv_writer(filename: str, mode: str = 'w'):
        file = open(filename, mode=mode, encoding='utf-8', newline='')
        csv_writer = csv.writer(file)
        return csv_writer


def clean_logs():
    if os.path.exists('logs.txt'):
        os.remove('logs.txt')
