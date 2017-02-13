import urllib
import json

def url_to_json(url):
    try:
        next = urllib.request.urlopen(url)
        next = next.read().decode("utf-8")
        next = json.loads(next)
    except facebook.GraphAPIError as e:
        print('Something went wrong:', e.type, e.message)
        raise
    except:
        print("Failed access to %s" % url)
        raise
    return next
