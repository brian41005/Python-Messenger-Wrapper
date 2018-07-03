import functools
import types
from collections import defaultdict

from requests import Session

from . import get, send, setting


class Messenger:
    '''
    `Only repacking method of these [get, send, setting] packages`

    ```python
    from messenger import Messenger

    m = Messenger(session, c_user, fb_dtsg)

    # get.get_threads(session, c_user, fb_dtsg, limit=10, before=None)

    m.get_threads(limit=10, before=None)
    ```

    '''

    def __init__(self, session, c_user, fb_dtsg):
        self.__session = self.__copy_session(session)
        self.c_user = c_user
        self.fb_dtsg = fb_dtsg
        self.api = {}
        self.__fetch()

    def __copy_session(self, session):
        s = Session()
        cookie_jar = session.cookies.copy()
        s.cookies.update(cookie_jar)
        return s

    @property
    def session(self):
        return self.__copy_session(self.__session)

    @session.setter
    def session(self, session):
        self.__session = self.__copy_session(session)

    def __partial(self, f, *args):
        new_f = functools.partial(f, *args)
        new_f = functools.update_wrapper(new_f, f)
        return new_f

    def __fetch_module_method(self, module):
        for i in dir(module):
            if isinstance(module.__dict__.get(i), types.FunctionType):
                old_f = module.__dict__.get(i)
                new_f = self.__partial(old_f,
                                       self.__session,
                                       self.c_user,
                                       self.fb_dtsg)
                self.api[old_f.__name__] = new_f

    def __fetch(self):
        for m in [get, send, setting]:
            self.__fetch_module_method(m)

    def __getattr__(self, name):
        if name in self.api:
            return self.api[name]
        raise AttributeError('There is not an api called {}'.format(name))

    def update(self, **kwargs):
        for name, value in kwargs.items():
            # print(self.__dict__)
            if name in self.__dict__:
                self.__dict__[name] = value
            elif getattr(self, name, None):
                setattr(self, name, value)
        self.__fetch()
