import os
import subprocess
from mutagen.id3 import ID3, TPE1, TIT2, ID3NoHeaderError
from mutagen.mp4 import MP4
from mutagen.wave import WAVE
from mutagen import MutagenError

def strip_metadata(file_path):
    """
    Strip metadata from a WAV file using ffmpeg.
    """
    temp_file = file_path + ".temp.wav"
    command = [
        "ffmpeg", "-i", file_path, "-map_metadata", "-1", "-c:v", "copy", "-c:a", "copy", temp_file
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.replace(temp_file, file_path)  # Replace the original file with the cleaned version
        print(f"Stripped metadata from {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to strip metadata from {file_path}: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)  # Clean up temporary file

def update_wav_tags(file_path, artist, title):
    try:
        # Try to load the existing ID3 tags
        audiofile = WAVE(file_path)
        tags = audiofile.tags
        if tags is None:
            tags = ID3()
    except (ID3NoHeaderError, MutagenError) as e:
        # If there's no ID3 tag or the file is corrupted, create a new one
        print(f"Warning: {file_path} has no or corrupted ID3 tags. Creating new tags. Error: {e}")
        audiofile = WAVE(file_path)  # Reinitialize the WAVE object
        tags = ID3()  # Create new ID3 tags
    except Exception as e:
        # Handle other exceptions, such as invalid chunk ID
        print(f"Error: {file_path} has an invalid or corrupted ID3 tag. Reinitializing tags. Error: {e}")
        audiofile = WAVE(file_path)  # Reinitialize the WAVE object
        tags = ID3()  # Create new ID3 tags
    
    # Check if the existing tags match the new ones
    existing_artist = tags.get('TPE1', None)
    existing_title = tags.get('TIT2', None)
    
    if (existing_artist and existing_artist.text[0] == artist and
        existing_title and existing_title.text[0] == title):
        return False  # No change needed
    
    # Update the artist and title tags
    tags['TPE1'] = TPE1(encoding=3, text=artist)
    tags['TIT2'] = TIT2(encoding=3, text=title)
    audiofile.tags = tags  # Assign the updated tags to the WAVE object
    audiofile.save()  # Save the changes
    return True  # Changes were made

def update_audio_tags(directory):
    for filename in os.listdir(directory):
        print('')
        print(filename)
        print('')
        if filename.endswith(".wav"):
            file_path = os.path.join(directory, filename)
            
            try:
                # Strip metadata before processing
                strip_metadata(file_path)
                
                # Parse filename and update tags
                artist, title = parse_filename(filename)
                changes_made = update_wav_tags(file_path, artist, title)
                
                if changes_made:
                    print(f"Updated: {filename} -> Artist: {artist}, Title: {title}")
                else:
                    print(f"No changes needed: {filename} -> Artist: {artist}, Title: {title}")
            except ValueError as e:
                print(f"Skipping: {filename} ({str(e)})")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test and strip/update WAV tags.")
    parser.add_argument("--dir", required=True, help="Directory containing WAV files")
    args = parser.parse_args()
    
    if os.path.isdir(args.dir):
        update_audio_tags(args.dir)
    else:
        print(f"Directory not found: {args.dir}")