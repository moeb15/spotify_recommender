import requests
import json
import os
import base64
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def get_token():
    url = 'https://accounts.spotify.com/api/token'
    auth_string = CLIENT_ID + ':' + CLIENT_SECRET
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    headers =  {
        'Authorization':'Basic '+auth_base64,
        'Content-type':'application/x-www-form-urlencoded'
    }
    data = {'grant_type':'client_credentials'}
    token_request = requests.post(url=url,data=data,headers=headers)

    if token_request.status_code == 200:
        access_token = token_request.json()['access_token']
        return access_token
    
    return token_request.status_code

def get_auth_header(token):
    return {'Authorization':'Bearer ' + token}

def get_genres(token):
    url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    headers = get_auth_header(token)
    genre_request = requests.get(url,headers=headers)
    return genre_request.json()['genres']

def spotify_search(token,genre,i,limit=50):
    offset = limit*i
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query_str = f'?q=genre:{genre}&type=artist&market=CA&limit={limit}&offset={offset}'
    query_url = url + query_str
    artist_search = requests.get(query_url,headers=headers)

    
    name_genres = {}
    try:
        for k in range(len(artist_search.json()['artists']['items'])):
            name = artist_search.json()['artists']['items'][k]['name']
            genres = artist_search.json()['artists']['items'][k]['genres']
            name_genres[name] = genres
    except KeyError:
        name_genres = {}

    return name_genres
