from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class MusicTrack(models.Model):
    track_id = models.CharField(max_length=22, unique=True, primary_key=True)  # Spotify ID
    name = models.CharField(max_length=255)
    artists = models.JSONField()
    year = models.IntegerField()
    explicit = models.BooleanField()
    first_artist = models.CharField(max_length=255)
    genres = models.JSONField()
    genres_limited = models.JSONField() # genres from top300 most popular genres
    valence = models.FloatField()
    acousticness = models.FloatField()
    danceability = models.FloatField()
    duration_ms = models.IntegerField()
    energy = models.FloatField()
    instrumentalness = models.FloatField()
    key = models.IntegerField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    popularity = models.IntegerField()
    speechiness = models.FloatField()
    tempo = models.FloatField()

    def __str__(self):
        artist_list = ", ".join(self.artists) if isinstance(self.artists, list) else self.artists
        return f"{self.name} - {artist_list} (Spotify ID: {self.track_id})"
    
    def clean(self):
        if not isinstance(self.artists, list) or not all(isinstance(artist, str) for artist in self.artists):
            raise ValidationError({"artists": "Artists must be a list of strings."})

        if not isinstance(self.genres, list) or not all(isinstance(genre, str) for genre in self.genres):
            raise ValidationError({"genres": "Genres must be a list of strings."})

        if not isinstance(self.genres_limited, list) or not all(isinstance(genre, str) for genre in self.genres_limited):
            raise ValidationError({"genres_limited": "Genres_limited must be a list of strings."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)