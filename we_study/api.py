# -*- coding: utf-8 -*-
"""
That module provides class and functions to work with WE STUDY API and process obtained data
"""
import json
from pprint import pprint
from typing import Union, List
import os

import requests as rq

from utils import (CsvTools, script_place, logger)


class API:
    """
    Class that provides functions to work with WE STUDY API
    """
    def __init__(self, api_token: str):
        self.API_TOKEN = api_token
        self.headers = {
            'x-auth-token': self.API_TOKEN,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    # Getting list of all courses
    def get_courses(self, cache=False) -> list:
        url = 'https://userapi.webinar.ru/v3/organization/courses'
        res = self._get_request(url, cache_filename='courses.json', use_cache=cache)
        return res['data']

    # Getting list of all groups
    def get_groups(self, cache=False):
        url = 'https://userapi.webinar.ru/v3/organization/courses/groups'
        res = self._get_request(url, cache_filename='groups.json', use_cache=cache)

        return res

    # Getting information about course
    def get_course_details(self, course_id: int, cache=False) -> dict:
        url = f'https://userapi.webinar.ru/v3/courses/{course_id}'
        res = self._get_request(url, use_cache=cache, cache_filename=f'course-{course_id}.json')

        useless_fields = ['additionalFields', 'owner', 'certSetting', 'visibilityStatus']
        for field in useless_fields:
            res.pop(field)

        return res

    # Getting user statistics
    def get_user_stat(self, user_id: int):
        url = f'https://userapi.webinar.ru/v3/organization/users/{user_id}/statistics'
        res = self._get_request(url)

        return res

    def get_user_id(self, contact_id: int) -> int:
        url = f'https://userapi.webinar.ru/v3/contacts/{contact_id}/user'
        res = self._get_request(url)

        return res['id']

    def get_course_group_stat(self, course_id: int, group_id: int, cache=False):
        url = f'https://userapi.webinar.ru/v3/courses/{course_id}/groups/{group_id}/statistics'
        res = self._get_request(url, use_cache=cache, cache_filename=f'course-{course_id}-group-{group_id}.json')

        return res

    # Main function that
    def _get_request(self, url: str,
                     headers: dict = None,
                     json_frm: bool = True,
                     use_cache: bool = True,
                     cache_filename: str = '') -> Union[dict, rq.Response]:
        """
        Function just send GET-request to We Study API

        :param url: some API url
        :param headers: provide some custom headers. If not, than default will be used
        :param json_frm: if True will turn Response instance in JSON format
        :param use_cache: if True will save response to cache file
        :param cache_filename: name of cache filename which futher will be get access to

        :return: the Response instance or dict/json format data
        """

        # load from cache if exist and it is allowed to use cache (use_cache = True)
        if json_frm and use_cache and cache_filename and \
                os.path.exists(os.path.dirname(__file__) + '/cache/' + cache_filename):

            res = self._load_cache(os.path.dirname(__file__) + '/cache/' + cache_filename)
            if res:
                return res

        if headers:
            headers = headers
        else:
            headers = self.headers

        # Sending requests
        response = rq.get(url, headers=headers)

        # Format response data to JSON
        if json_frm:
            response = response.json()

        # save to cache if is allowed to use cache (use_cache = True)
        if json_frm and use_cache and cache_filename and response:
            self._save_cache(os.path.dirname(__file__) + '/cache/' + cache_filename, response)

        return response

    # Load a cache from file
    @staticmethod
    def _load_cache(cache_file: str):
        with open(cache_file, 'r') as file:
            res = json.load(file)
            return res

    # Save data to cache file
    @staticmethod
    def _save_cache(cache_file: str, res: dict):
        with open(cache_file, 'w') as file:
            json.dump(res, file)

    # Clean all cache files
    @staticmethod
    def clean_cache():
        folder = os.path.dirname(__file__) + '/cache/'
        files = os.listdir(folder)
        for file in files:
            os.remove(folder + file)


class ApiManager(API):
    """
    Class provides easy-to-use methods to work with API class which work with We Study API
    """
    def __init__(self, api_token: str, use_cache=True):
        """
        :param api_token: API token to access We Study API
        :param use_cache: if True, it will save data to cache and get data from it. Default is True
        """
        super().__init__(api_token)
        self.courses: List[Course] = []
        self.use_cache = use_cache

        self._get_courses_as_list()
        self._get_course_structure()

    def _get_courses_as_list(self):
        """
        Collecting all courses data an save it as a list of Course instances
        """
        raw_courses = self.get_courses(cache=self.use_cache)
        for course in raw_courses:
            if not course['isPublish']:
                continue
            course_details = self.get_course_details(course['id'])
            self.courses += [Course(course_details['id'],
                                    course_details['name'],
                                    [id['id'] for id in course_details['groups']])]

    def _get_course_structure(self):
        """
        Add lessons information to all Course instances
        """
        for course in self.courses:
            for group_id in course.groups_id:
                structure = self.get_course_group_stat(course.id, group_id, cache=self.use_cache)
                lessons_data = structure[0]['lessonsPassing']
                for lesson in lessons_data:
                    course.lessons += [Lesson(lesson['type'],
                                              lesson['name'],
                                              lesson['id'])]

    def get_courses_data(self, save_data_to_file=True, file: str = None) -> List[list]:
        """
        It returns all courses data and save it to csv file if needed
        :param save_data_to_file: if True it will save data to csv file
        :param file: filename where to save adata
        """
        if file is None:
            file = script_place(__file__) + 'data/courses.csv'

        rows = [['id', 'name', 'groups_id']]
        for course in self.courses:
            row = [course.id, course.name, course.groups_id]
            rows += [row]

        if save_data_to_file and file:
            CsvTools.csv_write_rows(file=file, rows=rows)

        return rows


class Course:
    def __init__(self, course_id: int, name: str, groups_id: list):
        self.id = course_id
        self.name = name
        self.groups_id = groups_id
        self.lessons = []


class Lesson:
    def __init__(self, lesson_type: str, name: str, lesson_id: int):
        self.lesson_type = lesson_type
        self.name = name
        self.lesson_id = lesson_id


class Student:
    def __init__(self, first_name: str, last_name: str, contact_id: int, student_id: int, email: str, user_id: int):
        self.first_name = first_name
        self.last_name = last_name
        self.contact_id = contact_id
        self.email = email
        self.student_id = student_id
        self.user_id = user_id


if __name__ == '__main__':
    api = ApiManager('b540bd407852678c0af5b11105dcde14')
    for course in api.courses:
        print('COURSE DETAILS')
        print(f'{course.id=}', f'{course.name=}', f'{course.groups_id=}', sep='\n')
        print('\nCOURSE LESSONS')
        for lesson in course.lessons:
            print(f'\n{lesson.lesson_id=}', f'{lesson.name=}', f'{lesson.lesson_type=}', sep='\n')

    api.get_courses_data()
