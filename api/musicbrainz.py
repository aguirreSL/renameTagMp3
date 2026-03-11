import os
import musicbrainzngs

def initialize_musicbrainz():
    email = os.getenv('MUSICBRAINZ_EMAIL', 'your_email@example.com')
    musicbrainzngs.set_useragent("mp3_tag_checker", "1.0", email)

def fetch_metadata(title, artist=None):
    initialize_musicbrainz()
    try:
        if artist:
            result = musicbrainzngs.search_recordings(artist=artist, recording=title, limit=1)
        else:
            result = musicbrainzngs.search_recordings(recording=title, limit=1)

        if result['recording-list']:
            recording = result['recording-list'][0]
            artist_name = recording['artist-credit'][0]['artist']['name']
            song_title = recording['title']
            return artist_name, song_title
        else:
            return None, None
    except Exception as e:
        print(f"Error while searching MusicBrainz: {e}")
        return None, None
