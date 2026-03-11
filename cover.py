import os
import re
import argparse
import requests
from dotenv import load_dotenv
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from PIL import Image
from io import BytesIO

load_dotenv()

# Function to clean up the song name for better search results
def clean_song_name(song_name):
    # Remove file extensions and special characters
    song_name = re.sub(r'[^\w\s-]', '', song_name)  # Remove special characters
    song_name = re.sub(r'\b(remix|edit|mix|version|original)\b', '', song_name, flags=re.IGNORECASE)  # Remove common words
    return song_name.strip()

# Function to extract artist and title from filename (if formatted as "Artist - Title")
def extract_artist_title(filename):
    parts = filename.split(" - ")
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return None, None

# Function to search for a thumbnail using iTunes API
def search_itunes(song_name):
    try:
        itunes_url = f"https://itunes.apple.com/search?term={song_name}&media=music&entity=song&limit=1"
        response = requests.get(itunes_url)
        data = response.json()
        if data.get("results"):
            thumbnail_url = data["results"][0]["artworkUrl100"]
            return thumbnail_url.replace("100x100", "600x600")  # Higher resolution
    except Exception as e:
        print(f"Error searching iTunes: {e}")
    return None

# Function to search for a thumbnail using Last.fm API
def search_lastfm(song_name, artist=None):
    try:
        api_key = os.getenv("LASTFM_API_KEY")
        if not api_key:
            print("LASTFM_API_KEY is not set in .env")
            return None
            
        query = f"{artist} {song_name}" if artist else song_name
        lastfm_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&track={query}&format=json"
        response = requests.get(lastfm_url)
        data = response.json()
        if data.get("track") and data["track"].get("album"):
            thumbnail_url = data["track"]["album"]["image"][-1]["#text"]  # Get the largest image
            if thumbnail_url:
                return thumbnail_url
    except Exception as e:
        print(f"Error searching Last.fm: {e}")
    return None

# Function to download and add the thumbnail to the metadata
def add_thumbnail_to_metadata(file_path, thumbnail_url):
    try:
        response = requests.get(thumbnail_url)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)

        if file_path.endswith('.mp3'):
            audio = MP3(file_path, ID3=ID3)
            audio.tags.add(APIC(
                encoding=3,  # UTF-8
                mime='image/jpeg',  # or 'image/png'
                type=3,  # Cover image
                desc='Cover',
                data=image_data.getvalue()
            ))
            audio.save()
        elif file_path.endswith('.m4a') or file_path.endswith('.mp4'):
            audio = MP4(file_path)
            audio['covr'] = [image_data.getvalue()]
            audio.save()
        print(f"Added thumbnail to {file_path}")
    except Exception as e:
        print(f"Error adding thumbnail to {file_path}: {e}")

# Main function to process the music folder
def process_music_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(('.mp3', '.mp4', '.m4a')):
                file_path = os.path.join(root, file)
                song_name = os.path.splitext(file)[0]
                print(f"Processing: {song_name}")

                # Clean up the song name
                cleaned_name = clean_song_name(song_name)

                # Extract artist and title if possible
                artist, title = extract_artist_title(cleaned_name)
                search_query = f"{artist} {title}" if artist and title else cleaned_name

                # Try iTunes API first
                thumbnail_url = search_itunes(search_query)
                if not thumbnail_url:
                    # Fallback to Last.fm API
                    thumbnail_url = search_lastfm(title, artist)

                if thumbnail_url:
                    add_thumbnail_to_metadata(file_path, thumbnail_url)
                else:
                    print(f"No thumbnail found for {song_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and embed cover art into audio files.")
    parser.add_argument("--dir", required=True, help="Directory containing audio files")
    args = parser.parse_args()
    
    if os.path.isdir(args.dir):
        process_music_folder(args.dir)
    else:
        print(f"Directory not found: {args.dir}")