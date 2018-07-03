import json
import re

from requests import exceptions

from ..fbtypes import Thread
from ..header import Header
from ..utils import Payload, clean_graphql


class ThreadUtils:

    @staticmethod
    def get_thread_id(thread):
        thread_key = thread['thread_key']
        thread_id = (thread_key.get('thread_fbid') or
                     thread_key.get('other_user_id'))
        return thread_id

    @staticmethod
    def get_thread_participants(thread):
        participants = {}
        for participant in thread.get('all_participants').get('nodes'):
            p = participant['messaging_actor']
            participants[p['id']] = {'type': p.get('__typename'),
                                     'name': p.get('name'),
                                     'gender': p.get('gender'),
                                     'short_name': p.get('short_name'),
                                     'username': p.get('username'),
                                     'nickname': None,
                                     'is_admin': False}
        return participants

    @staticmethod
    def get_thread_name(thread, thread_id):
        if not thread.get('name'):
            for participant in thread.get('all_participants').get('nodes'):
                p = participant['messaging_actor']
                if p['id'] == thread_id:
                    return p.get('name')
        else:
            return thread['name']

    @staticmethod
    def get_thread_snippet(node):
        snippet = {'id': (node.get('message_sender')
                              .get('messaging_actor')
                              .get('id')),
                   'body': node.get('snippet'),
                   'timestamp': node.get('timestamp_precise')
                   }
        return snippet

    @staticmethod
    def get_thread_emoji(thread):
        if thread.get('customization_info'):
            return thread['customization_info'].get('emoji')
        else:
            return ''

    @staticmethod
    def set_participants_nickname(thread, participants):
        if thread.get('customization_info'):
            nicknames = (thread['customization_info']
                         .get('participant_customizations'))
            for nickname in nicknames:
                uid = nickname['participant_id']
                if participants.get(uid):
                    participants[uid]['nickname'] = nickname['nickname']

    @staticmethod
    def set_is_admin(thread, participants):
        admins = [p['id'] for p in thread.get('thread_admins')]
        for uid, p in participants.items():
            p['is_admin'] = uid in admins

    @staticmethod
    def parse_raw_thread(raw_thread):
        is_group = raw_thread['thread_type'] == 'GROUP'
        thread_id = ThreadUtils.get_thread_id(raw_thread)
        participants = ThreadUtils.get_thread_participants(raw_thread)
        emoji = ThreadUtils.get_thread_emoji(raw_thread)
        thread_name = ThreadUtils.get_thread_name(raw_thread, thread_id)

        node = raw_thread['last_message']['nodes'][0]
        snippet = ThreadUtils.get_thread_snippet(node)

        ThreadUtils.set_participants_nickname(raw_thread, participants)
        ThreadUtils.set_is_admin(raw_thread, participants)

        attachments = node.get('blob_attachements')
        timestamp = node.get('timestamp_precise')
        return Thread(**{'id': thread_id,
                         'name': thread_name,
                         'emoji': emoji,
                         'timestamp': timestamp,
                         'is_group': is_group,
                         'participants': participants,
                         'snippet': snippet,
                         'attachments': attachments
                         })

    @staticmethod
    def parse_raw_threads(raw_threads):
        threads = [ThreadUtils.parse_raw_thread(raw_thread)
                   for raw_thread in raw_threads]
        return threads


def get_threads(session, c_user, fb_dtsg, *, limit=15, before=None):
    '''
    limit: `int`, number of fetching thread you want

    before: `int`, default is `None`, timestamp offset

    return: `list` of Thread nametuple
    '''
    if before:
        before -= 1
    header = Header.create('origin',
                           'accept-language',
                           'user-agent',
                           'content-type',
                           'authority',
                           others={'accept-encoding': 'gzip, deflate',
                                   'x-msgr-region': 'ATN',
                                   'cache-control': 'max-age=0',
                                   'referer': 'https://www.messenger.com'})
    query = {
        'o0':
        {
            'doc_id': '1349387578499440',
            'query_params': {
                'limit': limit,
                'before': before,
                'tags': [] if not before else ['INBOX'],
                'includeDeliveryReceipts': True,
                'includeSeqID': False
            }
        }
    }

    payload = {'batch_name': 'MessengerGraphQLThreadlistFetcher',
               '__user': c_user,
               '__a': 1,
               '__req': 8,
               '__be': 0,
               '__pc': 'PHASED:messengerdotcom_pkg',
               'ttstamp': '2658170878850518911395104515865817183457873106120677266',
               'fb_dtsg': fb_dtsg,
               '__rev': 3716917,
               '__dyn': Payload.DYN,
               'jazoest': Payload.JAZOEST,
               'queries': json.dumps(query)
               }
    try:
        r = session.post('https://www.messenger.com/api/graphqlbatch',
                         data=payload,
                         headers=header)
    except exceptions.RequestException:
        threads = []
    else:
        json_string = clean_graphql(r.text)
        raw_threads = json.loads(json_string)
        raw_threads = (raw_threads['o0']['data']
                       ['viewer']['message_threads']['nodes'])
        threads = ThreadUtils.parse_raw_threads(raw_threads)
    finally:
        return threads


def get_thread(session, c_user, fb_dtsg, thread_id):
    '''
    thread_id: `str`

    return: a Thread nametuple

    '''
    referer = 'https://www.messenger.com/t/{}'.format(thread_id)
    header = Header.create('origin',
                           'accept-language',
                           'user-agent',
                           'content-type',
                           'authority',
                           others={'accept-encoding': 'gzip, deflate',
                                   'x-msgr-region': 'ATN',
                                   'cache-control': 'no-cache',
                                   'referer': referer})
    query = {
        'o0':
        {
            'doc_id': '1994296557271743',
            'query_params': {
                "id": thread_id,
                "message_limit": 0,
                "load_messages": True,
                "load_read_receipts": False,
                "before": None
            }
        }
    }

    payload = {'batch_name': 'MessengerGraphQLThreadFetcher',
               '__user': c_user,
               '__a': 1,
               '__req': 'q',
               '__be': -1,
               '__pc': 'PHASED:messengerdotcom_pkg',
               'fb_dtsg': fb_dtsg,
               '__rev': 4056814,
               '__dyn': Payload.DYN,
               'jazoest': Payload.JAZOEST,
               'queries': json.dumps(query)
               }
    try:
        r = session.post('https://www.messenger.com/api/graphqlbatch',
                         data=payload,
                         headers=header)
    except exceptions.RequestException:
        thread = []
    else:
        json_string = clean_graphql(r.text)
        raw_thread = json.loads(json_string)
        raw_thread = raw_thread['o0']['data']['message_thread']
        thread = ThreadUtils.parse_raw_thread(raw_thread)
    finally:
        return thread
