import logging

from requests import exceptions

from . import utils
from ..header import Header
from ..utils import Payload, clean_json


def set_nickname(session, c_user, fb_dtsg,
                 thread_id,
                 participant_id,
                 new_name=''):
    '''
    thread_id: `str`

    participant_id: `str`

    new_name: `str`, default `new_name=''` is reset.
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
        'thread_or_other_fbid': thread_id,
        'participant_id': participant_id,
        'nickname': new_name,
        '__user': c_user,
        '__a': 1,
        '__dyn': Payload.DYN,
        '__req': 'b',
        '__be': -1,
        '__pc': 'PHASED:messengerdotcom_pkg',
        '__rev': 3904427,
        'fb_dtsg': fb_dtsg,
        'jazoest': Payload.JAZOEST
    }
    try:
        r = session.post('https://www.messenger.com/messaging/save_thread_nickname/',
                         headers=header,
                         data=payload,
                         params={'source': 'thread_settings',
                                 'dpr': 1})
        return utils.check_result(r.text)
    except exceptions.RequestException:
        logging.warning('{} fail'.format(set_nickname.__name__))
