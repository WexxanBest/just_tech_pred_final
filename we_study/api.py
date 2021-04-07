# -*- coding: utf-8 -*-
"""
That module provides class and functions to work with WE STUDY API and process data
"""
import json
from pprint import pprint
from typing import Union
import os

import requests as rq


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
    def get_courses(self, cache=True):
        url = 'https://userapi.webinar.ru/v3/organization/courses'
        res = self._get_request(url, cache_filename='courses.json', use_cache=cache)
        return res['data']

    # Getting list of all groups
    def get_groups(self, cache=True):
        url = 'https://userapi.webinar.ru/v3/organization/courses/groups'
        res = self._get_request(url, cache_filename='groups.json', use_cache=cache)
        pprint(res)

    # Getting information about course
    def get_course_details(self, course_id: int, cache=True):
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
        pprint(res)

    def get_user_id(self, contact_id: int) -> int:
        url = f'https://userapi.webinar.ru/v3/contacts/{contact_id}/user'
        res = self._get_request(url)
        pprint(res)
        return res['id']

    def get_course_group_stat(self, course_id: int, group_id: int, cache=True):
        url = f'https://userapi.webinar.ru/v3/courses/{course_id}/groups/{group_id}/statistics'
        res = self._get_request(url, use_cache=cache, cache_filename=f'course-{course_id}-group-{group_id}.json')
        pprint(res)

    # Main function that
    def _get_request(self, url: str,
                     headers: dict = None,
                     json_frm: bool = True,
                     use_cache: bool = True,
                     cache_filename: str = '') -> Union[dict, rq.Response]:

        print(__file__ + '/cache/' + cache_filename, os.path.exists(os.path.dirname(__file__) + '/cache/' + cache_filename))
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
