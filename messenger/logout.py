import logging
from requests import exceptions

from .header import Header


def logout(session, fb_dtsg):
    '''
    '''
    url = 'https://www.messenger.com/logout/'
    header = Header.create('authority',
                           'accept',
                           'content-type',
                           'origin',
                           'pragma',
                           'user-agent',
                           others={'accept-encoding': 'gzip, deflate',
                                   'upgrade-insecure-requests': '1',
                                   'cache-control': 'no-cache',
                                   'referer': 'https://www.messenger.com'})
    payload = {'fb_dtsg': fb_dtsg}
    try:
        r = session.post(url, headers=header, data=payload)
    except exceptions.RequestException as msg:
        logging.error(msg)
