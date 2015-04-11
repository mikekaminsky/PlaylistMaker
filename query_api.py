import json
import requests

class SpotifyTrack:
    def __init__(self, name, album_name, artist_name, spotify_url):
        self.name = name
        self.album_name = album_name
        self.artist_name = artist_name
        self.spotify_url = spotify_url

def query_api(query):
    url = 'https://api.spotify.com/v1/search?'
    url = url + 'q=track:' + query + '&type=track'
    response = requests.get(url)
    if response.status_code != 200:
        print "Bad status code!" + response.status_code
        return False
    options = response.json()['tracks']['items']
    for option in options:
        track_name = option['name']
        album_name = option['album']['name']
        artist_name = option['artists'][0]['name']
        spotify_url = option['external_urls']['spotify']
        track = SpotifyTrack(track_name, album_name, artist_name, spotify_url)
        assert 'track' in spotify_url
        if track_name.lower() == query:
            return track
            break
        else:
            print "track did not match!" + track_name.lower()
