import logging
import re
import time

import requests
from bs4 import BeautifulSoup
from requests import exceptions

from .header import Header
from .utils import Payload


def get_session(user, passwd):
    '''
    user: `str`

    passwd: `str`
    '''
    invalid = (None, )*3

    session = requests.Session()
    session.cookies.set('wd', '1920x1080')

    header = Header().create('authority', 'accept', 'pragma', 'user-agent',
                             others={
                                 'accept-encoding': 'gzip, deflate',
                                 'cookie': 'wd=1440x162; dpr=2; locale=en_US',
                                 'upgrade-insecure-requests': '1'
                             })
    # stage 1
    try:
        stage_1_url = 'https://www.messenger.com/login'
        r = session.get(stage_1_url, headers=header)
        soup = BeautifulSoup(r.text, 'lxml')
    except (exceptions.RequestException,
            AttributeError) as msg:
        logging.error(msg)
        return invalid
    else:
        input_form = _find_input_form(soup)

    try:
        scripts = soup.find_all('script')
        identifier = (re.search(r'\"identifier\":\"\S{32}\"', scripts[7].text)
                      .group(0)
                      .split(':')[1][1:-1])
        _js_datr = (re.search(r'\"_js_datr\",\"\S{24}\"', scripts[13].text)
                    .group(0)
                    .split(',')[1][1:-1])
        session.cookies.set('_js_datr', _js_datr)
    except IndexError as msg:
        logging.error(msg)
        return invalid
    else:
        header = Header.create('authority', 'content-type', 'origin', 'pragma',
                               'user-agent',
                               others={'accept': '*/*',
                                       'accept-encoding': 'gzip, deflate, br',
                                       'referer': 'https://www.messenger.com/'})
    try:
        initial_request_id = input_form['initial_request_id']
        lsd = input_form['lsd']
        lgnrnd = input_form['lgnrnd']
        lgnjs = input_form['lgnjs']
    except KeyError as msg:
        logging.error(msg)
        return invalid
    else:
        payload = {
            'identifier': identifier,
            'initial_request_id': initial_request_id,
            '__user': 0,
            '__a': 1,
            '__dyn': Payload.DYN,
            '__req': 1,
            '__be': -1,
            '__pc': 'PHASED:messengerdotcom_pkg',
            '__rev': 3716917,
            'lsd': lsd,
        }

    # stage 2
    try:
        stage_2_url = 'https://www.facebook.com/login/async_sso/messenger_dot_com'
        lgndim = (session.post(stage_2_url,
                               headers=header,
                               data=payload,
                               params={'dpr': '2', '__a': '1', })
                  .headers['x-auth-result'])
    except (exceptions.RequestException, AttributeError, KeyError) as msg:
        logging.error(msg)
        return invalid
    else:
        header = Header.create('authority', 'accept', 'content-type',
                               'origin', 'pragma', 'user-agent',
                               others={'accept-encoding': 'gzip, deflate',
                                       'upgrade-insecure-requests': '1',
                                       'referer': 'https://www.messenger.com/login'})
        payload = {
            'lsd': lsd,
            'initial_request_id': initial_request_id,
            'timezone': -480,
            'lgndim': lgndim,
            'lgnrnd': lgnrnd,
            'lgnjs': lgnjs,
            'email': user,
            'pass': passwd,
            'login': 1,
            'default_persistent': 0
        }

    # stage 3
    try:
        stage_3_url = 'https://www.messenger.com/login/password/'
        r = session.post(stage_3_url, headers=header, data=payload)
    except exceptions.RequestException as msg:
        logging.error(msg)
        return invalid
    try:
        c_user = session.cookies.get_dict()['c_user']
        fb_dtsg = (re.search(r'\"token\":\"\S{12}:\S{12}\"', r.text)
                   .group(0)
                   .split('":"'))[1][:-1]
    except (KeyError, AttributeError, IndexError) as msg:
        logging.error(msg)
        return invalid
    else:
        return session, c_user, fb_dtsg


def _find_input_form(soup):
    names = ['lsd',
             'timezone',
             'lgnrnd',
             'lgnjs',
             'initial_request_id']
    input_form = soup.find_all(lambda tag: (tag.name == 'input' and
                                            tag.get('name') in names)
                               )

    input_form = {name: value
                  for name, value in map(lambda x: (x.get('name'),
                                                    x.get('value')),
                                         input_form)}
    return input_form
