from django.urls import path
from . import views

urlpatterns = [
    #path('plot/', views.plot_user_music_data, name='plot_user_music_data'),
    path('', views.index, name='index'),
    path('music_recommender_app/', views.index, name="index"),
    path('music_recommender_app/demofile/', views.demofile_preview, name='demofile_preview'),
    path('music_recommender_app/spotify/login-info/', views.login_info, name='login_info'),
    path('music_recommender_app/spotify/login/', views.spotify_login, name='spotify_login'),
    path('music_recommender_app/spotify/callback/', views.spotify_callback, name='spotify_callback'),
    path('music_recommender_app/spotify/callback/recommended_songs/', views.recommended_songs_view, name='recommended_songs_view'),
    path('music_recommender_app/spotify/callback/create_playlist/', views.create_playlist_view, name='create_playlist'),
    #path('music_recommender_app/track_list/', views.track_list, name='track_list'),
]
