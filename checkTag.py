import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError

# Global folder path removed to use argparse

# Function to read metadata and compare with filename
def check_metadata(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            file_path = os.path.join(folder_path, filename)
            
            # Extract artist and title from filename
            try:
                artist, title = filename[:-4].split(' - ')
            except ValueError:
                print(f"Filename '{filename}' does not match expected format.")
                continue

            # Read metadata
            try:
                audio = MP3(file_path, ID3=ID3)
                actual_artist = audio.get('TPE1')  # Artist
                actual_title = audio.get('TIT2')    # Title

                # Check if the artist and title match
                if actual_artist and actual_title:
                    actual_artist = actual_artist[0]
                    actual_title = actual_title[0]

                    if actual_artist != artist or actual_title != title:
                        # Rename the file to match metadata
                        new_filename = f"{actual_artist} - {actual_title}.mp3"
                        new_file_path = os.path.join(folder_path, new_filename)
                        os.rename(file_path, new_file_path)
                        print(f"Renamed '{filename}' to '{new_filename}'")
                else:
                    print(f"No metadata found for '{filename}'")
            except ID3NoHeaderError:
                print(f"No ID3 header found for '{filename}'")
            except Exception as e:
                print(f"Error processing '{filename}': {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Check metadata and compare with filename.")
    parser.add_argument("--dir", required=True, help="Directory containing MP3 files")
    args = parser.parse_args()
    
    if os.path.isdir(args.dir):
        check_metadata(args.dir)
    else:
        print(f"Directory not found: {args.dir}")
