import json
import logging

from requests import exceptions

from .header import Header
from .utils import clean_json
from .fbtypes import Msg


class Pull:
    def __init__(self):
        self.seq = 1
        self.had_increment = False
        self.client_id = '52adf842'
        self.sticky = 210
        self.sticky_pool = 'atn5c06_chat-proxy'
        self.retry = 0

    def _clean(self, text):
        try:
            text = clean_json(text)
        except AttributeError:
            text = ''
        else:
            text = text.strip()
            text = text.replace('\n', ',')

        try:
            raw_json_data = json.loads('[{}]'.format(text))
        except json.decoder.JSONDecodeError:
            raw_json_data = []
        finally:
            return raw_json_data

    def _pull(self, session, c_user):
        url = 'https://3-edge-chat.messenger.com/pull'
        params = {
            'channel': 'p_' + c_user,
            'seq': self.seq,
            'partition': -2,
            'clientid': self.client_id,
            'cb': '70md',
            'idle': 101,
            'qp': 'y',
            'cap': 8,
            'pws': 'fresh',
            'isq': 1447168,
            'msgs_recv': 0,
            'uid': c_user,
            'viewer_uid': c_user,
            'sticky_token': self.sticky,
            'sticky_pool': self.sticky_pool,
            'state': 'offline',
            'mode': 'stream',
            'format': 'json'
        }
        header = Header.create('origin',
                               'accept-language',
                               'user-agent',
                               'content-type',
                               'authority',
                               others={'accept-encoding': 'gzip, deflate',
                                       'x-msgr-region': 'ATN',
                                       'cache-control': 'max-age=0',
                                       'referer': 'https://www.messenger.com',
                                       'accept': '*/*'})
        try:
            r = session.get(url,
                            params=params,
                            headers=header,
                            stream=True)
            # r is raw socket response from the server
            # http://docs.python-requests.org/en/master/user/quickstart/#raw-response-content
            return r
        except exceptions.RequestException as msg:
            logging.error(msg)

    def _gen_msg(self, ms, body=None, att=None):
        meta = ms['delta']['messageMetadata']
        return Msg(**{'body': body,
                      'author': meta.get('actorFbId'),
                      'timestamp': meta['timestamp'],
                      'other_user_fbid': meta['threadKey'].get('otherUserFbId'),
                      'thread_fbid': meta['threadKey'].get('threadFbId'),
                      'storyAttachment': None,
                      'attachment': att
                      })

    def _parse(self, message):
        try:
            t = message.get('t')
            if t == 'msg':
                self.seq = message['seq']
                self.had_increment = True
                for ms in message['ms']:
                    if ms['type'] == 'delta' and ms.get('delta'):
                        if ms['delta']['class'] == 'NewMessage':
                            # TEXT
                            if ms['delta'].get('body'):
                                body = ms['delta']['body']
                                yield self._gen_msg(ms, body)

                            elif ms['delta'].get('attachments'):
                                att = ms['delta']['attachments'][0]
                                # STICKER
                                if att['mercury'].get('sticker_attachment'):
                                    attachment = att['mercury']['sticker_attachment']['label']
                                    yield self._gen_msg(ms, att=attachment)

                                elif att['mercury'].get('blob_attachment'):
                                    type_ = att['mercury']['blob_attachment']['__typename']
                                    # PICTURE
                                    if type_ == 'MessageImage':
                                        url = (att['mercury']
                                               ['blob_attachment']
                                               ['preview']
                                               ['uri'])
                                        yield self._gen_msg(ms, att=url)
                                    # GIF
                                    elif type_ == 'MessageAnimatedImage':
                                        url = (att['mercury']
                                               ['blob_attachment']
                                               ['animated_image']
                                               ['uri'])
                                        yield self._gen_msg(ms, att=url)

                                else:
                                    pass

                        # Admin Text Message
                        elif ms['delta']['class'] == 'AdminTextMessage':
                            body = ms['delta']['messageMetadata']['adminText']
                            yield self._gen_msg(ms, body)

                    elif ms['type'] == 'typ':
                        # yield {'type': ms['type'],
                        #        'st': ms['st'],
                        #        'from': ms['from'],
                        #        'to': ms['to']
                        #        }
                        pass

            elif t == 'heatbeat':
                if self.had_increment:
                    self.seq += 1
                    self.had_increment = False

            elif t == 'fullReload':
                self.seq = message['seq']

            elif t == 'lb':
                self.sticky = message['lb_info']['sticky']
                self.sticky_pool = message['lb_info']['pool']

        except KeyError as msg:
            logging.error(msg)

    def get(self, session, c_user):
        '''
        return: `nametuple`
        '''
        r = self._pull(session, c_user)
        if r:
            try:
                for chunk in r.iter_content(chunk_size=None):
                    for data in self._clean(chunk.decode('utf-8')):
                        for msg in self._parse(data):
                            if msg:
                                yield msg
            except exceptions.RequestException as msg:
                logging.error(msg)
