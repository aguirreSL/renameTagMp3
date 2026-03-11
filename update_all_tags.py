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

def update_mp3_tags(file_path, artist, title):
    try:
        # Try to load the existing ID3 tags
        audiofile = ID3(file_path)
    except ID3NoHeaderError:
        # If there's no ID3 tag, create a new one
        audiofile = ID3()
    
    # Check if the existing tags match the new ones
    existing_artist = audiofile.get('TPE1', None)
    existing_title = audiofile.get('TIT2', None)
    
    if (existing_artist and existing_artist.text[0] == artist and
        existing_title and existing_title.text[0] == title):
        return False  # No change needed
    
    # Update the artist and title tags
    audiofile['TPE1'] = TPE1(encoding=3, text=artist)
    audiofile['TIT2'] = TIT2(encoding=3, text=title)
    audiofile.save(file_path)
    return True  # Changes were made

def update_m4a_tags(file_path, artist, title):
    audiofile = MP4(file_path)
    
    # Check if the existing tags match the new ones
    existing_artist = audiofile.get('\xa9ART', None)
    existing_title = audiofile.get('\xa9nam', None)
    
    if (existing_artist and existing_artist[0] == artist and
        existing_title and existing_title[0] == title):
        return False  # No change needed
    
    # Update the artist and title tags
    audiofile['\xa9ART'] = artist
    audiofile['\xa9nam'] = title
    audiofile.save()
    return True  # Changes were made

def update_mp4_tags(file_path, artist, title):
    audiofile = MP4(file_path)
    
    # Check if the existing tags match the new ones
    existing_artist = audiofile.get('\xa9ART', None)
    existing_title = audiofile.get('\xa9nam', None)
    
    if (existing_artist and existing_artist[0] == artist and
        existing_title and existing_title[0] == title):
        return False  # No change needed
    
    # Update the artist and title tags
    audiofile['\xa9ART'] = artist
    audiofile['\xa9nam'] = title
    audiofile.save()
    return True  # Changes were made

def update_wav_tags(file_path, artist, title):
    try:
        # Load the WAV file
        audiofile = WAVE(file_path)
        
        # Ensure the file has ID3 tags
        if audiofile.tags is None:
            audiofile.add_tags()  # Add ID3 tags if they don't exist
        
        # Get the existing tags
        tags = audiofile.tags
        
        # Check if the existing tags match the new ones
        existing_artist = tags.get('TPE1', None)
        existing_title = tags.get('TIT2', None)
        
        if (existing_artist and existing_artist.text[0] == artist and
            existing_title and existing_title.text[0] == title):
            return False  # No change needed
        
        # Update the artist and title tags
        tags['TPE1'] = TPE1(encoding=3, text=artist)
        tags['TIT2'] = TIT2(encoding=3, text=title)
        
        # Save the changes
        audiofile.save()
        return True  # Changes were made
    
    except (ID3NoHeaderError, MutagenError) as e:
        print(f"Warning: {file_path} has no or corrupted ID3 tags. Creating new tags. Error: {e}")
        audiofile = WAVE(file_path)
        audiofile.add_tags()  # Add ID3 tags
        tags = audiofile.tags
        
        # Update the artist and title tags
        tags['TPE1'] = TPE1(encoding=3, text=artist)
        tags['TIT2'] = TIT2(encoding=3, text=title)
        
        # Save the changes
        audiofile.save()
        return True  # Changes were made
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def parse_filename(filename):
    """
    Parse the filename into artist and title, handling cases like "Feat.".
    """
    # Remove the file extension
    name = filename[:-4]
    
    # Split on " - " to separate artist and title
    parts = name.split(" - ", 1)
    if len(parts) != 2:
        raise ValueError("Filename does not match 'Artist - Title' format")
    
    artist, title = parts
    return artist.strip(), title.strip()

def update_audio_tags(directory):
    for filename in os.listdir(directory):
        print('')
        print(filename)
        print('')
        if filename.endswith(".mp3") or filename.endswith(".m4a") or filename.endswith(".mp4") or filename.endswith(".wav"):
            file_path = os.path.join(directory, filename)
            
            try:
                # Strip metadata from WAV files before processing
                if filename.endswith(".wav"):
                    strip_metadata(file_path)
                
                # Parse filename and update tags
                artist, title = parse_filename(filename)
                
                if filename.endswith(".mp3"):
                    changes_made = update_mp3_tags(file_path, artist, title)
                elif filename.endswith(".m4a"):
                    changes_made = update_m4a_tags(file_path, artist, title)
                elif filename.endswith(".mp4"):
                    changes_made = update_mp4_tags(file_path, artist, title)
                elif filename.endswith(".wav"):
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
    parser = argparse.ArgumentParser(description="Update audio tags parsed from filename.")
    parser.add_argument("--dir", required=True, help="Directory containing audio files")
    args = parser.parse_args()
    
    if os.path.isdir(args.dir):
        update_audio_tags(args.dir)
    else:
        print(f"Directory not found: {args.dir}")
