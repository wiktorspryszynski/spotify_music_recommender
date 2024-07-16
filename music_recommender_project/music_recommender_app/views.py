# Create your views here.
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
import modules.spotify_functions as spotify_functions

from spotipy.oauth2 import SpotifyOAuth
import spotipy

def spotify_login(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        #scope='user-library-read'
        scope='user-library-read, user-read-private, user-read-email, user-top-read'
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def spotify_callback(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        #scope=['user-library-read']
        scope='user-library-read, user-read-private, user-read-email, user-top-read'
    )
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    
    if token_info:
        access_token = token_info['access_token']
        sp = spotipy.Spotify(auth=access_token)
        user_profile = sp.current_user()
        user_top_tracks = sp.current_user_top_tracks(time_range="long_term")
        #user_top_tracks = spotify_functions.get_current_users_top_songs(token=access_token, type="tracks")
        context = {
            'user_profile': user_profile,
            'user_top_tracks': user_top_tracks
            }

        print(f'\n\n{user_top_tracks}')
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
