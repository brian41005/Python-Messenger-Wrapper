import json
import logging
import time

from requests import exceptions

from . import utils
from ..header import Header
from ..utils import Payload


def save_admin(session, c_user, fb_dtsg, thread_id, admin_id, add):
    '''
    Only for group thread.

    thread_id: `str`

    admin_id: `str` or `list`

    add: `bool`. make admin or remove
    '''
    referer = 'https://www.messenger.com/t/{}'.format(thread_id)
    header = Header.create('origin',
                           'accept-language',
                           'user-agent',
                           'content-type',
                           others={'accept-encoding': 'gzip, deflate',
                                   'x-msgr-region': 'ATN',
                                   'cache-control': 'no-cache',
                                   'referer': referer})
    payload = {
        'thread_fbid': thread_id,
        'add': add,
        '__user': c_user,
        '__a': 1,
        '__dyn': Payload.DYN,
        '__req': '1h',
        '__be': -1,
        '__pc': 'PHASED:messengerdotcom_pkg',
        '__rev': 4056466,
        'fb_dtsg': fb_dtsg,
        'jazoest': Payload.JAZOEST
    }

    pamars = {'dpr': 1.5}

    if type(admin_id) is str:
        admin_id = [admin_id]

    for i, a_id in enumerate(admin_id):
        payload['admin_ids[{}]'.format(i)] = a_id

    try:
        r = session.post('https://www.messenger.com/messaging/save_admins/',
                         headers=header,
                         data=payload,
                         params=pamars)
        return utils.check_result(r.text, 'You might not be a admin.')
    except exceptions.RequestException:
        logging.warning('{} fail'.format(save_admin.__name__))
