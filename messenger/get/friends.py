import json
import re

from requests import exceptions

from ..fbtypes import Friend
from ..header import Header
from ..utils import clean_json


def _parse_raw_friends(raw_friends):
    friends = {}
    for uid, v in raw_friends['payload'].items():
        if v.get('vanity'):
            friends[uid] = Friend(**{'id': uid,
                                     'first_name': v.get('firstName'),
                                     'name': v.get('name'),
                                     'vanity': v.get('vanity'),
                                     'is_nonfriend_messenger_contact': v.get('is_nonfriend_messenger_contact'),
                                     'is_active': v.get('is_active'),
                                     'is_messenger_user': v.get('is_messenger_user'),
                                     'is_friend': v.get('is_friend'),
                                     'gender': v.get('gender'),
                                     'type': v.get('type')})
    return friends


def get_friends(session, c_user, fb_dtsg):
    '''

    return: `dict`, key is user id, value is Friend nametuple
    '''
    header = Header.create('origin',
                           'accept-language',
                           'user-agent',
                           'content-type',
                           'authority',
                           others={'accept-encoding':
                                   'gzip, deflate',
                                   'x-msgr-region': 'ATN',
                                   'cache-control': 'max-age=0',
                                   'referer': 'https://www.messenger.com'})

    payload = {'__user': c_user,
               '__a': 1,
               '__req': 8,
               '__be': 0,
               '__pc': 'EXP1:messengerdotcom_pkg',
               'ttstamp': '2658170878850518911395104515865817183457873106120677266',
               'fb_dtsg': fb_dtsg,
               '__rev': 3716917
               }
    try:
        r = session.post('https://www.messenger.com/chat/user_info_all',
                         params={'viewer': c_user, 'dpr': 1},
                         headers=header,
                         data=payload)
    except exceptions.RequestException:
        friends = []
    else:
        raw_friends = json.loads(clean_json(r.text))
        friends = _parse_raw_friends(raw_friends)
    finally:
        return friends
