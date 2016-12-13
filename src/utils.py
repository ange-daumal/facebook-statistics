import urllib
import json

def url_to_json(url):
    next = urllib.request.urlopen(url)
    next = next.read().decode("utf-8")
    next = json.loads(next)
    return next
