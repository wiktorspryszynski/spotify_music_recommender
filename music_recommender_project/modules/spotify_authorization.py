import random
import string
from urllib.parse import quote
import os
from requests import post, get
import base64
import json
from dotenv import load_dotenv

load_dotenv()

class SpotifyAuth:
    def __init__(self, client_id: str, client_secret: str, scope: list[str], redirect_uri: str, show_dialog: bool = False) -> None:        
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.show_dialog = show_dialog
        # generate random string (16 char long) as a security measure https://developer.spotify.com/documentation/web-api/tutorials/implicit-flow  
        self.state = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
        self.set_scope(scope)
        self.set_auth_uri()
        
    def set_scope(self, scope: list[str]):
        # https://developer.spotify.com/documentation/web-api/concepts/scopes
        VIABLE_SCOPES = [
            'ugc-image-upload',
            'user-read-playback-state',
            'user-modify-playback-state',
            'user-read-currently-playing',
            'app-remote-control',
            'streaming',
            'playlist-read-private',
            'playlist-read-collaborative',
            'playlist-modify-private',
            'playlist-modify-public',
            'user-follow-modify',
            'user-follow-read',
            'user-read-playback-position',
            'user-top-read',
            'user-read-recently-played',
            'user-library-modify',
            'user-library-read',
            'user-read-email',
            'user-read-private',
            'user-soa-link',
            'user-soa-unlink',
            'soa-manage-entitlements',
            'soa-manage-partner',
            'soa-create-partner'
        ]
        
        viable = []
        
        for s in scope:
            if s in VIABLE_SCOPES:
                viable.append(s)
        
        self.scope = ', '.join(viable)
    
    # equivalent to encodeURIComponent in JS
    def endoce_URI_component(self, component: str) -> str:
        return quote(component, safe="-_.!~*'()")
        
    def set_auth_uri(self) -> str:
        uri = "https://accounts.spotify.com/authorize" 
        uri += f'?client_id={self.endoce_URI_component(self.client_id)}' 
        uri += f'&response_type=code' 
        uri += f'&scope={self.endoce_URI_component(self.scope)}'
        uri += f'&redirect_uri={self.endoce_URI_component(self.redirect_uri)}' 
        uri += f'&state={self.endoce_URI_component(self.state)}'
        # if self.show_dialog:
        #     uri += f'&show_dialog={self.endoce_URI_component(self.show_dialog)}'
        # uri_bytes = uri.encode("utf-8")
        # uri_base64 = str(base64.b64encode(uri_bytes), "utf-8")
        self.uri = uri
        return self.uri

    def get_access_token(self):
        auth_token = self.client_id + ":" + self.client_secret
        auth_bytes = auth_token.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url=url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token
    
    def __str__(self) -> str:
        return f"id: {self.client_id}\nsecret: {self.client_secret}\nscope: {self.scope}\nuri: {self.uri}\ntoken: {self.get_token()}"
    
    def get_authorize_url(self):
        return self.uri
            
# client_id = os.getenv("CLIENT_ID")
# client_secret = os.getenv("CLIENT_SECRET")
# s = SpotifyAuth(client_id, 
#                 client_secret, 
#                 ['user-library-read', 'user-read-private', 'user-read-email', 'user-top-read']
#                 )



# x = 'https://accounts.spotify.com/pl/authorize?client_id=88819e7531f44a748e4112c5542522e8&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fmusic_recommender_app%2Fspotify%2Fcallback%2F&scope=+user-read-email++user-read-private++user-top-read+user-library-read&show_dialog=True'
# y = 'https://accounts.spotify.com/authorize?client_id=88819e7531f44a748e4112c5542522e8&response_type=code&scope=user-library-read%2C%20user-read-private%2C%20user-read-email%2C%20user-top-read&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fmusic_recommender_app%2Fspotify%2Fcallback%2F&state=qpS3AGPlX1QffodX'
# print(s)