import logging
import time

from requests import exceptions

from . import utils
from ..header import Header
from ..utils import Payload, gen_msg_id, load_result_json_text


def add_participant(session, c_user, fb_dtsg, thread_id, new_participants):
    '''
    Only for group thread.

    thread_id: `str`

    new_participants: `str` or `list`
    '''
    msg_id = gen_msg_id()
    referer = 'https://www.messenger.com/t/{}'.format(thread_id)
    header = Header.create('origin',
                           'accept-language',
                           'user-agent',
                           'content-type',
                           others={'accept-encoding': 'gzip, deflate',
                                   'x-msgr-region': 'ASH',
                                   'cache-control': 'max-age=0',
                                   'referer': referer})
    payload = {
        '__a': 1,
        '__be': -1,
        '__dyn': Payload.DYN,
        '__pc':	'PHASED:messengerdotcom_pkg',
        '__req': 'w',
        '__rev': 4064091,
        '__user': c_user,
        'action_type': 'ma-type:log-message',
        'client': 'mercury',
        'ephemeral_ttl_mode': 0,
        'fb_dtsg': fb_dtsg,
        'jazoest': Payload.JAZOEST,
        'log_message_type':	'log:subscribe',
        'message_id': msg_id,
        'offline_threading_id': msg_id,
        'source': 'source:messenger:web',
        'thread_fbid': thread_id,
        'timestamp': int(time.time()*1000)
    }

    pamars = {'dpr': 1.5}

    if type(new_participants) is str:
        new_participants = [new_participants]

    for i, p in enumerate(new_participants):
        key = 'log_message_data[added_participants][{}]'.format(i)
        payload[key] = 'fbid:{}'.format(p)

    try:
        r = session.post('https://www.messenger.com/messaging/send/',
                         headers=header,
                         data=payload,
                         params=pamars)
        return utils.check_result(r.text)
    except exceptions.RequestException:
        logging.warning('{} fail'.format(add_participant.__name__))


def rm_participant(session, c_user, fb_dtsg, thread_id, participant):
    '''
    Only for group thread.

    thread_id: `str`

    participant: `str`
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
        '__a': 1,
        '__be': -1,
        '__dyn': Payload.DYN,
        '__pc': 'PHASED:messengerdotcom_pkg',
        '__req': 'z',
        '__rev': 4051586,
        '__user': c_user,
        'fb_dtsg': fb_dtsg,
        'jazoest': Payload.JAZOEST
    }

    pamars = {
        'dpr': 3,
        'tid': thread_id,
        'uid': participant
    }

    try:
        r = session.post('https://www.messenger.com/chat/remove_participants/',
                         headers=header,
                         data=payload,
                         params=pamars)
        return utils.check_result(r.text, 'You might not be a admin.')
    except exceptions.RequestException:
        logging.warning('{} fail'.format(rm_participant.__name__))
