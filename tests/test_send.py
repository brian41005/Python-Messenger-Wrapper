import json
import logging
import os
import re
import sys
import time
import unittest

from messenger import login, logout, send


class TestSendMessage(unittest.TestCase):
    def setUp(self):
        with open('tests/test_config.json') as f:
            user_data = json.load(f)
        (self.session,
         self.c_user,
         self.fb_dtsg) = login.get_session(user_data['user'],
                                           user_data['passwd'])
        group = user_data['thread'][0]
        self.group_id = group[0]
        self.group_recipient_id = group[1][0]
        self.friend_id = user_data['thread'][1][0]

    def tearDown(self):
        logout(self.session, self.fb_dtsg)

    def test_send_personal_msg(self):
        body = 'Hello, sad world.[{}]'.format(time.time())
        send.send_msg(self.session, self.c_user, self.fb_dtsg,
                      self.friend_id, body, group=False)

    def test_send_group_msg(self):
        body = 'Hello, sad world.[{}]'.format(time.time())
        send.send_msg(self.session, self.c_user, self.fb_dtsg,
                      self.group_id, body, group=True)

    def test_send_emoji(self):
        body = '👍'
        send.send_msg(self.session, self.c_user, self.fb_dtsg,
                      self.group_id, body, group=True)
