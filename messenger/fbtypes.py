from collections import namedtuple

Friend = namedtuple('Friend', ['id',
                               'first_name',
                               'name',
                               'vanity',
                               'is_nonfriend_messenger_contact',
                               'is_active',
                               'is_messenger_user',
                               'is_friend',
                               'gender',
                               'type'])

Msg = namedtuple('Msg', ['body',
                         'author',
                         'timestamp',
                         'other_user_fbid',
                         'thread_fbid',
                         'storyAttachment',
                         'attachment'])

Thread = namedtuple('Thread', ['id',
                               'name',
                               'emoji',
                               'timestamp',
                               'is_group',
                               'participants',
                               'snippet',
                               'attachments'])
