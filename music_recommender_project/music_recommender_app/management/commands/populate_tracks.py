import pandas as pd
import ast
import os
import sys
import django
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from music_recommender_app.models import MusicTrack

class Command(BaseCommand):
    help = 'Populate the database with track data from a CSV file'

    def _render_progress_bar(self, current, total, bar_width=40):
        if total == 0:
            return "\rProgress [----------------------------------------] 0.00% (0/0)"

        percent = (current / total) * 100
        filled = int((current / total) * bar_width)
        empty = bar_width - filled

        color = "\033[32m"  # green
        # if percent < 34:
        #     color = "\033[31m"  # red
        # elif percent < 67:
        #     color = "\033[33m"  # yellow
        # else:
        #     color = "\033[32m"  # green

        reset = "\033[0m"
        filled_bar = f"{color}{'█' * filled}{reset}"
        empty_bar = ' ' * empty

        return f"\rProgress [{filled_bar}{empty_bar}] {percent:6.2f}% ({current}/{total})"

    def handle(self, *args, **kwargs):
        # Set up Django environment
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(parent_dir)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_recommender_project.settings')
        django.setup()

        # Check if the database is already populated
        if MusicTrack.objects.exists():
            self.stdout.write(self.style.SUCCESS("Database is already populated. Skipping population."))
            return

        # df = pd.read_csv('music_recommender_project/data/music_tracks_dataset.csv')
        df = pd.read_csv('data/music_tracks_dataset.csv')

        df['artists'] = df['artists'].apply(lambda x: ast.literal_eval(x))
        df['genres'] = df['genres'].apply(lambda x: ast.literal_eval(x))
        df['genres_limited'] = df['genres_limited'].apply(lambda x: ast.literal_eval(x))

        total_rows = len(df)

        for row_number, (_, row) in enumerate(df.iterrows(), start=1):
            if row_number == 1 or row_number % 100 == 0 or row_number == total_rows:
                self.stdout.write(
                    self._render_progress_bar(row_number, total_rows),
                    ending=""
                )

            if isinstance(row['artists'], list) and isinstance(row['genres'], list) and isinstance(row['genres_limited'], list):
                track = MusicTrack(
                    valence=row['valence'],
                    year=row['year'],
                    acousticness=row['acousticness'],
                    artists=row['artists'],
                    danceability=row['danceability'],
                    duration_ms=row['duration_ms'],
                    energy=row['energy'],
                    explicit=row['explicit'],
                    track_id=row['id'],
                    instrumentalness=row['instrumentalness'],
                    key=row['key'],
                    liveness=row['liveness'],
                    loudness=row['loudness'],
                    mode=row['mode'],
                    name=row['name'],
                    popularity=row['popularity'],
                    speechiness=row['speechiness'],
                    tempo=row['tempo'],
                    first_artist=row['first_artist'],
                    genres=row['genres'],
                    genres_limited=row['genres_limited']
                )

                try:
                    track.save()
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f"Validation error for track '{row['name']}': {e}"))
            else:
                self.stdout.write(self.style.ERROR(f"Skipping track '{row['id']}': Artists, genres and genres limited must be lists"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
