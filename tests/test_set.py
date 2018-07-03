import json
import logging
import random
import unittest

from messenger import login, logout, setting


class TestSet(unittest.TestCase):
    def setUp(self):
        with open('tests/test_config.json') as f:
            user_data = json.load(f)
        (self.session,
         self.c_user,
         self.fb_dtsg) = login.get_session(user_data['user'],
                                           user_data['passwd'])
        group = user_data['thread'][0]
        self.group_id = group[0]
        self.group_recipient = group[1]
        self.some_one_to_be_added = user_data['thread'][2][0]

    def tearDown(self):
        logout(self.session, self.fb_dtsg)

    def test_set_emoji(self):
        emoji = '😱'
        flag = setting.set_emoji(self.session,
                                 self.c_user,
                                 self.fb_dtsg,
                                 self.group_id, emoji)
        self.assertTrue(flag)
        flag = setting.set_emoji(self.session,
                                 self.c_user,
                                 self.fb_dtsg,
                                 self.group_id, '')
        self.assertTrue(flag)

    def test_set_emoji_not_in_list(self):
        emoji = '🥠'
        flag = setting.set_emoji(self.session,
                                 self.c_user,
                                 self.fb_dtsg,
                                 self.group_id, emoji)
        self.assertIsNone(flag)
        flag = setting.set_emoji(self.session,
                                 self.c_user,
                                 self.fb_dtsg,
                                 self.group_id, '')
        self.assertTrue(flag)

    def test_set_nickname(self):
        for p_id in self.group_recipient:
            new_name = 'Chatbot_{}'.format(random.randint(0, 100))
            flag = setting.set_nickname(self.session,
                                        self.c_user,
                                        self.fb_dtsg,
                                        self.group_id,
                                        p_id,
                                        new_name)
            self.assertTrue(flag)
        for p_id in self.group_recipient:
            new_name = ''
            flag = setting.set_nickname(self.session,
                                        self.c_user,
                                        self.fb_dtsg,
                                        self.group_id,
                                        p_id,
                                        new_name)
            self.assertTrue(flag)

    def test_set_thread_name(self):
        new_name = 'new_name'
        flag = setting.set_thread_name(self.session,
                                       self.c_user,
                                       self.fb_dtsg,
                                       self.group_id,
                                       new_name)
        self.assertTrue(flag)
        flag = setting.set_thread_name(self.session,
                                       self.c_user,
                                       self.fb_dtsg,
                                       self.group_id)
        self.assertTrue(flag)
        flag = setting.set_thread_name(self.session,
                                       self.c_user,
                                       self.fb_dtsg,
                                       self.group_id, 'TT')
        self.assertTrue(flag)

    def test_revome_people_from_group(self):
        flag = setting.rm_participant(self.session,
                                      self.c_user,
                                      self.fb_dtsg,
                                      self.group_id,
                                      self.group_recipient[0])
        self.assertTrue(flag)

        flag = setting.add_participant(self.session,
                                       self.c_user,
                                       self.fb_dtsg,
                                       self.group_id,
                                       [self.group_recipient[0]])
        self.assertTrue(flag)

    def test_add_people_to_group(self):
        flag = setting.add_participant(self.session,
                                       self.c_user,
                                       self.fb_dtsg,
                                       self.group_id,
                                       self.some_one_to_be_added)
        self.assertTrue(flag)
        flag = setting.rm_participant(self.session,
                                      self.c_user,
                                      self.fb_dtsg,
                                      self.group_id,
                                      self.some_one_to_be_added)
        self.assertTrue(flag)

    def test_save_admin(self):
        member_id = self.group_recipient[0]

        flag = setting.save_admin(self.session,
                                  self.c_user,
                                  self.fb_dtsg,
                                  self.group_id,
                                  member_id,
                                  add=True)
        self.assertIsNotNone(flag)
        flag = setting.save_admin(self.session,
                                  self.c_user,
                                  self.fb_dtsg,
                                  self.group_id,
                                  member_id,
                                  add=False)
        self.assertIsNotNone(flag)

    def test_leave_group(self):
        # setting.leave_group(self.session, self.c_user, self.fb_dtsg,
        #                     self.group_id)
        pass
