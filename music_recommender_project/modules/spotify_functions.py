import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get
from urllib.parse import urlparse

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


def get_current_users_top_tracks(token, limit: int = 20, time_range: str = "medium_term"):
    '''
    :param limit: max items to return (range = 0 - 50, default = 20)
    :param time_range:
        long_term = last ~1 year of music data\n
        medium_term = last ~6 months\n
        short_term = last ~4 weeks\n
    '''
    url = f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}"
    headers = get_auth_header(token)

    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)

    if len(json_result) == 0:
        print("No user's top tracks found")
        return None
    return json_result

def get_current_users_saved_songs(token, limit: int = 20, offset: int = 0, market: str = ""):
    '''
    :param limit: max items to return (range = 0 - 50, default = 20)
    :param offset: index of 1st item, can use with limit to return next set of tracks (default = 0)
    :param market: (None by default) - An ISO 3166-1 alpha-2 country code, if specified, only returns track if available in that market (default None)
    https://developer.spotify.com/documentation/web-api/reference/get-users-saved-tracks
    '''
    url = f"https://api.spotify.com/v1/me/tracks/?limit={limit}&offset={offset}"
    headers = get_auth_header(token)
    
    if market != "":
        url = f'?market={market}'
    
    result = get(url=url, headers=headers)
    # if result.status_code == 404:
    #     print("result status 404")
    #     return None
    
    json_result = json.loads(result.content)

    if len(json_result) == 0:
        print("No user's top tracks found")
        return None
    return json_result

def get_current_users_top_artists(token, limit: int = 20, time_range: str = "medium_term"):
    '''
    :param limit: max items to return (range = 0 - 50, default = 20)
    :param time_range:
        long_term = last ~1 year of music data\n
        medium_term = last ~6 months\n
        short_term = last ~4 weeks\n
    '''
    url = f"https://api.spotify.com/v1/me/top/artists/?time_range={time_range}&limit={limit}"
    headers = get_auth_header(token)

    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)

    if len(json_result) == 0:
        print("No user's top artists found")
        return None
    return json_result

def get_songs_audio_features(token, track_list: list[str]):
    """
    Get several songs audio features, up to a 100 at a time\n

        :param track_list: list of ID's of songs to get audio features of
    """
    ids = '%2C'.join(track_list) # '%2C' is a URL-encoded comma
    url = f'https://api.spotify.com/v1/audio-features?ids={ids}'
    headers = get_auth_header(token)

    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)

    return json_result['audio_features']

def get_artist_by_id(token, artist_id: str):
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    # print(url)
    headers = get_auth_header(token)

    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)
    
    if len(json_result) == 0:
        print("No artist found")
        return None
    return json_result
