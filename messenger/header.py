
class Header:
    general_header = {
        'origin': 'https://www.messenger.com',
        'authority': 'www.messenger.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ms;q=0.6,zh-CN;q=0.5,ja;q=0.4',
        'pragma': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded'
    }

    @classmethod
    def create(cls, *args, others=None):
        '''

        '''
        header = {}
        for a in args:
            header[a] = cls.general_header[a]
        if 'cache-control' not in header:
            header['cache-control'] = 'no-cache'
        if others:
            header.update(others)

        return header
