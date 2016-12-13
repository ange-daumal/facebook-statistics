import facebook
from src.api_utils import read_token, pull_contact_list, pull_messages


# PARAMETERS
LOOP_LIMIT = 1
INBOX_LIMIT = 10


graph = facebook.GraphAPI(access_token=read_token(), version='2.3')
try:
    identity = graph.get_object(id="me")
except facebook.GraphAPIError as e:
    print('Something went wrong:', e.type, e.message)

USER_ID = identity['id']
FIRST_NAME = identity['first_name']
LAST_NAME = identity['first_name']
USER_NAME = identity['name']
USER_GENDER = identity['gender']

try:
    inbox = graph.get_object(id=USER_ID, fields="inbox{to, comments}")
except facebook.GraphAPIError as e:
    print('Something went wrong:', e.type, e.message)

print("Last recent contact:")
contacts = pull_contact_list(inbox['inbox'], USER_ID, loop_limit=LOOP_LIMIT)
for contact in contacts:
    print(contact, contacts[contact]['name'])

print("Enter the contact number you want to stalk your conversation with:")
target = int(input())

pull_messages(inbox['inbox'], USER_ID, contacts[target]['id'],
        loop_limit=LOOP_LIMIT, inbox_limit=INBOX_LIMIT)
