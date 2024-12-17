import joblib
import pandas as pd
import os
import sys
import django
from django.conf import settings

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_recommender_project.settings')
django.setup()

from music_recommender_app.models import MusicTrack
from modules import spotify_functions

def preprocess_data(df, mlb, scaler):
    genres_encoded = mlb.transform(df['genres'])
    genres_df = pd.DataFrame(genres_encoded, columns=mlb.classes_)
    
    if 'year' not in df.columns:
        df['year'] = pd.to_datetime(df['release_date']).dt.year
        
    features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                'instrumentalness', 'liveness', 'valence', 'tempo', 'key', 'explicit', 'popularity', 'year']

    X = pd.concat([df[features], genres_df], axis=1)
    
    X_scaled = scaler.transform(X)
    return X_scaled


def get_recommended_songs_ids(user_songs):
    """
    Please note that this is showcase only, as Spotify deprecated their audio_features endpoint, so for now it will only
    with pre-saved sample music tracks and their features.
    
    Args:
        user_songs: String "demofile" (To be implemented if Spotify reverts changes: User's songs with their audio features)
    
    Returns:
        ID's of songs recommended based on user_songs (up to 50).
    """
    
    # if Spotify reverts deprecating audio_features endpoint, I will add the functionality of getting "real" recommendations
    if user_songs == "demofile":
        knn = joblib.load(os.path.join(settings.BASE_DIR, 'data', 'knn_model.joblib'))
        scaler = joblib.load(os.path.join(settings.BASE_DIR, 'data', 'scaler.joblib'))
        mlb = joblib.load(os.path.join(settings.BASE_DIR, 'data', 'mlb.joblib'))
        
        user_songs_df = pd.read_csv(os.path.join(settings.BASE_DIR, 'data', 'demofile.txt'), sep=';', encoding='utf-8')
        user_songs_df['genres'] = user_songs_df['genres'].apply(lambda x: eval(x))
        
        X_user_scaled = preprocess_data(user_songs_df, mlb, scaler)

        big_dataset = MusicTrack.objects.all().values()
        big_df = pd.DataFrame(list(big_dataset))
        
        #big_df['genres'] = big_df['genres'].apply(lambda x: eval(x))
        X_big_scaled = preprocess_data(big_df, mlb, scaler)

        knn.fit(X_big_scaled)

        distances, indices = knn.kneighbors(X_user_scaled)

        recommended_indices = indices.flatten()
        recommendations_df = big_df.iloc[recommended_indices]

        recommendations_df = recommendations_df.drop_duplicates(subset='track_id').head(50)
        track_ids = recommendations_df['track_id'].tolist()

        return track_ids
    
