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
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, scope: list[str] = [], show_dialog: bool = False) -> None:        
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.show_dialog = show_dialog
        # generate random string (16 char long) as a security measure https://developer.spotify.com/documentation/web-api/tutorials/implicit-flow  
        # self.state = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
        if scope == []:
            self.scope = []
        else:
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
        
        for s in list(set(scope)):
            if s in VIABLE_SCOPES:
                viable.append(s)
        
        self.scope = ' '.join(viable)
    
    # equivalent to encodeURIComponent in JS
    def endoce_URI_component(self, component: str) -> str:
        return quote(component, safe="-_.!~*'()")
        
    def set_auth_uri(self) -> str:
        uri = "https://accounts.spotify.com/authorize" 
        uri += f'?client_id={self.endoce_URI_component(self.client_id)}'
        uri += f'&response_type=code'
        uri += f'&redirect_uri={self.endoce_URI_component(self.redirect_uri)}'
        if self.scope != []:
            uri += f'&scope={self.endoce_URI_component(self.scope)}'
        #uri += f'&state={self.endoce_URI_component(self.state)}'
        if self.show_dialog:
            uri += f'&show_dialog={self.show_dialog}'
        self.uri = uri
        return self.uri
    
    def set_token(self):
        token = self.get_access_token()
        self.access_token = token
    
    def get_access_token(self, code=None):
        auth_token = self.client_id + ":" + self.client_secret
        auth_bytes = auth_token.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code": code
        }
        result = post(url=url, headers=headers, data=data)
        json_result = json.loads(result.content)
        return json_result
    
    def __str__(self) -> str:
        return f"id: {self.client_id}\nscope: {self.scope}\nuri: {self.uri}\ntoken: {self.get_access_token()}"
    
    def get_authorize_url(self):
        return self.uri
