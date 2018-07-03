import logging
import time

from requests import exceptions

from ..header import Header
from ..utils import Payload, clean_json, gen_msg_id


def send_msg(session, c_user, fb_dtsg, recipient_id, body, group=False):
    '''
    recipient_id: `str`, user id

    body: `str`, msg

    group: `bool`, is recipient_id a group or not
    '''

    referer = 'https://www.messenger.com/t/{}'.format(recipient_id)
    utc_timestamp = int(time.time() * 1000)
    msg_id = gen_msg_id()

    header = Header.create('origin',
                           'accept-language',
                           'user-agent',
                           'content-type',
                           'authority',
                           others={'accept-encoding': 'gzip, deflate',
                                   'x-msgr-region': 'ATN',
                                   'cache-control': 'max-age=0',
                                   'referer': referer})

    if group:
        payload = {'client': 'mercury',
                   'action_type': 'ma-type:user-generated-message',
                   'body': body,
                   'ephemeral_ttl_mode': 0,
                   'has_attachment': False,
                   'message_id': msg_id,
                   'offline_threading_id': msg_id,
                   'source': 'source:messenger:web',
                   'thread_fbid': recipient_id,
                   'timestamp': utc_timestamp,
                   '__user': c_user,
                   '__a': 1,
                   '__dyn': Payload.DYN,
                   '__req': 'i',
                   '__be': -1,
                   '__pc': 'PHASED:messengerdotcom_pkg',
                   '__rev': 3896064,
                   'fb_dtsg': fb_dtsg,
                   'jazoest': Payload.JAZOEST
                   }
    else:
        payload = {'client': 'mercury',
                   'action_type': 'ma-type:user-generated-message',
                   'body': body,
                   'ephemeral_ttl_mode': 0,
                   'has_attachment': 'false',
                   'message_id': msg_id,
                   'offline_threading_id': msg_id,
                   'other_user_fbid': recipient_id,
                   'source': 'source:messenger:web',
                   'specific_to_list[0]': 'fbid:{}'.format(recipient_id),
                   'specific_to_list[1]': 'fbid:{}'.format(c_user),
                   'timestamp': utc_timestamp,
                   '__user': c_user,
                   '__a': 1,
                   '__dyn': Payload.DYN,
                   '__req': 'g',
                   '__be': -1,
                   '__pc': 'PHASED:messengerdotcom_pkg',
                   '__rev': 3896064,
                   'fb_dtsg': fb_dtsg,
                   'jazoest': Payload.JAZOEST
                   }
    try:
        r = session.post('https://www.messenger.com/messaging/send/',
                         headers=header,
                         data=payload,
                         params={'dpr': 1})
    except exceptions.RequestException:
        logging.warning('sending fail')
