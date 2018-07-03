import json
import logging
import os
import re
import sys
import time
import unittest

from messenger import Pull, login, logout, send


class TestPullRunningTime(unittest.TestCase):
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

    def test_pull_id(self):
        p = Pull()
        flag = 0
        while True:
            body = 'Hello, sad world.[{}]'.format(int(time.time()))
            send.send_msg(self.session, self.c_user, self.fb_dtsg,
                          self.recipient_id, body, group=False)
            for msg in p.get(self.session, self.c_user):
                self.assertTrue(msg.thread_fbid or msg.other_user_fbid)
                if msg.thread_fbid or msg.other_user_fbid:
                    flag += 1
                    break
            if flag > 1:
                break

    def test_pull_att(self):
        p = Pull()
        body = 'https://www.google.com/'
        send.send_msg(self.session, self.c_user, self.fb_dtsg,
                      self.recipient_id, body, group=False)
        for msg in p.get(self.session, self.c_user):
            self.assertEqual(msg.attachment, 'https://www.google.com/')


class TestPullClass(unittest.TestCase):

    def setUp(self):
        self.p = Pull()

    def test_pull_clean(self):
        p = Pull()
        self.assertEqual(p._clean('{},{}'), [{}, {}])
        self.assertEqual(p._clean('{},{}'), [{}, {}])
        self.assertEqual(p._clean('{},{},'), [])
        self.assertEqual(p._clean('ASDF'), [])
        self.assertEqual(p._clean(None), [])

    def test_pull_parse_1(self):
        raw = {'t': 'lb', 'lb_info': {
            'sticky': '323', 'pool': 'atn1c08_chat-proxy'}}
        for r in self.p._parse(raw):
            self.assertIsNone(r)

    def test_pull_parse_2(self):
        raw = {'t': 'fullReload', 'seq': 189}
        for r in self.p._parse(raw):
            self.assertIsNone(r)

    def test_pull_parse_3(self):
        raw = {'t': 'msg',
               'seq': 191,
               'u': 1234,
               'ms': [{'ofd_ts': 1526043268527, 'delta': {'actionTimestamp': '1526043268315',
                                                          'irisSeqId': '1452401', 'threadKeys': [{'otherUserFbId': '1234'}],
                                                          'watermarkTimestamp': '1526043244666',
                                                          'class': 'MarkRead'},
                       'type': 'delta', 'iseq': 1452401, 'queue': 1234},
                      {'type': 'inbox',
                       'unseen': 0, 'recent_unread': 0,
                       'seen_timestamp': 0,
                       'view_id': 44392134,
                       'unread': 0}]}
        for r in self.p._parse(raw):
            self.assertIsNone(r)
