import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError

# Global folder path removed to use argparse

def check_metadata(file_path):
    try:
        # Try loading the ID3 tags
        audio = EasyID3(file_path)
        title = audio.get('title', [None])[0]
        artist = audio.get('artist', [None])[0]

        # Check if either title or artist is missing
        if not title or not artist:
            print(f"Missing or incorrect tags in: {file_path}")
            return False
        else:
            return True
    except ID3NoHeaderError:
        # The file has no ID3 tag at all
        print(f"No ID3 tag found in: {file_path}")
        return False

def process_folder(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            file_path = os.path.join(directory, filename)
            is_valid = check_metadata(file_path)
    
            if not is_valid:
                print(f"File '{filename}' is missing metadata and needs correction.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Check MP3 files for missing ID3 tags.")
    parser.add_argument("--dir", required=True, help="Directory containing MP3 files")
    args = parser.parse_args()
    
    if os.path.isdir(args.dir):
        process_folder(args.dir)
    else:
        print(f"Directory not found: {args.dir}")
