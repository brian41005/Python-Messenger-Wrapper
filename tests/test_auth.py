import re
import os
import sys
import json
import unittest
import logging

from messenger import login, logout


class TestLogout(unittest.TestCase):
    def setUp(self):
        with open('tests/test_config.json') as f:
            user_data = json.load(f)
        (self.session,
         self.c_user,
         self.fb_dtsg) = login.get_session(user_data['user'],
                                           user_data['passwd'])

    def test_logout(self):
        logout(self.session, self.fb_dtsg)


class TestLogin(unittest.TestCase):
    def setUp(self):
        with open('tests/test_config.json') as f:
            user_data = json.load(f)
        self.user = user_data['user']
        self.passwd = user_data['passwd']

    def tearDown(self):
        logout(self.session, self.fb_dtsg)

    def test_login_1(self):
        (self.session,
         c_user,
         self.fb_dtsg) = login.get_session(self.user,
                                           self.passwd)

        self.assertIsNotNone(self.session)
        self.assertIsNotNone(c_user)
        self.assertIsNotNone(self.fb_dtsg)
