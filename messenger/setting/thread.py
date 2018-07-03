import logging
import time

from requests import exceptions

from . import utils
from ..header import Header
from ..utils import Payload, gen_msg_id


def set_thread_name(session, c_user, fb_dtsg, thread_id, new_name=None):
    '''
    Only for group thread. if thread is friend, use `set_nickname()`

    thread_id: `str`

    new_name: `str`. default None means reset.

    '''
    referer = 'https://www.messenger.com/t/{}'.format(thread_id)
    header = Header.create('origin',
                           'accept-language',
                           'user-agent',
                           'content-type',
                           others={'accept-encoding': 'gzip, deflate',
                                   'x-msgr-region': 'ATN',
                                   'cache-control': 'max-age=0',
                                   'referer': referer})
    payload = {
        '__a':	1,
        '__be': -1,
        '__dyn': Payload.DYN,
        '__pc': 'PHASED:messengerdotcom_pkg',
        '__req': '2h',
        '__rev': 4041621,
        '__user': c_user,
        'fb_dtsg': fb_dtsg,
        'jazoest': Payload.JAZOEST,
        'thread_id': thread_id,
        'thread_name': new_name,
    }
    params = {'dpr': 1}
    try:
        r = session.post('https://www.messenger.com/messaging/set_thread_name/',
                         headers=header,
                         data=payload,
                         params=params)
        return utils.check_result(r.text)
    except exceptions.RequestException:
        logging.warning('{} fail'.format(set_thread_name.__name__))


def leave_group(session, c_user, fb_dtsg, thread_id):
    '''
    thread_id: `str`
    '''
    msg_id = gen_msg_id()
    referer = 'https://www.messenger.com/t/{}'.format(thread_id)
    header = Header.create('origin',
                           'accept-language',
                           'user-agent',
                           'content-type',
                           others={'accept-encoding': 'gzip, deflate',
                                   'x-msgr-region': 'ATN',
                                   'referer': referer})
    payload = {
        'client': 'mercury',
        'action_type': 'ma-type:log-message',
        'ephemeral_ttl_mode': '0',
        'log_message_data[removed_participants][0]': 'fbid:{}'.format(c_user),
        'log_message_type': 'log:unsubscribe',
        'message_id': msg_id,
        'offline_threading_id': msg_id,
        'source': 'source:messenger:web',
        'thread_fbid': thread_id,
        'timestamp': int(time.time() * 1000),
        '__user': c_user,
        '__a': 1,
        '__dyn': Payload.DYN,
        '__req': '3d',
        '__be': -1,
        '__pc': 'PHASED:messengerdotcom_pkg',
        '__rev': 4056622,
        'fb_dtsg': fb_dtsg,
        'jazoest': Payload.JAZOEST
    }
    try:
        r = session.post('https://www.messenger.com/messaging/send/',
                         headers=header,
                         data=payload,
                         params={'dpr': 1.5})
        return utils.check_result(r.text)
    except exceptions.RequestException:
        logging.warning('{} fail'.format(leave_group.__name__))
