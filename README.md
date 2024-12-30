# spotify_music_recommender

## Introduction
Spotify Music Recommender is an app that allows you to log in via your Spotify account, see your top tracks and get a (play)list of recommended songs that best suit your liking.

The recommendation algorithm will use machine learning and a csv file loaded with music.
In the future there might also appear a little section with analysis of your music taste, most listened to artists, genres etc., as I am fond of data analysis.

## IMPORTANT NOTE
    
As of december 2024, Spotify deprecated their audio features endpoint, rendering this app useless.
I am keeping the code responsible for handling audio features in case they revert the changes.

To not make this app a complete waste of time, I will be showcasing it further using my personal set of music tracks I tested the app with.
This means that this app will no longer get any recommendations based on user's music, as the app can't get the much needed audio features of user's top music tracks and
will instead showcase (what it would look like had it all worked out) recommendations based on my saved music data and it's audio features (demofile.txt in the root directory).

## YouTube Link
If you want to see how the project works with saved tracks, you can see it [HERE](https://youtu.be/Jc-vJqKS7Ks).

## To run:
Make sure to have Python installed on your system, then type the following:

```bash
pip install -r requirements.txt
cd music_recommender_project
python manage.py migrate
python manage.py populate_tracks
python manage.py runserver
```

Please note that this is a work-in-progress project and I don't make my client credentials public.
You need to supply your own CLIENT_ID and CLIENT_SECRET, that you can find in your Spotify's API Dashboard supplied after creating your own app.
Click [HERE](https://developer.spotify.com/dashboard) to make your own app using Spotify's API.


## Technologies used

- Python
    - Django
    
- Hopefully in the future
    - Pyspark 
    - TensorFlow
    - Docker 

- Ditched
    - Spotipy

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
You can reach me through my e-mail: spryszynskiwiktor@gmail.com.