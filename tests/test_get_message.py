import re
import os
import sys
import json
import unittest
import logging

from messenger import login, logout
from messenger import get


class TestGetMessage(unittest.TestCase):
    def setUp(self):
        with open('tests/test_config.json') as f:
            user_data = json.load(f)
        (self.session,
         self.c_user,
         self.fb_dtsg) = login.get_session(user_data['user'],
                                           user_data['passwd'])
        self.recipient_id = user_data['thread'][1][0]

    def tearDown(self):
        logout(self.session, self.fb_dtsg)

    def test_get_message(self):

        limit = 10000
        messages = get.get_msg(self.session,
                               self.c_user,
                               self.fb_dtsg,
                               self.recipient_id,
                               limit)
        for m in messages:
            self.assertTrue(m.other_user_fbid or m.thread_fbid)
            self.assertTrue(m.author)
            self.assertTrue((m.body or
                             m.storyAttachment or
                             m.attachment),
                            msg=m.author)

    def test_offset(self):
        limit = 100
        messages = get.get_msg(self.session,
                               self.c_user,
                               self.fb_dtsg,
                               self.recipient_id,
                               limit)
        self.assertEqual(len(messages), limit)

        set1 = set([m.timestamp for m in messages])
        time_offset = sorted(list(set1))[0]

        messages = get.get_msg(self.session,
                               self.c_user,
                               self.fb_dtsg,
                               self.recipient_id,
                               limit,
                               before=int(time_offset))
        set2 = set([m.timestamp for m in messages])

        self.assertEqual(len(messages), limit)
        self.assertTrue(len(set1.union(set2)), 200)
