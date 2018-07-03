import unittest

from messenger import Friend, Msg, Thread


class TestTypes(unittest.TestCase):

    def test_field(self):
        f = Thread(**{'id': None,
                      'name': None,
                      'emoji': None,
                      'timestamp': None,
                      'is_group': None,
                      'participants': None,
                      'snippet': None,
                      'attachments': None
                      })
        self.assertEqual(set(f._fields), set([
            'id',
            'name',
            'emoji',
            'timestamp',
            'is_group',
            'participants',
            'snippet',
            'attachments'
        ]))
