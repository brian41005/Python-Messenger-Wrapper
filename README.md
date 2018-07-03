# Python Messenger Wrapper

An unofficial Facebook Messenger Wrapper for Python.

# Installation

```
pip install messenger-wrapper
```
# Developping
for developer
```
Python-Messenger-Wrapper$ pip3 install -e .

```

---
testing
```
Python-Messenger-Wrapper$ python3 tests/tests.py
```

individual testing

```
Python-Messenger-Wrapper$ python3 -m unittest tests.test_set.TestSet.test_save_admin
```
# Example
Login

```python
from meesenger import login
session, c_user, fb_dtsg = login.get_session(user, passwd)
```

Logout

```python
from meesenger import logout
logout(session, fb_dtsg)
```

Pull

```python
from messenger import Pull
p = Pull()
while True:
    for data in p.get(session, c_user):
        ...
```

## Integrated Wrapping
Same as individual usage without passing first three parameters(session, c_user, fb_dtsg)
```python
from messenger import Messenger
m = Messenger(session, c_user, fb_dtsg)
# get.get_threads(session, c_user, fb_dtsg, limit=10, before=None)
m.get_threads(limit=10, before=None)
```
## Individual Use Scenarios

### Getting

Get friends

```python
from meesenger import get

friends = get.get_friends(session, c_user, fb_dtsg)
for uid, f in friends.items():
    ...
```

Get message

```python
from meesenger import get

messages = get.get_msg(session, c_user, fb_dtsg, recipient_id, 10, before=None)

for m in messages:
    ...
```

Get threads

```python
from meesenger import get

threads = get.get_threads(session, c_user, fb_dtsg, limit=10, before=None)    
for t in threads:
    ...
```
### Sending

Send message

```python
from messenger import send

body = 'Hello, world'
recipient_id = 'fb user id'

send.send_msg(session, c_user, fb_dtsg, recipient_id, body, group=True)
```

Upload file

Send file


### Setting

Set emoji

```python
from messenger import setting

thread_id = 'thread id'
emoji = '👍'

setting.set_emoji(session, c_user, fb_dtsg, thread_id, emoji)
```

Set nickname

```python
from messenger import setting

thread_id = 'thread id'
participant = 'member user id'
new_name = 'new nickname'

setting.set_nickname(session, c_user, fb_dtsg, thread_id, participant, new_name)
```

Set thread name

```python
from messenger import setting

new_name = 'new name'
thread_id = 'thread id'

setting.set_thread_name(session, c_user, fb_dtsg, thread_id, new_name)
```

Add people into group

```python
from messenger import setting

thread_id = 'thread id'
participants = ['participant 1', 'participant 2']

setting.add_participant(session, c_user, fb_dtsg, thread_id, participants)
```

Remove from group 

```python
from messenger import setting

thread_id = 'thread id'
participant = 'member user should be removed'

setting.rm_participant(session, c_user, fb_dtsg, thread_id, participant)
```

Make admin

```python
from messenger import setting

thread_id = 'thread id'
member_id = 'member user should be made as admin'

setting.save_admin(session, c_user, fb_dtsg, thread_id, member_id, add=True)

```

Remove admin

```python
from messenger import setting

thread_id = 'thread id'
member_id = 'member user should be removed from admin'

setting.save_admin(session, c_user, fb_dtsg, thread_id, member_id, add=False)

```

Leave group

```python
from messenger import setting

setting.leave_group(session, c_user, fb_dtsg, thread_id)
```