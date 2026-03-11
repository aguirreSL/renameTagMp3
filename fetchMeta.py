import os
import re
import argparse
from dotenv import load_dotenv
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError
import musicbrainzngs

load_dotenv()

email = os.getenv('MUSICBRAINZ_EMAIL', 'your_email@example.com')

# Set up the MusicBrainz API
musicbrainzngs.set_useragent("mp3_tag_checker", "1.0", email)

def clean_filename(filename):
    # Replace underscores with spaces and remove the file extension
    cleaned = filename.replace("_", " ").replace(".mp3", "")
    return cleaned

def fetch_metadata_from_musicbrainz(title, artist=None):
    try:
        # Search for the song in MusicBrainz by title (and artist if provided)
        if artist:
            result = musicbrainzngs.search_recordings(artist=artist, recording=title, limit=1)
        else:
            result = musicbrainzngs.search_recordings(recording=title, limit=1)

        if result['recording-list']:
            recording = result['recording-list'][0]
            artist_name = recording['artist-credit'][0]['artist']['name']
            song_title = recording['title']
            print(f"Found: {artist_name} - {song_title}")
            return artist_name, song_title
        else:
            print(f"No match found for {artist} - {title}")
            return None, None
    except Exception as e:
        print(f"Error while searching MusicBrainz: {e}")
        return None, None

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            file_path = os.path.join(folder_path, filename)
            try:
                audio = EasyID3(file_path)
                title = audio.get('title', [None])[0]
                artist = audio.get('artist', [None])[0]
    
                # Clean the filename by replacing underscores with spaces
                cleaned_filename = clean_filename(filename)
                
                # Check if title or artist are missing or incorrectly set
                if not title or artist == "Track07" or not artist:
                    print(f"File '{filename}' has missing or incorrect metadata. Trying to fetch...")
    
                    # Extract artist and title from the filename
                    match = re.match(r"(.+) - (.+)", cleaned_filename)
                    if match:
                        artist_guess, title_guess = match.groups()
                    else:
                        artist_guess = None
                        title_guess = cleaned_filename
    
                    # Try to fetch correct metadata from MusicBrainz
                    artist_correct, title_correct = fetch_metadata_from_musicbrainz(title_guess, artist_guess)
    
                    # If no match was found on MusicBrainz, use the artist/title from the cleaned filename
                    if not artist_correct:
                        artist_correct = artist_guess
                    if not title_correct:
                        title_correct = title_guess
    
                    # Update the MP3 file's tags if we have valid data
                    if artist_correct and title_correct:
                        audio['artist'] = artist_correct
                        audio['title'] = title_correct
                        audio.save()
                        print(f"Updated metadata for '{filename}': {artist_correct} - {title_correct}")
                    else:
                        print(f"Could not fetch metadata for '{filename}'.")
            except ID3NoHeaderError:
                print(f"No ID3 tag found in: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch missing metadata from MusicBrainz.")
    parser.add_argument("--dir", required=True, help="Directory containing MP3 files")
    args = parser.parse_args()
    
    if os.path.isdir(args.dir):
        process_folder(args.dir)
    else:
        print(f"Directory not found: {args.dir}")
