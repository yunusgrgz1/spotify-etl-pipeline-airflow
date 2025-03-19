# spotify_transformation.py

import pandas as pd
from spotify_extraction import fetch_new_tracks  # Import the Extraction module
from airflow.exceptions import AirflowException

def process_data(data):
    """Processes Spotify data and converts it into a DataFrame."""
    if 'albums' not in data or 'items' not in data['albums']:
        raise AirflowException("No albums found.")
    
    albums = data['albums']['items']
    
    # Extract necessary information from each item in albums.
    df = pd.DataFrame([{
        "album_name": album["name"],
        "artist_name": album["artists"][0]["name"],
        "release_date": album["release_date"],
        "album_url": album["external_urls"]["spotify"],  # Add Spotify URL
        "total_tracks": album["total_tracks"],  # Number of tracks in the album
    } for album in albums])
    
    return df

def transform_data(**context):
    """Fetches newly released tracks, processes, and transforms them."""
    data = fetch_new_tracks()  # Extraction process, fetching data from Spotify API
    if not data:
        raise AirflowException("No data fetched from Spotify.")
    
    # Process and convert data into a DataFrame
    df = process_data(data)  # Transformation process

    # Additional processing can be added here: filtering, cleaning, etc.
    
    return df
