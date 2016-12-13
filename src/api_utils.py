import urllib
from urllib.parse import urlencode
import subprocess
import collections
from src.utils import url_to_json

def read_token():
    try:
        with open("user.settings", "r") as access_token:
            ACCESS_TOKEN = access_token.read().split()[0]
    except:
        print("Please put your access token in user.settings file (see README.md)")
        exit(1)
    return ACCESS_TOKEN


def pull_contact_list(inbox, USER_ID, loop_limit=2):
    n_contact = 0
    contacts = collections.OrderedDict()
    for i in range(loop_limit):
        for conversation_list in inbox['data']:
            to = conversation_list['to']['data']
            # Only handle 1 to 1 conversation
            if len(to) == 2:
                interlocutor = to[0] if to[1]['id'] == USER_ID else to[1]
                contacts.update({n_contact : interlocutor})
                n_contact = len(contacts)
        inbox = url_to_json(inbox['paging']['next'])
    return contacts




# This is not used, but should be, actually.
def normal_way_to_get_token():
    FACEBOOK_APP_ID     = 'XXXXXXXXXXXXXXX'
    FACEBOOK_APP_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    FACEBOOK_PROFILE_ID = 'XXXXXX'

    oauth_args = dict(client_id     = FACEBOOK_APP_ID,
            client_secret = FACEBOOK_APP_SECRET,
            grant_type    = 'client_credentials')
    oauth_curl_cmd = ['curl', 'https://graph.facebook.com/oauth/access_token?' + \
            urlencode(oauth_args)]
    oauth_response = subprocess.Popen(oauth_curl_cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE).communicate()[0]

    try:
        ACCESS_TOKEN = urllib.parse.parse_qs(str(oauth_response))['access_token'][0]
    except KeyError:
        print('Unable to grab an access token!')
        exit(1)
