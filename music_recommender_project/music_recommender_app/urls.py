from django.urls import path
from . import views

urlpatterns = [
    path('music_recommender_app/', views.index, name="index"),
]