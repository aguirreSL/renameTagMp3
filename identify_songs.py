import os
import argparse
import requests
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

# Replace with your AudD API key
API_KEY = os.getenv('AUDD_API_KEY')

def identify_song(file_path):
    if not API_KEY:
        print("AUDD_API_KEY is not set in .env")
        return None
        
    """Send an audio file to AudD API for recognition."""
    url = 'https://api.audd.io/'
    data = {
        'api_token': API_KEY,
        'return': 'title,artist',  # Request song title and artist
    }
    with open(file_path, 'rb') as audio_file:
        files = {'file': audio_file}
        response = requests.post(url, data=data, files=files)
    result = response.json()
    if result.get('status') == 'success' and result.get('result'):
        return result['result']
    return None

def rename_file_with_song_info(file_path, song_info):
    """Rename the file with the song title and artist."""
    title = song_info.get('title', 'Unknown Title')
    artist = song_info.get('artist', 'Unknown Artist')
    new_name = f"{artist} - {title}.mp3"
    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)
    print(f"Renamed: {os.path.basename(file_path)} -> {new_name}")

def process_folder(folder_path):
    """Process all MP3 files in the folder."""
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.mp3'):
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing: {file_name}")
            song_info = identify_song(file_path)
            if song_info:
                rename_file_with_song_info(file_path, song_info)
            else:
                print(f"Could not identify: {file_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Identify songs using AudD API.")
    parser.add_argument("--dir", required=True, help="Directory containing MP3 files to process")
    args = parser.parse_args()
    
    if os.path.isdir(args.dir):
        process_folder(args.dir)
    else:
        print(f"Directory not found: {args.dir}")