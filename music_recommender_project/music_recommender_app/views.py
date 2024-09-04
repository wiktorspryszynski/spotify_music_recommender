# # Create your views here.
# from django.shortcuts import redirect, render
# from django.conf import settings
# from django.http import HttpResponse
# from django.template import loader
# import modules.spotify_functions as spotify_functions
# import modules.spotify_authorization as spotify_auth

# import concurrent.futures

# def recommended_songs_site(request):
#     global token_info
    
#     if token_info:
#         access_token = token_info['access_token']
#         user_profile = spotify_functions.current_users_profile(token=access_token)
#         user_saved_tracks = spotify_functions.get_current_users_saved_songs(token=access_token, limit=50)
#         user_top_tracks = spotify_functions.get_current_users_top_tracks(token=access_token, limit=50, time_range="long_term")
        
#         all_tracks = user_saved_tracks['items'] + user_top_tracks['items']
#         tracks_ids = list(set([track["track"]["id"] if "track" in track else track["id"] for track in all_tracks]))
#         user_tracks_audio_features = spotify_functions.get_songs_audio_features(token=access_token, track_list=tracks_ids)
        
#         audio_features_map = {audio['id']: audio for audio in user_tracks_audio_features if audio is not None}
        
#         # Combine all_tracks and audio_features_map into a single data structure with nested audio features
#         enriched_tracks = []
#         for track in all_tracks:
#             track_id = track["track"]["id"] if "track" in track else track["id"]
#             if track_id in audio_features_map:
#                 # Add a nested 'audio_features' dict to the track data
#                 combined_data = {
#                     **track, 
#                     'audio_features': audio_features_map[track_id]
#                 }
#                 enriched_tracks.append(combined_data)
        
#         artist_genres_cache = {}
        
#         # Fetch artist info concurrently
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             future_to_artist = {executor.submit(spotify_functions.get_artist_by_id, access_token, artist['id']): artist['id'] for track in enriched_tracks for artist in (track['track']['artists'] if 'track' in track else track['artists'])}
#             for future in concurrent.futures.as_completed(future_to_artist):
#                 artist_id = future_to_artist[future]
#                 try:
#                     artist_genres_cache[artist_id] = future.result().get('genres', [])
#                 except Exception as e:
#                     artist_genres_cache[artist_id] = []
        
#         # Write enriched data to the file
#         with open("demofile.txt", "w") as f:
#             written_ids = set()
#             for track in enriched_tracks:
#                 track_id = track["track"]["id"] if "track" in track else track["id"]
                
#                 if track_id not in written_ids:
#                     written_ids.add(track_id)
                    
#                     f.write(f'name: {track["track"]["name"] if "track" in track else track["name"]}\n')
#                     f.write('artists: ')
#                     artists = track['track']['artists'] if 'track' in track else track['artists']
#                     genres = set()
#                     artists_names = []
#                     for artist in artists:
#                         artists_names.append(artist["name"])
#                         genres.update(artist_genres_cache.get(artist['id'], []))
#                     f.write(f'{", ".join(artists_names)}\n')
#                     f.write(f'genres: {", ".join(genres) if genres else "Unknown"}\n')
                    
#                     # Write the nested audio features
#                     f.write('audio_features:\n')
#                     audio_features = track['audio_features']
#                     for key, val in audio_features.items():
#                         if key not in ['type', 'uri', 'track_href', 'analysis_url']:
#                             f.write(f'  {key}: {val}\n')
#                     f.write('\n\n')

#         context = {
#             'user_profile': user_profile,
#             'user_saved_tracks': user_saved_tracks,
#             # 'user_top_tracks': user_top_tracks,
#             # 'user_tracks_audio_features': user_tracks_audio_features
#             'tracks': enriched_tracks
#         }
#         return render(request, 'recommended_songs_site.html', context)
#     else:
#         return redirect('spotify_login')


# # def recommended_songs_site(request):
# #     global token_info
    
# #     if token_info:
# #         access_token = token_info['access_token']
# #         user_profile = spotify_functions.current_users_profile(token=access_token)
# #         user_saved_tracks = spotify_functions.get_current_users_saved_songs(token=access_token, limit=50)
# #         user_top_tracks = spotify_functions.get_current_users_top_tracks(token=access_token, limit=50, time_range="long_term")
        
# #         all_tracks = user_saved_tracks['items'] + user_top_tracks['items']
        
# #         tracks_ids = list(set([track["track"]["id"] if "track" in track else track["id"] for track in all_tracks]))
# #         user_tracks_audio_features = spotify_functions.get_songs_audio_features(token=access_token ,track_list=tracks_ids)

# #         audio_features_map = {audio['id']: audio for audio in user_tracks_audio_features if audio is not None}
        
# #         with open("demofile.txt", "w") as f:
# #             written_ids = set()
# #             for song in all_tracks:
# #                 track_id = song['track']['id'] if 'track' in song else song['id']
                
# #                 if track_id not in written_ids:
# #                     written_ids.add(track_id)
                    
# #                     if track_id in audio_features_map:
# #                         audio = audio_features_map[track_id]
# #                         print(str(audio)+'\n')
# #                         f.write(f'name: {song["track"]["name"] if "track" in song else song["name"]}\n')
# #                         f.write('artists: ')
# #                         artists = song['track']['artists'] if 'track' in song else song['artists']
# #                         artist_ids = [artist['id'] for artist in artists]
# #                         artists_names = []
# #                         for artist in artists:
# #                             artists_names.append(artist["name"])
# #                         f.write(f"{', '.join(artists_names)}\n")
                        
# #                         genres = set()
# #                         for artist_id in artist_ids:
# #                             artist_info = spotify_functions.get_artist_by_id(token=access_token, artist_id=artist_id)
# #                             genres.update(artist_info.get('genres', []))
# #                         f.write(f'genres: {", ".join(genres) if genres else "Unknown"}\n')
                        
# #                         for key, val in audio.items():
# #                             if key not in ['type', 'uri', 'track_href', 'analysis_url']:
# #                                 f.write(f'{key}: {val}\n')
# #                         f.write('\n\n')

# #         context = {
# #             'user_profile': user_profile,
# #             'user_saved_tracks': user_saved_tracks,
# #             'user_top_tracks': user_top_tracks,
# #             'user_tracks_audio_features': user_tracks_audio_features
# #         }
# #         return render(request, 'recommended_songs_site.html', context)
# #     else:
# #         return redirect('spotify_login')
    

# def spotify_login(request):
#     sp_oauth = spotify_auth.SpotifyAuth(
#         client_id=settings.SPOTIFY_CLIENT_ID,
#         client_secret=settings.SPOTIFY_CLIENT_SECRET,
#         redirect_uri=settings.SPOTIFY_REDIRECT_URI,
#         scope=['user-library-read', 'user-read-private', 'user-read-email', 'user-top-read'],
#         show_dialog=True
#     )
#     auth_url = sp_oauth.get_authorize_url()
#     return redirect(auth_url)

# def spotify_callback(request):
#     global sp_oauth, token_info
#     sp_oauth = spotify_auth.SpotifyAuth(
#         client_id=settings.SPOTIFY_CLIENT_ID,
#         client_secret=settings.SPOTIFY_CLIENT_SECRET,
#         redirect_uri=settings.SPOTIFY_REDIRECT_URI,
#         scope=['user-library-read', 'user-read-private', 'user-read-email', 'user-top-read']
#     )
#     code = request.GET.get('code')
#     token_info = sp_oauth.get_access_token(code=code)
    
#     if token_info:
#         access_token = token_info['access_token']
#         user_profile = spotify_functions.current_users_profile(token=access_token)
#         user_saved_tracks = spotify_functions.get_current_users_saved_songs(token=access_token, limit=50)
#         user_top_tracks = spotify_functions.get_current_users_top_tracks(token=access_token, limit=50, time_range="long_term")
#         context = {
#             'user_profile': user_profile,
#             'user_saved_tracks': user_saved_tracks,
#             'user_top_tracks': user_top_tracks,
#             'code': code
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

#     author_id = spotify_functions.get_artist_id(token, "Metallica")
#     songs = spotify_functions.get_songs_by_artist(token, author_id)

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

# Recommendation view leveraging preloaded data
# def recommended_songs_site(request):
#     access_token = request.session.get('access_token')

#     if access_token:
#         # Retrieve data from session
#         user_profile = request.session.get('user_profile')
#         user_saved_tracks = request.session.get('user_saved_tracks')
#         user_top_tracks = request.session.get('user_top_tracks')

#         all_tracks = user_saved_tracks['items'] + user_top_tracks['items']
#         tracks_ids = list(set([track["track"]["id"] if "track" in track else track["id"] for track in all_tracks]))
#         user_tracks_audio_features = spotify_functions.get_songs_audio_features(token=access_token, track_list=tracks_ids)

#         audio_features_map = {audio['id']: audio for audio in user_tracks_audio_features if audio is not None}

#         enriched_tracks = []
#         for track in all_tracks:
#             track_id = track["track"]["id"] if "track" in track else track["id"]
#             if track_id in audio_features_map:
#                 combined_data = {
#                     **track,
#                     'audio_features': audio_features_map[track_id]
#                 }
#                 enriched_tracks.append(combined_data)

#         artist_genres_cache = {}
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             future_to_artist = {
#                 executor.submit(spotify_functions.get_artist_by_id, access_token, artist['id']): artist['id']
#                 for track in enriched_tracks for artist in (track['track']['artists'] if 'track' in track else track['artists'])
#             }
#             for future in concurrent.futures.as_completed(future_to_artist):
#                 artist_id = future_to_artist[future]
#                 try:
#                     artist_genres_cache[artist_id] = future.result().get('genres', [])
#                 except Exception:
#                     artist_genres_cache[artist_id] = []

#         # Optionally write to file (if needed for debugging or logging)
#         # with open("demofile.txt", "w") as f:
#         #     written_ids = set()
#         #     for track in enriched_tracks:
#         #         track_id = track["track"]["id"] if "track" in track else track["id"]

#         #         if track_id not in written_ids:
#         #             written_ids.add(track_id)

#         #             f.write(f'name: {track["track"]["name"] if "track" in track else track["name"]}\n')
#         #             f.write('artists: ')
#         #             artists = track['track']['artists'] if 'track' in track else track['artists']
#         #             genres = set()
#         #             artists_names = []
#         #             for artist in artists:
#         #                 artists_names.append(artist["name"])
#         #                 genres.update(artist_genres_cache.get(artist['id'], []))
#         #             f.write(f'{", ".join(artists_names)}\n')
#         #             f.write(f'genres: {", ".join(genres) if genres else "Unknown"}\n')

#         #             f.write('audio_features:\n')
#         #             audio_features = track['audio_features']
#         #             for key, val in audio_features.items():
#         #                 if key not in ['type', 'uri', 'track_href', 'analysis_url']:
#         #                     f.write(f'  {key}: {val}\n')
#         #             f.write('\n\n')

#         context = {
#             'user_profile': user_profile,
#             'tracks': enriched_tracks
#         }
#         return render(request, 'recommended_songs_site.html', context)
#     else:
#         return redirect('spotify_login')


def recommended_songs_site(request):
    access_token = request.session.get('access_token')

    if access_token:
        # Retrieve data from session
        user_profile = request.session.get('user_profile')
        user_saved_tracks = request.session.get('user_saved_tracks')
        user_top_tracks = request.session.get('user_top_tracks')

        all_tracks = user_saved_tracks['items'] + user_top_tracks['items']
        tracks_ids = list(set([track["track"]["id"] if "track" in track else track["id"] for track in all_tracks]))
        user_tracks_audio_features = spotify_functions.get_songs_audio_features(token=access_token, track_list=tracks_ids)

        audio_features_map = {audio['id']: audio for audio in user_tracks_audio_features if audio is not None}

        enriched_tracks = []
        for track in all_tracks:
            track_id = track["track"]["id"] if "track" in track else track["id"]
            if track_id in audio_features_map:
                combined_data = {
                    **track,
                    'audio_features': audio_features_map[track_id]
                }
                enriched_tracks.append(combined_data)

        # Caching artist genres
        artist_genres_cache = {}
        
        def get_artist_genres(artist_id):
            if artist_id not in artist_genres_cache:
                artist_data = spotify_functions.get_artist_by_id(access_token, artist_id)
                artist_genres_cache[artist_id] = artist_data.get('genres', []) if artist_data else []
            return artist_genres_cache[artist_id]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_artist = {
                executor.submit(get_artist_genres, artist['id']): artist['id']
                for track in enriched_tracks for artist in (track['track']['artists'] if 'track' in track else track['artists'])
            }
            for future in concurrent.futures.as_completed(future_to_artist):
                artist_id = future_to_artist[future]
                try:
                    artist_genres_cache[artist_id] = future.result()
                except Exception:
                    artist_genres_cache[artist_id] = []

        context = {
            'user_profile': user_profile,
            'tracks': enriched_tracks
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
