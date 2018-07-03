import json
import os
import re
import sys
import unittest

from messenger import get, login, logout


class TestGetFriends(unittest.TestCase):
    def setUp(self):
        with open('tests/test_config.json') as f:
            user_data = json.load(f)
        (self.session,
         self.c_user,
         self.fb_dtsg) = login.get_session(user_data['user'],
                                           user_data['passwd'])

    def tearDown(self):
        logout(self.session, self.fb_dtsg)

    def test_get_friends(self):
        friends = get.get_friends(self.session, self.c_user, self.fb_dtsg)
        self.assertGreater(len(friends), 0)
        for uid, f in friends.items():
            self.assertIsNotNone(f.id)
