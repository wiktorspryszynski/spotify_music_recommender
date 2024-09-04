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
        
        # Set the scope
        self.scope = self.build_viable_scope(scope) if scope else ''
        self.auth_uri = self.build_auth_uri()
        self.access_token = None
    
    def build_auth_uri(self) -> str:
        """Construct the Spotify authorization URL."""
        uri = "https://accounts.spotify.com/authorize"
        uri += f'?client_id={self.encode_URI_component(self.client_id)}'
        uri += f'&response_type=code'
        uri += f'&redirect_uri={self.encode_URI_component(self.redirect_uri)}'
        if self.scope:
            uri += f'&scope={self.encode_URI_component(self.scope)}'
        if self.show_dialog:
            uri += f'&show_dialog={self.show_dialog}'
        return uri

    def build_viable_scope(self, scope: list[str]):
        """https://developer.spotify.com/documentation/web-api/concepts/scopes"""
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
        
        return ' '.join(viable)
    
    def encode_URI_component(self, component: str) -> str:
        """Equivalent to encodeURIComponent in JavaScript."""
        return quote(component, safe="-_.!~*'()")
    
    def get_access_token(self, code: str = None) -> dict:
        """Retrieve the access token from Spotify."""
        auth_token = f"{self.client_id}:{self.client_secret}"
        auth_base64 = base64.b64encode(auth_token.encode("utf-8")).decode("utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }
        if code:
            data["code"] = code
            
        result = post(url=url, headers=headers, data=data)
        try:
            result.raise_for_status()
            self.access_token = result.json()
        except Exception as e:
            print(f"Error fetching access token: {e}")
            self.access_token = None
        
        return self.access_token
    
    def get_authorize_url(self) -> str:
        """Return the authorization URL."""
        return self.auth_uri

