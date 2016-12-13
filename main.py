import facebook
from src.get_token import read_token

ACCESS_TOKEN = read_token()
print(ACCESS_TOKEN)
graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version='2.2')
