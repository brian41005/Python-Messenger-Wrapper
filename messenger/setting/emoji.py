import logging
import math
import os
import random
import re
import sys
import time
from datetime import datetime

from requests import exceptions

from . import utils
from ..header import Header
from ..utils import Payload, clean_json


def set_emoji(session, c_user, fb_dtsg, thread_id, emoji_choice):
    '''
    thread_id: `str`

    emoji_choice: `str` or unicode. if you provide emoji that isn't in 
    messenger emoji list, error will occur.
    '''
    referer = 'https://www.messenger.com/t/{}'.format(thread_id)
    header = Header.create('origin',
                           'accept-language',
                           'user-agent',
                           'content-type',
                           'authority',
                           others={'accept-encoding': 'gzip, deflate',
                                   'x-msgr-region': 'ATN',
                                   'cache-control': 'max-age=0',
                                   'referer': referer})
    payload = {
        'emoji_choice': emoji_choice,
        'thread_or_other_fbid': thread_id,
        '__user': c_user,
        '__a': 1,
        '__dyn': Payload.DYN,
        '__req': '3d',
        '__be': -1,
        '__pc': 'PHASED:messengerdotcom_pkg',
        '__rev': 3904427,
        'fb_dtsg': fb_dtsg,
        'jazoest': Payload.JAZOEST
    }
    try:
        r = session.post('https://www.messenger.com/messaging/save_thread_emoji/',
                         headers=header,
                         data=payload,
                         params={'source': 'thread_settings',
                                 'dpr': 1})
        return utils.check_result(r.text)
    except exceptions.RequestException:
        logging.warning('{} fail'.format(set_emoji.__name__))
