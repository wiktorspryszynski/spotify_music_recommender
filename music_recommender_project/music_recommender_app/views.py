# # Create your views here.
# from django.shortcuts import redirect, render
# from django.conf import settings
# from django.http import HttpResponse
# from django.template import loader
# import modules.spotify_functions as spotify_functions

# from spotipy.oauth2 import SpotifyOAuth
# import spotipy

# # def recommended_songs_site(request):
# #     sp_oauth = SpotifyOAuth(
# #         client_id=settings.SPOTIFY_CLIENT_ID,
# #         client_secret=settings.SPOTIFY_CLIENT_SECRET,
# #         redirect_uri=settings.SPOTIFY_REDIRECT_URI,
# #         scope='user-library-read, user-read-private, user-read-email, user-top-read'
# #     )
# #     code = request.GET.get('code')
# #     token_info = sp_oauth.get_access_token(code)
# #     token = spotify_functions.get_token()
# #     user_profile = spotify_functions.current_users_profile(token)
# #     context = {
# #         'user_profile': user_profile,
# #     }
# #     return render(request, 'recommended_songs_site.html', context)


# def recommended_songs_site(request):
#     sp_oauth = SpotifyOAuth(
#         client_id=settings.SPOTIFY_CLIENT_ID,
#         client_secret=settings.SPOTIFY_CLIENT_SECRET,
#         redirect_uri=settings.SPOTIFY_REDIRECT_URI,
#         scope='user-library-read, user-read-private, user-read-email, user-top-read'
#     )
#     code = request.GET.get('code')
#     token_info = sp_oauth.get_access_token(code)
    
#     if token_info:
#         access_token = token_info['access_token']
#         sp = spotipy.Spotify(auth=access_token)
#         user_profile = sp.current_user()
#         user_top_tracks = sp.current_user_top_tracks(limit=50, time_range="long_term")
#         user_saved_tracks = sp.current_user_saved_tracks(limit=50)
        
#         all_tracks = user_saved_tracks['items'] + user_top_tracks['items']
        
#         tracks_ids = list(set([track["track"]["id"] if "track" in track else track["id"] for track in all_tracks]))

#         user_tracks_audio_features = sp.audio_features(tracks=tracks_ids)

#         audio_features_map = {audio['id']: audio for audio in user_tracks_audio_features if audio is not None}
        
#         with open("demofile.txt", "w") as f:
#             written_ids = set()
#             for song in all_tracks:
#                 track_id = song['track']['id'] if 'track' in song else song['id']
                
#                 if track_id not in written_ids:
#                     written_ids.add(track_id)
                    
#                     if track_id in audio_features_map:
#                         audio = audio_features_map[track_id]
                        
#                         f.write(f'name: {song["track"]["name"] if "track" in song else song["name"]}\n')
#                         f.write('artists: ')
#                         artists = song['track']['artists'] if 'track' in song else song['artists']
#                         artist_ids = [artist['id'] for artist in artists]
#                         for artist in artists:
#                             f.write(f'{artist["name"]}  ')
#                         f.write('\n')
                        
#                         genres = set()
#                         for artist_id in artist_ids:
#                             artist_info = sp.artist(artist_id)
#                             genres.update(artist_info.get('genres', []))
#                         f.write(f'genres: {", ".join(genres) if genres else "Unknown"}\n')
                        
#                         for key, val in audio.items():
#                             if key not in ['type', 'uri', 'track_href', 'analysis_url']:
#                                 f.write(f'{key}: {val}\n')
#                         f.write('\n\n')

#         context = {
#             'user_profile': user_profile,
#             'user_saved_tracks': user_saved_tracks,
#             'user_top_tracks': user_top_tracks,
#             'user_tracks_audio_features': user_tracks_audio_features
#         }
#         return render(request, 'recommended_songs_site.html', context)
#     else:
#         return redirect('spotify_login')


# def spotify_login(request):
#     sp_oauth = SpotifyOAuth(
#         client_id=settings.SPOTIFY_CLIENT_ID,
#         client_secret=settings.SPOTIFY_CLIENT_SECRET,
#         redirect_uri=settings.SPOTIFY_REDIRECT_URI,
#         scope='user-library-read, user-read-private, user-read-email, user-top-read',
#         show_dialog=True
#     )
#     auth_url = sp_oauth.get_authorize_url()
#     return redirect(auth_url)

# def spotify_callback(request):
#     sp_oauth = SpotifyOAuth(
#         client_id=settings.SPOTIFY_CLIENT_ID,
#         client_secret=settings.SPOTIFY_CLIENT_SECRET,
#         redirect_uri=settings.SPOTIFY_REDIRECT_URI,
#         scope='user-library-read, user-read-private, user-read-email, user-top-read'
#     )
#     code = request.GET.get('code')
#     token_info = sp_oauth.get_access_token(code)
    
#     if token_info:
#         access_token = token_info['access_token']
#         sp = spotipy.Spotify(auth=access_token)
#         user_profile = sp.current_user()
#         user_top_tracks = sp.current_user_top_tracks(limit=50, time_range="long_term")
#         user_saved_tracks = sp.current_user_saved_tracks(limit=50)
#         #user_top_tracks = spotify_functions.get_current_users_top_songs(token=access_token, type="tracks")
#         context = {
#             'user_profile': user_profile,
#             'user_saved_tracks': user_saved_tracks,
#             'user_top_tracks': user_top_tracks
#             }
#         return render(request, 'spotify_user.html', context)
#     else:
#         return redirect('spotify_login')


# def index(request):
#     template = loader.get_template('index.html')
#     return HttpResponse(template.render())
    
    
# def track_list(request):
#     template = loader.get_template('track_list.html')
#     token = spotify_functions.get_token()

#     trav_id = spotify_functions.get_artist_id(token, "$uicideboy$")
#     songs = spotify_functions.get_songs_by_artist(token, trav_id)

#     context = {
#         'songs': songs
#     }

#     return HttpResponse(template.render(context, request))
# Create your views here.
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
import modules.spotify_functions as spotify_functions
import modules.spotify_authorization as spotify_auth
import os

from spotipy.oauth2 import SpotifyOAuth
import spotipy

# def recommended_songs_site(request):
#     sp_oauth = SpotifyOAuth(
#         client_id=settings.SPOTIPY_CLIENT_ID,
#         client_secret=settings.SPOTIPY_CLIENT_SECRET,
#         redirect_uri=settings.SPOTIPY_REDIRECT_URI,
#         scope='user-library-read, user-read-private, user-read-email, user-top-read'
#     )
#     code = request.GET.get('code')
#     token_info = sp_oauth.get_access_token(code)
#     token = spotify_functions.get_token()
#     user_profile = spotify_functions.current_users_profile(token)
#     context = {
#         'user_profile': user_profile,
#     }
#     return render(request, 'recommended_songs_site.html', context)


# def recommended_songs_site(request):
#     sp_oauth = spotify_auth.SpotifyAuth(
#         client_id=settings.SPOTIFY_CLIENT_ID,
#         client_secret=settings.SPOTIFY_CLIENT_SECRET,
#         redirect_uri=settings.SPOTIFY_REDIRECT_URI,
#         scope=['user-library-read', 'user-read-private', 'user-read-email', 'user-top-read']
#     )
#     code = request.GET.get('code')
#     token_info = sp_oauth.get_access_token(code=code)
#     print(f'\ntoken_info:\n{token_info}\n\n')
    
#     if token_info:
#         access_token = token_info['access_token']
#         user_profile = spotify_functions.current_users_profile(token=access_token)
#         user_saved_tracks = spotify_functions.get_current_users_saved_songs(token=access_token, limit=50)
#         user_top_tracks = spotify_functions.get_current_users_top_tracks(token=access_token, limit=50, time_range="long_term")
        
#         all_tracks = user_saved_tracks['items'] + user_top_tracks['items']
        
#         tracks_ids = list(set([track["track"]["id"] if "track" in track else track["id"] for track in all_tracks]))
#         #########################################################################################
#         user_tracks_audio_features = spotify_functions.get_songs_audio_features(tracks=tracks_ids)

#         # audio_features_map = {audio['id']: audio for audio in user_tracks_audio_features if audio is not None}
        
#         # with open("demofile.txt", "w") as f:
#         #     written_ids = set()
#         #     for song in all_tracks:
#         #         track_id = song['track']['id'] if 'track' in song else song['id']
                
#         #         if track_id not in written_ids:
#         #             written_ids.add(track_id)
                    
#         #             if track_id in audio_features_map:
#         #                 audio = audio_features_map[track_id]
                        
#         #                 f.write(f'name: {song["track"]["name"] if "track" in song else song["name"]}\n')
#         #                 f.write('artists: ')
#         #                 artists = song['track']['artists'] if 'track' in song else song['artists']
#         #                 artist_ids = [artist['id'] for artist in artists]
#         #                 for artist in artists:
#         #                     f.write(f'{artist["name"]}  ')
#         #                 f.write('\n')
                        
#         #                 genres = set()
#         #                 for artist_id in artist_ids:
#         #                     #########################################################################################
#         #                     artist_info = sp.artist(artist_id)
#         #                     genres.update(artist_info.get('genres', []))
#         #                 f.write(f'genres: {", ".join(genres) if genres else "Unknown"}\n')
                        
#         #                 for key, val in audio.items():
#         #                     if key not in ['type', 'uri', 'track_href', 'analysis_url']:
#         #                         f.write(f'{key}: {val}\n')
#         #                 f.write('\n\n')

#         context = {
#             'user_profile': user_profile,
#             'user_saved_tracks': user_saved_tracks,
#             'user_top_tracks': user_top_tracks,
#             'user_tracks_audio_features': user_tracks_audio_features
#         }
#         return render(request, 'recommended_songs_site.html', context)
#     else:
#         return redirect('spotify_login')
def recommended_songs_site(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope='user-library-read, user-read-private, user-read-email, user-top-read'
    )
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    
    if token_info:
        access_token = token_info['access_token']
        sp = spotipy.Spotify(auth=access_token)
        user_profile = sp.current_user()
        user_top_tracks = sp.current_user_top_tracks(limit=50, time_range="long_term")
        user_saved_tracks = sp.current_user_saved_tracks(limit=50)
        
        all_tracks = user_saved_tracks['items'] + user_top_tracks['items']
        
        tracks_ids = list(set([track["track"]["id"] if "track" in track else track["id"] for track in all_tracks]))

        user_tracks_audio_features = sp.audio_features(tracks=tracks_ids)

        audio_features_map = {audio['id']: audio for audio in user_tracks_audio_features if audio is not None}
        
        with open("demofile.txt", "w") as f:
            written_ids = set()
            for song in all_tracks:
                track_id = song['track']['id'] if 'track' in song else song['id']
                
                if track_id not in written_ids:
                    written_ids.add(track_id)
                    
                    if track_id in audio_features_map:
                        audio = audio_features_map[track_id]
                        
                        f.write(f'name: {song["track"]["name"] if "track" in song else song["name"]}\n')
                        f.write('artists: ')
                        artists = song['track']['artists'] if 'track' in song else song['artists']
                        artist_ids = [artist['id'] for artist in artists]
                        for artist in artists:
                            f.write(f'{artist["name"]}  ')
                        f.write('\n')
                        
                        genres = set()
                        for artist_id in artist_ids:
                            artist_info = sp.artist(artist_id)
                            genres.update(artist_info.get('genres', []))
                        f.write(f'genres: {", ".join(genres) if genres else "Unknown"}\n')
                        
                        for key, val in audio.items():
                            if key not in ['type', 'uri', 'track_href', 'analysis_url']:
                                f.write(f'{key}: {val}\n')
                        f.write('\n\n')

        context = {
            'user_profile': user_profile,
            'user_saved_tracks': user_saved_tracks,
            'user_top_tracks': user_top_tracks,
            'user_tracks_audio_features': user_tracks_audio_features
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
        #show_dialog=True
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def spotify_callback(request):
    sp_oauth = spotify_auth.SpotifyAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope=['user-library-read', 'user-read-private', 'user-read-email', 'user-top-read']
    )
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code=code)
    
    if token_info:
        access_token = token_info['access_token']
        user_profile = spotify_functions.current_users_profile(token=access_token)
        user_saved_tracks = spotify_functions.get_current_users_saved_songs(token=access_token, limit=50)
        user_top_tracks = spotify_functions.get_current_users_top_tracks(token=access_token, limit=50, time_range="long_term")
        context = {
            'user_profile': user_profile,
            'user_saved_tracks': user_saved_tracks,
            'user_top_tracks': user_top_tracks,
            'code': code
            }
        return render(request, 'spotify_user.html', context)
    else:
        return redirect('spotify_login')


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
    
    
def track_list(request):
    template = loader.get_template('track_list.html')
    token = spotify_functions.get_token()

    trav_id = spotify_functions.get_artist_id(token, "$uicideboy$")
    songs = spotify_functions.get_songs_by_artist(token, trav_id)

    context = {
        'songs': songs
    }

    return HttpResponse(template.render(context, request))
