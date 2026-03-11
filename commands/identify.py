import os
import argparse
from api.audd import identify_song

def rename_file_with_song_info(file_path, song_info):
    title = song_info.get('title', 'Unknown Title')
    artist = song_info.get('artist', 'Unknown Artist')
    new_name = f"{artist} - {title}.mp3"
    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)
    print(f"Renamed: {os.path.basename(file_path)} -> {new_name}")

def run_identify(args):
    """Identify songs via AudD and rename them."""
    if not os.path.isdir(args.dir):
        print(f"Directory not found: {args.dir}")
        return
        
    for file_name in os.listdir(args.dir):
        if file_name.endswith('.mp3'):
            file_path = os.path.join(args.dir, file_name)
            print(f"Processing: {file_name}")
            song_info = identify_song(file_path)
            if song_info:
                rename_file_with_song_info(file_path, song_info)
            else:
                print(f"Could not identify: {file_name}")

def register_parser(subparsers):
    parser = subparsers.add_parser("identify", help="Identify MP3 files using AudD fingerprinting and rename them.")
    parser.add_argument("--dir", required=True, help="Directory containing MP3 files")
    parser.set_defaults(func=run_identify)
