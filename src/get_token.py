import urllib
from urllib.parse import urlencode
import subprocess

def read_token():
    try:
        with open("user.settings", "r") as access_token:
            ACCESS_TOKEN = access_token.read()
    except:
        print("Please put your access token in user.settings file (see README.md)")
        exit(1)
    return ACCESS_TOKEN

def normal_way_to_get_token():
    FACEBOOK_APP_ID     = 'XXXXXXXXXXXXXXX'
    FACEBOOK_APP_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    FACEBOOK_PROFILE_ID = 'XXXXXX'


    # Trying to get an access token. Very awkward.
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
