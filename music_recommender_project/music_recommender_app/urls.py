from django.urls import path
from . import views

urlpatterns = [
    #path('plot/', views.plot_user_music_data, name='plot_user_music_data'),
    path('', views.index, name='index'),
    path('music_recommender_app/', views.index, name="index"),
    path('music_recommender_app/spotify/login/', views.spotify_login, name='spotify_login'),
    path('music_recommender_app/spotify/callback/', views.spotify_callback, name='spotify_callback'),
    path('music_recommender_app/spotify/callback/recommended_songs/', views.recommended_songs_site, name='recommended_songs'),
    #path('music_recommender_app/track_list/', views.track_list, name='track_list'),
]
