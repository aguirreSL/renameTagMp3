# renameTagMp3 (Refactored)

`renameTagMp3` is a modular Python CLI utility designed to help organize, manage, rename, and tag audio files in a local music library. This repository is especially useful for DJs and music collectors looking to maintain a clean and standardized library across various audio formats (MP3, WAV, M4A, MP4).

It features embedding cover art, identifying unknown songs via APIs, syncing filenames with ID3 tags, finding duplicates, and managing metadata.

## Prerequisites & Setup

Ensure you have Python installed on your system. 

1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Some commands additionally require `musicbrainzngs`, `requests`, `pydub`, `Pillow`, and `ffmpeg` installed on your system.*

3. Copy the `.env.example` file to a new file named `.env` and fill in your API keys (if using `fetch-covers` or `identify`):
   ```bash
   cp .env.example .env
   ```

## Usage

This tool now operates via a unified `cli.py` entry point using subcommands.

### Tag & Metadata Management
- `python cli.py update-tags --dir /path/to/music`
  *Reads "Artist - Title" filenames and cleanly updates tags for `.mp3`, `.wav`, `.m4a`, and `.mp4` files. (Strips corrupt metadata first on WAVs).*

### API Integration
- `python cli.py fetch-covers --dir /path/to/music`
  *Searches iTunes and Last.fm for cover art and embeds it into the tags.*
- `python cli.py identify --dir /path/to/music`
  *Uses the AudD API to fingerprint unknown `.mp3` tracks and rename them.*

### File Utilities
- `python cli.py find-duplicates --dir /path/to/music [--out filename.txt]`
  *Recursively hashes files to find exact duplicates.*
- `python cli.py bitrates --dir /path/to/music`
  *Scans and lists bitrates to find low-quality tracks.*
- `python cli.py capitalize --dir /path/to/music`
  *Capitalizes all words for `.m4a` files in a given directory.*
- `python cli.py copies --dir /path/to/music [--out filename.txt]`
  *Looks for macOS or Windows duplication naming schemes (like "copy" or "2.").*
- `python cli.py diff --dir1 /path/A --dir2 /path/B [--out filename.txt]`
  *Compares two directories and lists files unique to each.*

## Development Architecture

All specific handlers are now moved into a structured format:
- `core/`: Shared audio file traversal and metadata manipulation.
- `api/`: Reusable code for iTunes, Last.FM, AudD, and MusicBrainz.
- `commands/`: Subcommands easily hooked into the `cli.py` router.
