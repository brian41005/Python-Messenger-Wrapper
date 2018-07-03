import json
import re

from requests import exceptions

from ..fbtypes import Msg
from ..header import Header
from ..utils import Payload, clean_json


def _parse_message(raw_messages):
    data = []
    if raw_messages['o0'].get('data'):
        thread = raw_messages['o0']['data'].get('message_thread')
        if thread:
            messages = thread['messages']['nodes']
            for m in messages:
                text = None
                if m.get('message'):
                    text = m['message']['text']

                if not text and m.get('sticker'):
                    text = m['sticker']['label'] or m['sticker']['url']

                # Admin message
                if not text and m.get('snippet'):
                    text = m['snippet']

                storyAttachment = attachment = None

                if m.get('extensible_attachment'):
                    extensible_attachment = m['extensible_attachment']
                    title = extensible_attachment['story_attachment']['title_with_entities']['text']
                    url = extensible_attachment['story_attachment']['url']
                    storyAttachment = {'title': title, 'url': url}

                if m.get('blob_attachments'):
                    blob_attachments = m['blob_attachments'][0]
                    type_ = blob_attachments['__typename']

                    if type_ == 'MessageImage':
                        attachment = blob_attachments['preview']['uri']

                    elif type_ == 'MessageAnimatedImage':
                        attachment = blob_attachments['animated_image']['uri']

                    elif type_ == 'MessageAudio':
                        attachment = blob_attachments['playable_url']

                    elif type_ == 'MessageVideo':
                        attachment = blob_attachments['playable_url']

                    elif type_ == 'MessageFile':
                        attachment = blob_attachments['url']

                d = Msg(**{'body': text,
                           'author': m['message_sender']['id'],
                           'timestamp': m['timestamp_precise'],
                           'other_user_fbid': thread['thread_key'].get('other_user_id'),
                           'thread_fbid': thread['thread_key'].get('thread_fbid'),
                           'storyAttachment': storyAttachment,
                           'attachment': attachment
                           })

                # if not (d['body'] or d['storyAttachment'] or d['attachment']):
                #     print(m)
                data.append(d)
    return data


def get_msg(session, c_user, fb_dtsg, recipient_id, limit, before=None):
    '''
    recipient_id: `str` or `int`

    limit: `int`, number of message

    before: `int`, default is `None`, timestamp offset

    return: `list` of Msg nametuple
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

    queries = {'o0': {'doc_id': '1505711682889534',
                      'query_params': {
                          'id': recipient_id,
                          'message_limit': limit,
                          'load_messages': True,
                          'load_read_receipts': False,
                          'before': before}
                      }
               }

    payload = {'__user': c_user,
               '__a': 1,
               '__dyn': Payload.DYN,
               '__af': 'iw',
               '__req': 'q',
               '__be': -1,
               '__pc': 'PHASED:messengerdotcom_pkg',
               '__rev': 3105978,
               'fb_dtsg': fb_dtsg,
               'jazoest': Payload.JAZOEST,
               'queries': json.dumps(queries)
               }
    try:
        r = session.post('https://www.messenger.com/api/graphqlbatch/',
                         data=payload,
                         headers=header)
    except exceptions.RequestException:
        messages = []
    else:
        text = r.text.replace('\r\n', ',').replace('\n', '')
        raw_messages, result = json.loads('[{}]'.format(text))
        messages = _parse_message(raw_messages)
    finally:
        return messages
