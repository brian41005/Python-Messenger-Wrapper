import json
import os
import re
import sys
import unittest

from messenger import get, login, logout


class TestGetThreads(unittest.TestCase):
    def setUp(self):
        with open('tests/test_config.json') as f:
            user_data = json.load(f)
        (self.session,
         self.c_user,
         self.fb_dtsg) = login.get_session(user_data['user'],
                                           user_data['passwd'])
        self.group_id = user_data['thread'][0][0]

    def tearDown(self):
        logout(self.session, self.fb_dtsg)

    def test_get_threads_offset(self):

        threads = get.get_threads(self.session, self.c_user, self.fb_dtsg)
        self.assertEqual(len(threads), 15)

        time_offset_lst = []
        set1 = set([])
        for t in threads:

            try:
                self.assertTrue(t.id and t.name and t.timestamp)
            except AssertionError:
                # group without name
                self.assertTrue(t.id and t.timestamp)

            set1.add(t.id)
            time_offset_lst.append(t.timestamp)
        # print(set1)
        time_offset = sorted(time_offset_lst)[0]
        threads = get.get_threads(self.session,
                                  self.c_user,
                                  self.fb_dtsg,
                                  limit=10,
                                  before=int(time_offset))
        self.assertEqual(len(threads), 10)
        set2 = set([])
        for t in threads:
            try:
                self.assertTrue(t.id and t.name and t.timestamp)
            except AssertionError:
                # group without name
                self.assertTrue(t.id and t.timestamp)

            set2.add(t.id)
        # print(set2)
        # print(set1.intersection(set2))
        self.assertEqual(len(set1.union(set2)), 25)

    def test_get_threads(self):
        threads = get.get_threads(self.session, self.c_user, self.fb_dtsg)
        for t in threads:
            try:
                self.assertTrue(t.id and t.name and t.timestamp)
            except AssertionError:
                # some group without name
                self.assertTrue(t.id and t.timestamp)

    def test_get_a_thread(self):
        thread = get.get_thread(self.session, self.c_user,
                                self.fb_dtsg, self.group_id)
        try:
            self.assertTrue(thread.id and thread.name and thread.timestamp)
        except AssertionError:
            # group without name
            self.assertTrue(thread.id and thread.timestamp)
