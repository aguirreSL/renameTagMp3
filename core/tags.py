import os
import subprocess
from mutagen.id3 import ID3, TPE1, TIT2, ID3NoHeaderError
from mutagen.mp4 import MP4
from mutagen.wave import WAVE
from mutagen import MutagenError
from core.files import parse_filename

def strip_metadata_wav(file_path):
    """Strip metadata from a WAV file using ffmpeg."""
    temp_file = file_path + ".temp.wav"
    command = ["ffmpeg", "-i", file_path, "-map_metadata", "-1", "-c:v", "copy", "-c:a", "copy", temp_file]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.replace(temp_file, file_path)
    except subprocess.CalledProcessError as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def update_mp3_tags(file_path, artist, title):
    try:
        audiofile = ID3(file_path)
    except ID3NoHeaderError:
        audiofile = ID3()
    
    existing_artist = audiofile.get('TPE1', None)
    existing_title = audiofile.get('TIT2', None)
    
    if (existing_artist and existing_artist.text[0] == artist and
        existing_title and existing_title.text[0] == title):
        return False
        
    audiofile['TPE1'] = TPE1(encoding=3, text=artist)
    audiofile['TIT2'] = TIT2(encoding=3, text=title)
    audiofile.save(file_path)
    return True

def update_m4a_tags(file_path, artist, title):
    audiofile = MP4(file_path)
    existing_artist = audiofile.get('\xa9ART', None)
    existing_title = audiofile.get('\xa9nam', None)
    
    if (existing_artist and existing_artist[0] == artist and
        existing_title and existing_title[0] == title):
        return False
        
    audiofile['\xa9ART'] = artist
    audiofile['\xa9nam'] = title
    audiofile.save()
    return True

def update_wav_tags(file_path, artist, title):
    try:
        audiofile = WAVE(file_path)
        if audiofile.tags is None:
            audiofile.add_tags()
        
        tags = audiofile.tags
        existing_artist = tags.get('TPE1', None)
        existing_title = tags.get('TIT2', None)
        
        if (existing_artist and existing_artist.text[0] == artist and
            existing_title and existing_title.text[0] == title):
            return False
            
        tags['TPE1'] = TPE1(encoding=3, text=artist)
        tags['TIT2'] = TIT2(encoding=3, text=title)
        audiofile.save()
        return True
    except (ID3NoHeaderError, MutagenError):
        audiofile = WAVE(file_path)
        audiofile.add_tags()
        tags = audiofile.tags
        tags['TPE1'] = TPE1(encoding=3, text=artist)
        tags['TIT2'] = TIT2(encoding=3, text=title)
        audiofile.save()
        return True
    except Exception as e:
        return False

def sync_tags_with_filename(file_path):
    """Read the filename and update the metadata of the file automatically."""
    filename = os.path.basename(file_path)
    artist, title = parse_filename(filename)
    if not artist:
        return False, "Filename not formatted as 'Artist - Title'"
        
    if file_path.endswith(".wav"):
        strip_metadata_wav(file_path)
        return update_wav_tags(file_path, artist, title), f"Artist: {artist}, Title: {title}"
    elif file_path.endswith(".mp3"):
        return update_mp3_tags(file_path, artist, title), f"Artist: {artist}, Title: {title}"
    elif file_path.endswith(".m4a") or file_path.endswith(".mp4"):
        return update_m4a_tags(file_path, artist, title), f"Artist: {artist}, Title: {title}"
    return False, "Unsupported format"
