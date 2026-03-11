import os

def walk_audio_files(directory, extensions=(".mp3", ".m4a", ".mp4", ".wav")):
    """Yields all audio files in the given directory that match the extensions."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                yield os.path.join(root, file)

def parse_filename(filename):
    """Parse a filename into artist and title, assuming 'Artist - Title.ext' format."""
    name = os.path.splitext(filename)[0]
    parts = name.split(" - ", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return None, name.strip()  # Only return title if no dash is found
