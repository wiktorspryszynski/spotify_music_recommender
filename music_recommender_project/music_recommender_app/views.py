# Create your views here.
from django.http import HttpResponse
from django.template import loader
import modules.spotify_token as spotify_token


def index(request):
    template = loader.get_template('index.html')
    token = spotify_token.get_token()

    trav_id = spotify_token.get_artist_id(token, "Travis scott")
    songs = spotify_token.get_songs_by_artist(token, trav_id)

    context = {
        'songs': songs
    }

    return HttpResponse(template.render(context, request))
