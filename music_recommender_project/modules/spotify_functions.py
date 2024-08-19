import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get

# import spotipy


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET") 

def get_token():
    auth_token = client_id + ":" + client_secret
    auth_bytes = auth_token.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url=url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    print(token)
    return {"Authorization": "Bearer " + token}

def current_users_profile(token):
    url = 'https://api.spotify.com/v1/me'
    headers = get_auth_header(token)
    
    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)

    if len(json_result) == 0:
        print("User not found")
        return None
    return json_result


def get_artist_info(token, artist_name):
    url = "https://api.spotify.com/v1/search?"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    query_url = url + query

    result = get(url=query_url, headers=headers)
    json_result = json.loads(result.content)

    if len(json_result) == 0:
        print("No artist found")
        return None
    return json_result['artists']['items'][0]


def get_artist_id(token, artist_name):
    res = get_artist_info(token, artist_name)
    if res:
        return res["id"]
    return None


def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)

    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)

    if len(json_result) == 0:
        print("No artist's top tracks found")
        return None
    return json_result["tracks"]


'''
long_term: last ~1 year of music data
medium_term: last ~6 months
short_term: last ~4 weeks

type = ["artists", "tracks"], 
type = "tracks" by default
'''
def get_current_users_top_songs(token, type="tracks"):
    url = f"https://api.spotify.com/v1/me/top/{type}"
    headers = get_auth_header(token)

    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)

    if len(json_result) == 0:
        print("No user's top tracks found")
        return None
    return json_result

if __name__ == '__main__':
    token = get_token()
    u = current_users_profile(token)
    print(u)