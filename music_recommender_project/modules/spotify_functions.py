import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get

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

    result = get(url=url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result
    return None


def get_artist_info(token, artist_name):
    url = "https://api.spotify.com/v1/search?"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    query_url = url + query

    result = get(url=url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result['artists']['items'][0]
    return None


def get_artist_id(token, artist_name):
    res = get_artist_info(token, artist_name)
    if res:
        return res["id"]
    return None


def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)

    result = get(url=url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result["tracks"]
    return None


def get_several_songs_by_ids(token, users_market: str, song_ids: list[str]):
    ids = ','.join(song_ids)
    url = f'https://api.spotify.com/v1/tracks?'
    if users_market:
        url += f'market={users_market}&'
    url += f'ids={ids}'
        
    headers = get_auth_header(token)

    result = get(url=url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result['tracks']
    return None


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
    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result
    return None

def get_current_users_saved_songs(token, limit: int = 20, offset: int = 0, market: str = ""):
    '''
    :param limit: max items to return (range = 0 - 50, default = 20)
    :param offset: index of 1st item, can use with limit to return next set of tracks (default = 0)
    :param market: (None by default) - An ISO 3166-1 alpha-2 country code, if specified, only returns track if available in that market (default None)
    https://developer.spotify.com/documentation/web-api/reference/get-users-saved-tracks
    '''
    url = f"https://api.spotify.com/v1/me/tracks/?limit={limit}&offset={offset}"
    headers = get_auth_header(token)
    
    if market:
        url = f'?market={market}'
    
    result = get(url=url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result
    return None

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
    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result
    return None

def get_songs_audio_features(token, track_list: list[str]):
    """
    IMPORTANT NOTE:
    
    As of december 2024, Spotify deprecated their audio features endpoint, rendering this app useless.
    I am keeping the code responsible for handling audio features in case they revert the changes.
    
    As such, this function will most likely return None instead of audio_features.
    
    Get several songs audio features, up to a 100 at a time\n

        :param track_list: list of ID's of songs to get audio features of
        
    """
    ids = ','.join(track_list)
    url = f'https://api.spotify.com/v1/audio-features?ids={ids}'
    headers = get_auth_header(token)

    result = get(url=url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result['audio_features']
    return None

def get_artist_by_id(token, artist_id: str):
    """Fetch info about artist by Spotify ID (can be obtained using get_artist_id() function)

    Args:
        token : self explanatory
        artist_id (str): Artist's Spotify ID

    Returns:
        JSON object with artist's info (including genres!)
    """
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = get_auth_header(token)

    result = get(url=url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result
    return None


def get_several_artists_by_id(token, artists_id: list[str]):
    """Fetch info about multiple (up to 50 at a time) artists by using Spotify ID's (IDs can be obtained using get_artist_id() function)

    Args:
        token : self explanatory
        artist_id (list(str)): list of artist's Spotify IDs

    Returns:
        JSON object with artist's info (including genres!)
    """
    ids = ",".join(artists_id)
    url = f'https://api.spotify.com/v1/artists/?ids={ids}'
    headers = get_auth_header(token)

    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)
    
    if "artists" not in json_result:
        print("No artist found or error in response")
        return None

    return json_result["artists"]



def get_relevant_track_info(track_data):
    """
    Extracts relevant information from Spotify track data, handling both types of structures.

    Args:
    track_data (dict): The track dictionary fetched from Spotify's API.

    Returns:
    dict: A dictionary with relevant song features for ML.
    """
    
    if 'track' in track_data:
        track = track_data['track']
        audio_features = track_data.get('audio_features', {})
        artist_genres = track_data.get('artist_genres', [])
    else:
        track = track_data
        audio_features = track_data.get('audio_features', {})
        artist_genres = track_data.get('artist_genres', [])
    
    artist_names = [artist['name'] for artist in track['artists']]
    song_name = track.get('name', 'Unknown Song')
    track_id = track.get('id', 'Unknown ID')
    duration_ms = track.get('duration_ms', 0)
    release_date = track['album'].get('release_date', 'Unknown release date')
    explicit = track.get('explicit', False)
    popularity = track.get('popularity', 0)
    
    unpacked_audio_features = {
        'danceability': audio_features.get('danceability', 0),
        'energy': audio_features.get('energy', 0),
        'key': audio_features.get('key', 0),
        'loudness': audio_features.get('loudness', 0),
        'mode': audio_features.get('mode', 0),
        'speechiness': audio_features.get('speechiness', 0),
        'acousticness': audio_features.get('acousticness', 0),
        'instrumentalness': audio_features.get('instrumentalness', 0),
        'liveness': audio_features.get('liveness', 0),
        'valence': audio_features.get('valence', 0),
        'tempo': audio_features.get('tempo', 0),
        #'time_signature': audio_features.get('time_signature', 0),
        'duration_ms': audio_features.get('duration_ms', 0)
    }

    return {
        'artist_names': artist_names,
        'song_name': song_name,
        'track_id': track_id,
        'release_date': release_date,
        'duration_ms': duration_ms,
        'genres': artist_genres,
        'explicit': explicit,
        'popularity': popularity,
        **unpacked_audio_features
    }
    
    
def get_artists_genres_batch(access_token, artist_ids):
        if not artist_ids:
            return {}

        artist_genres_map = {}
        
        # Split artist_ids into batches of 50 (limit per API request)
        for i in range(0, len(artist_ids), 50):
            batch_ids = artist_ids[i:i + 50]
            artists_data = get_several_artists_by_id(access_token, batch_ids)

            for artist in artists_data:
                artist_genres_map[artist['id']] = artist.get('genres', [])

        return artist_genres_map

def save_music_audio_features_to_file(enriched_tracks, file_name):
    with open(file_name, "w") as f:
        is_first_track = True
        
        for track in enriched_tracks:
            track_info = get_relevant_track_info(track)
            
            if is_first_track:
                f.write(';'.join([*track_info.keys()]))
                f.write('\n')
                is_first_track = False
            
            vals_to_write = []
            for v in track_info.values():
                vals_to_write.append(str(v))
            f.write(str(';'.join(vals_to_write)))
            f.write('\n')


def create_playlist(user_id, access_token):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "name": "Moja polecana playlista :~)",
        "description": "Playlista stworzona na podstawie twojego gustu muzycznego",
        "public": False
    }
    
    response = post(url, json=data, headers=headers)
    
    if response.status_code < 300:
        playlist = response.json()
        return playlist['id']
    else:
        print(f"Error creating playlist: {response.status_code} {response.json()}")
        return None


def add_songs_to_playlist(playlist_id, track_ids, access_token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Prepare the track URIs (prefix 'spotify:track:' to the track IDs)
    track_uris = [f"spotify:track:{track_id}" for track_id in track_ids]
    
    data = {
        "uris": track_uris
    }
    
    response = post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        print("Songs added to playlist successfully")
    else:
        print(f"Error adding songs: {response.status_code}")
    
    return response.status_code
