import facebook
from src.api_utils import read_token
from src.utils import url_to_json

import collections

ACCESS_TOKEN = read_token()
graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version='2.3')

try:
    identity = graph.get_object(id="me")
except facebook.GraphAPIError as e:
    print('Something went wrong:', e.type, e.message)

USER_ID = identity['id']
FIRST_NAME = identity['first_name']
LAST_NAME = identity['first_name']
USER_NAME = identity['name']
USER_GENDER = identity['gender']

INBOX_LIMIT = 0
LOOP_LIMIT = 3

try:
    inbox = graph.get_object(id=USER_ID, fields="inbox{to, comments}")
except facebook.GraphAPIError as e:
    print('Something went wrong:', e.type, e.message)

print("Last recent contact:")
contacts = pull_contact_list(inbox['inbox'], loop_limit=LOOP_LIMIT)
for contact in contacts:
    print(contact, contacts[contact]['name'])
