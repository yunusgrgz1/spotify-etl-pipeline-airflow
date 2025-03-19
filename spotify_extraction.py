# spotify_extraction.py

import requests
import logging

CLIENT_ID = "your_id"
CLIENT_SECRET = "your_secret"
TOKEN_URL = "your_token"

def get_access_token():
    """Function to obtain an access token from the Spotify API."""
    try:
        response = requests.post(TOKEN_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        })
        response.raise_for_status()
        token_info = response.json()
        return token_info.get('access_token')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching token: {e}")
        return None

def get_spotify_data(endpoint, params=None):
    """Function to fetch data from the Spotify API."""
    token = get_access_token()
    if not token:
        logging.error("Unable to fetch access token.")
        return {}
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()

def fetch_new_tracks():
    """Fetches newly released tracks from Spotify."""
    url = "https://api.spotify.com/v1/browse/new-releases"
    return get_spotify_data(url)

