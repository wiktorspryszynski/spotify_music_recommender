# Create your views here.
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
import modules.spotify_functions as spotify_functions
import modules.spotify_authorization as spotify_auth
import matplotlib.pyplot as plt
import base64, urllib

import concurrent.futures
from asgiref.sync import sync_to_async

# Asynchronous Spotify callback function
async def spotify_callback(request):
    sp_oauth = spotify_auth.SpotifyAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope=['user-library-read', 'user-read-private', 'user-read-email', 'user-top-read']
    )
    code = request.GET.get('code')
    token_info = await sync_to_async(sp_oauth.get_access_token)(code=code)

    if token_info:
        access_token = token_info['access_token']

        # Fetch user profile and tracks immediately after authentication
        user_profile = await sync_to_async(spotify_functions.current_users_profile)(token=access_token)
        user_saved_tracks = await sync_to_async(spotify_functions.get_current_users_saved_songs)(token=access_token, limit=50)
        user_top_tracks = await sync_to_async(spotify_functions.get_current_users_top_tracks)(token=access_token, limit=50, time_range="long_term")

        # Store this data in session
        await sync_to_async(request.session.__setitem__)('access_token', access_token)
        await sync_to_async(request.session.__setitem__)('user_profile', user_profile)
        await sync_to_async(request.session.__setitem__)('user_saved_tracks', user_saved_tracks)
        await sync_to_async(request.session.__setitem__)('user_top_tracks', user_top_tracks)
        # request.session['access_token'] = access_token
        # request.session['user_profile'] = user_profile
        # request.session['user_saved_tracks'] = user_saved_tracks
        # request.session['user_top_tracks'] = user_top_tracks

        # return redirect('recommended_songs_site')
        
        context = {
            'user_profile': user_profile,
            'user_saved_tracks': user_saved_tracks,
            'user_top_tracks': user_top_tracks,
            'code': code
            }
        return render(request, 'spotify_user.html', context)
    else:
        return redirect('spotify_login')

import matplotlib.pyplot as plt
import seaborn as sns
import io
from django.http import HttpResponse
from collections import Counter

def recommended_songs_site(request):
    import time
    start_time = time.time()
    access_token = request.session.get('access_token')

    if access_token:
        user_profile = request.session.get('user_profile')
        user_saved_tracks = request.session.get('user_saved_tracks')
        user_top_tracks = request.session.get('user_top_tracks')

        all_tracks = user_saved_tracks['items'] + user_top_tracks['items']
        tracks_ids = list(set([track["track"]["id"] if "track" in track else track["id"] for track in all_tracks]))
        user_tracks_audio_features = spotify_functions.get_songs_audio_features(token=access_token, track_list=tracks_ids)

        audio_features_map = {audio['id']: audio for audio in user_tracks_audio_features if audio is not None}

        enriched_tracks = []
        artist_genres_cache = {}
        
        def get_artists_genres_batch(artist_ids):
            if not artist_ids:
                return {}

            artist_genres_map = {}
            
            # Split artist_ids into batches of 50 (limit per API request)
            for i in range(0, len(artist_ids), 50):
                batch_ids = artist_ids[i:i + 50]
                artists_data = spotify_functions.get_several_artists_by_id(access_token, batch_ids)

                for artist in artists_data:
                    artist_genres_map[artist['id']] = artist.get('genres', [])

            return artist_genres_map

        all_artist_ids = set()
        for track in all_tracks:
            artists = track['track']['artists'] if 'track' in track else track['artists']
            for artist in artists:
                all_artist_ids.add(artist['id'])

        artist_genres_cache.update(get_artists_genres_batch(list(all_artist_ids)))

        for track in all_tracks:
            track_id = track["track"]["id"] if "track" in track else track["id"]
            if track_id in audio_features_map:
                combined_data = {
                    **track,
                    'audio_features': audio_features_map[track_id]
                }

                artists = track['track']['artists'] if 'track' in track else track['artists']
                artist_genres_set = set()

                for artist in artists:
                    genres = artist_genres_cache.get(artist['id'], [])
                    artist_genres_set.update(genres)

                combined_data['artist_genres'] = list(artist_genres_set)
                enriched_tracks.append(combined_data)
             
        with open("demofile.txt", "w") as f:
            is_first_track = True
            
            for track in enriched_tracks:
                track_info = spotify_functions.get_relevant_track_info(track)
                
                if is_first_track:
                    f.write(';'.join([*track_info.keys()]))
                    f.write('\n')
                    is_first_track = False
                
                vals_to_write = []
                for v in track_info.values():
                    vals_to_write.append(str(v))
                f.write(str(';'.join(vals_to_write)))
                f.write('\n')

        running_time = round(time.time() - start_time, 2)
        context = {
            'user_profile': user_profile,
            'tracks': enriched_tracks,
            'running_time': running_time
        }
        return render(request, 'recommended_songs_site.html', context)
    else:
        return redirect('spotify_login')


    
    
def spotify_login(request):
    sp_oauth = spotify_auth.SpotifyAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope=['user-library-read', 'user-read-private', 'user-read-email', 'user-top-read'],
        show_dialog=True
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def track_list(request):
    template = loader.get_template('track_list.html')
    token = spotify_functions.get_token()

    author_id = spotify_functions.get_artist_id(token, "Metallica")
    songs = spotify_functions.get_songs_by_artist(token, author_id)

    context = {
        'songs': songs
    }

    return HttpResponse(template.render(context, request))
