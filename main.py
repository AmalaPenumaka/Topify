import os
from dotenv import load_dotenv
import base64
from requests import post, get
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# from flask import Flask, request, url_for, session, redirect

# app = Flask(__name__)

# app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
# app.secret_key = 'assafjf6'

# TOKEN_INFO_CONSTANT = 'token_info'

# # creating routes

# @app.route('/')
# @app.route('/redirect')
# @app.route('/saveDiscoverWeekly')

# def create_spotify_oauth():
#     return SpotifyOAuth(
#         client_id = "249a343f66b548e2a2f26786235f912c",
#         client_secret = "4d5721792ee544679b066d54720e937d",
#         redirect_uri=url_for('redirect'), _external=True
#         scope = 'user-library-read playlist-modify-public playlist-modify-private'
#         )


load_dotenv()

# Unique to this Spotify project - will be used when requesting authorization token
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Gets authorization token by sending request
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # To send any request to the API, you need an API endpoint URL and headers
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64, 
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    # Produces JSON data in a field called content
    result = post(url, headers=headers, data=data)

    # Convert JSON data into a Python dict
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_artist_name():
    artist_name = input("Enter artist: ")
    return artist_name

# Searches for an artist and get artist top tracks
def search_for_artist(token):
    artist_name = get_artist_name()
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    # Construct query for search API endpoint
    # "limit=1" gives the first result when searching for that artist (gives most popular)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists.")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


token = get_token() 
result = search_for_artist(token)
artist_id = result["id"]
# related_artists = spotipy.artist_related_artists(artist_id)
# print(related_artists)
print(result["name"] + "'s top songs are:")
songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")