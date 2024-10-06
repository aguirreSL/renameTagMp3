import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TPE1

# Specify the folder containing the MP3 files
folder_path = "/Users/sergio/Music/Backup/music/tecno"

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".mp3"):
        # Full path to the MP3 file
        file_path = os.path.join(folder_path, filename)
        
        # Extract the file name without the extension
        title_artist = os.path.splitext(filename)[0]
        
        # Split the filename by ' - ' to separate artist and song title
        if " - " in title_artist:
            artist, title = title_artist.split(" - ", 1)
        else:
            # If no separator is found, use the full name as the title and leave artist empty
            artist = ""
            title = title_artist

        # Load the MP3 file
        try:
            # Try to use EasyID3, otherwise create a new tag
            audio = EasyID3(file_path)
        except:
            audio = ID3(file_path)

        # Set the 'title' and 'artist' tags
        audio['title'] = title
        audio['artist'] = artist

        # Save the changes
        audio.save()

        print(f"Updated title to '{title}' and artist to '{artist}' for {filename}")

print("All MP3 files have been updated.")
