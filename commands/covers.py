import os
import argparse
from api.artwork import search_itunes, search_lastfm
from mutagen.id3 import ID3, APIC
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from PIL import Image
from io import BytesIO
import requests
import re

def clean_song_name(song_name):
    song_name = re.sub(r'[^\w\s-]', '', song_name)
    song_name = re.sub(r'\b(remix|edit|mix|version|original)\b', '', song_name, flags=re.IGNORECASE)
    return song_name.strip()

def extract_artist_title(filename):
    parts = filename.split(" - ")
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return None, None

def add_thumbnail_to_metadata(file_path, thumbnail_url):
    try:
        response = requests.get(thumbnail_url)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)

        if file_path.endswith('.mp3'):
            audio = MP3(file_path, ID3=ID3)
            audio.tags.add(APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
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

def run_fetch_covers(args):
    """Fetch and embed covers using iTunes and Last.fm."""
    if not os.path.isdir(args.dir):
        print(f"Directory not found: {args.dir}")
        return
        
    for root, dirs, files in os.walk(args.dir):
        for file in files:
            if file.endswith(('.mp3', '.mp4', '.m4a')):
                file_path = os.path.join(root, file)
                song_name = os.path.splitext(file)[0]
                print(f"Processing: {song_name}")

                cleaned_name = clean_song_name(song_name)
                artist, title = extract_artist_title(cleaned_name)
                search_query = f"{artist} {title}" if artist and title else cleaned_name

                thumbnail_url = search_itunes(search_query)
                if not thumbnail_url:
                    thumbnail_url = search_lastfm(title, artist)

                if thumbnail_url:
                    add_thumbnail_to_metadata(file_path, thumbnail_url)
                else:
                    print(f"No thumbnail found for {song_name}")

def register_parser(subparsers):
    parser = subparsers.add_parser("fetch-covers", help="Fetch cover artwork from iTunes/Last.fm and embed it into files.")
    parser.add_argument("--dir", required=True, help="Directory containing audio files")
    parser.set_defaults(func=run_fetch_covers)
