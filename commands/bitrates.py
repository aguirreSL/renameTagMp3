import os
import argparse
from core.files import walk_audio_files
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

def get_bitrate(file_path):
    try:
        if file_path.endswith(".mp3"):
            audio = MP3(file_path)
            return audio.info.bitrate // 1000
        elif file_path.endswith(".m4a") or file_path.endswith(".mp4"):
            audio = MP4(file_path)
            return audio.info.bitrate // 1000
        else:
            return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def run_bitrates(args):
    if not os.path.isdir(args.dir):
        print(f"Directory not found: {args.dir}")
        return
        
    for file_path in walk_audio_files(args.dir):
        bitrate = get_bitrate(file_path)
        if bitrate:
            print(f"File: {os.path.basename(file_path)}, Bitrate: {bitrate} kbps")

def register_parser(subparsers):
    parser = subparsers.add_parser("bitrates", help="List audio file bitrates.")
    parser.add_argument("--dir", required=True, help="Directory containing audio files")
    parser.set_defaults(func=run_bitrates)
