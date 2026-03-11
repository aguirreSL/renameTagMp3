import os
import requests

def search_itunes(song_name):
    try:
        itunes_url = f"https://itunes.apple.com/search?term={song_name}&media=music&entity=song&limit=1"
        response = requests.get(itunes_url)
        data = response.json()
        if data.get("results"):
            thumbnail_url = data["results"][0]["artworkUrl100"]
            return thumbnail_url.replace("100x100", "600x600")
    except Exception as e:
        print(f"Error searching iTunes: {e}")
    return None

def search_lastfm(song_name, artist=None):
    try:
        api_key = os.getenv("LASTFM_API_KEY")
        if not api_key:
            return None
            
        query = f"{artist} {song_name}" if artist else song_name
        lastfm_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&track={query}&format=json"
        response = requests.get(lastfm_url)
        data = response.json()
        if data.get("track") and data["track"].get("album"):
            thumbnail_url = data["track"]["album"]["image"][-1]["#text"]
            if thumbnail_url:
                return thumbnail_url
    except Exception as e:
        print(f"Error searching Last.fm: {e}")
    return None
