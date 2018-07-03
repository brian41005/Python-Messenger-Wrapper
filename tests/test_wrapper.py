import json
import unittest

from requests import Session

from messenger import Messenger, login, logout


class TestMessengerWorkingTime(unittest.TestCase):
    def setUp(self):
        with open('tests/test_config.json') as f:
            user_data = json.load(f)
        (self.session,
         self.c_user,
         self.fb_dtsg) = login.get_session(user_data['user'],
                                           user_data['passwd'])

    def tearDown(self):
        logout(self.session, self.fb_dtsg)

    def test_is_workable_method(self):
        m = Messenger(self.session, self.c_user, self.fb_dtsg)
        threads = m.get_threads(limit=15, before=None)
        self.assertEqual(len(threads), 15)


class TestMessenger(unittest.TestCase):

    def test_expected_method(self):
        m = Messenger(Session(), '', '')
        self.assertTrue(m.get_friends)
        self.assertTrue(m.get_threads)
        self.assertTrue(m.get_msg)
        self.assertTrue(m.send_msg)
        self.assertTrue(m.set_nickname)
        self.assertTrue(m.set_emoji)

    def test_session(self):
        s = Session()
        s.cookies.set('a', 1)
        m = Messenger(s, '', '')
        self.assertEqual(m.session.cookies.get_dict(), {'a': 1})

        s.cookies.set('a', 2)
        self.assertEqual(m.session.cookies.get_dict(), {'a': 1})

        s = Session()
        self.assertEqual(m.session.cookies.get_dict(), {'a': 1})

    def test_update_session(self):
        s = Session()
        s.cookies.set('a', 1)
        m = Messenger(s, '', '')
        self.assertEqual(m.session.cookies.get_dict(), {'a': 1})

        m.update(session=Session())
        self.assertEqual(m.session.cookies.get_dict(), {})

    def test_update_c_user(self):
        m = Messenger(Session(), '', '')
        self.assertEqual(m.c_user, '')

        m.update(c_user='1')
        self.assertEqual(m.c_user, '1')

    def test_property_session_cookie(self):
        m = Messenger(Session(), '', '')
        s = m.session
        s.cookies.set(name='a', value=1)
        s = m.session
        self.assertEqual(s.cookies.get_dict(), {})

    def test_property_c_user(self):
        m = Messenger(Session(), '', '')
        c_user = m.c_user
        c_user = '1'
        c_user = m.c_user
        self.assertEqual(c_user, '')

    def test_property_fb_dtsg(self):
        m = Messenger(Session(), '', '')
        fb_dtsg = m.fb_dtsg
        fb_dtsg = '1'
        fb_dtsg = m.fb_dtsg
        self.assertEqual(fb_dtsg, '')

    def test_attrerror(self):
        m = Messenger(Session(), '', '')
        fb_dtsg = m.fb_dtsg
        fb_dtsg = '1'
        fb_dtsg = m.fb_dtsg
        self.assertEqual(fb_dtsg, '')
