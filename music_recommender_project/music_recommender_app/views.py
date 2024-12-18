# Create your views here.
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
import modules.spotify_functions as spotify_functions
import modules.spotify_authorization as spotify_auth
from django.http import HttpResponse
from asgiref.sync import sync_to_async
import modules.recommendation as recommendation
from django.urls import reverse

async def spotify_callback(request):
    sp_oauth = spotify_auth.SpotifyAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope=['user-library-read', 'user-read-private', 'user-read-email', 'user-top-read', 'playlist-modify-public', 'playlist-modify-private']
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


def recommended_songs_view(request):
    """
    IMPORTANT NOTE:
    
    As of december 2024, Spotify deprecated their audio features endpoint, rendering this app useless.
    I am keeping the code responsible for handling audio features in case they revert the changes.
    
    To not make this app a complete waste of time, I will be showcasing it further using my personal set of music tracks I tested the app with.
    This means that this app will no longer get any recommendations based on user's music, as the app can't get the much needed audio features of user's top music tracks and
    will instead showcase (what it would look like had it all worked out) recommendations based on my saved music data and it's audio features (demofile.txt in the root directory).
    """
    
    access_token = request.session.get('access_token')
    playlist_created = request.session.get('playlist_created', None)
    
    if access_token:
        user_profile = request.session.get('user_profile')
        user_saved_tracks = request.session.get('user_saved_tracks')
        user_top_tracks = request.session.get('user_top_tracks')

        all_tracks = user_saved_tracks['items'] + user_top_tracks['items']
        tracks_ids = list(set([track["track"]["id"] if "track" in track else track["id"] for track in all_tracks]))
        user_tracks_audio_features = spotify_functions.get_songs_audio_features(token=access_token, track_list=tracks_ids)
 
        context = {
            'user_profile': user_profile,
            'playlist_created': playlist_created,
        }
        
        if user_tracks_audio_features:  # this will be None as long as the audio_features endpoint is deprecated in the API
            audio_features_map = {audio['id']: audio for audio in user_tracks_audio_features if audio is not None}

            enriched_tracks = []
            artist_genres_cache = {}
            
            all_artist_ids = set()
            for track in all_tracks:
                artists = track['track']['artists'] if 'track' in track else track['artists']
                for artist in artists:
                    all_artist_ids.add(artist['id'])

            artist_genres_cache.update(spotify_functions.get_artists_genres_batch(access_token, list(all_artist_ids)))

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
                    
                    # spotify_functions.save_music_audio_features_to_file(enriched_tracks, "demofile.txt")
                    
                    
                    context['tracks'] = enriched_tracks
                    
        else: # get recommendations based on saved music data in demofile.txt
            recommended_songs_ids = recommendation.get_recommended_songs_ids('demofile')
            recommended_songs = spotify_functions.get_several_songs_by_ids(access_token, user_profile['country'], recommended_songs_ids)
            request.session['recommended_songs_ids'] = recommended_songs_ids
            
            context['tracks'] = recommended_songs
            
        return render(request, 'recommended_songs.html', context)
    else:
        return redirect('spotify_login')


def create_playlist_view(request):
    if request.method == "POST":
        access_token = request.session.get('access_token')
        
        user_profile = request.session.get('user_profile')
        user_id = user_profile["id"]
        
        if not access_token or not user_id:
            return HttpResponse("User not authenticated", status=401)
        
        recommended_tracks_ids = request.session.get('recommended_songs_ids')
        
        if recommended_tracks_ids:
            playlist_id = spotify_functions.create_playlist(user_id, access_token)
            
            if playlist_id:
                spotify_functions.add_songs_to_playlist(playlist_id, recommended_tracks_ids, access_token)
                request.session['playlist_created'] = True
                del request.session['recommended_songs_ids']
            else:
                request.session['playlist_created'] = False
        else:
            request.session['playlist_created'] = False
    
    return redirect('recommended_songs_view')
        


def spotify_login(request):
    sp_oauth = spotify_auth.SpotifyAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope=['user-library-read', 'user-read-private', 'user-read-email', 'user-top-read', 'playlist-modify-public', 'playlist-modify-private'],
        show_dialog=True
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def index(request):
    template = loader.get_template('index.html')
    
    if 'playlist_created' in request.session.keys():
        del request.session['playlist_created']
    
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
