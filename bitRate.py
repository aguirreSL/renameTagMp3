import os
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

def get_bitrate(file_path):
    try:
        if file_path.endswith(".mp3"):
            audio = MP3(file_path)
            return audio.info.bitrate // 1000  # Convert to kbps
        elif file_path.endswith(".m4a") or file_path.endswith(".mp4"):
            audio = MP4(file_path)
            bitrate = audio.info.bitrate // 1000  # Convert to kbps
            return bitrate
        else:
            print(f"Unsupported file format: {file_path}")
            return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def read_bitrates(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".mp3", ".m4a", ".mp4")):
                file_path = os.path.join(root, file)
                bitrate = get_bitrate(file_path)
                if bitrate:
                    print(f"File: {file}, Bitrate: {bitrate} kbps")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Read bitrates of audio files.")
    parser.add_argument("--dir", required=True, help="Directory containing audio files")
    args = parser.parse_args()
    
    if os.path.exists(args.dir):
        read_bitrates(args.dir)
    else:
        print(f"The directory {args.dir} does not exist.")