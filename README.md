# spotify_music_recommender

## Introduction
Spotify Music Recommender is an app that allows you to log in via your Spotify account, see your top tracks and get a (play)list of recommended songs that best suit your liking.

The recommendation algorithm will use machine learning and a csv file loaded with music (WIP).
In the future there might also appear a little section with analysis of your music taste, most listened to artists, genres etc., as I am fond of data analysis.

## To run:
Make sure to have Python installed on your system, then type the following:

```bash
pip install django

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
You can reach me through e-mail (spryszynskiwiktor@gmail.com).