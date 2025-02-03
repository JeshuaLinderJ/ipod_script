import os
import json
import sys
from mutagen import File as MutagenFile

# --- Configuration ---

# Path to the Music folder on your external drive.
# Adjust the path if necessary.
IPOD_PATH = ""


# List of file extensions to check. Add or remove as needed.
AUDIO_EXTENSIONS = {'.mp3', '.m4a', '.flac', '.aac', '.ogg'}

# Output files
OUTPUT_TEXT_FILE = "ipod_song_list.txt"
OUTPUT_JSON_FILE = "ipod_song_list.json"


def is_audio_file(filename):
    """Check if the file has one of the specified audio extensions."""
    _, ext = os.path.splitext(filename)
    return ext.lower() in AUDIO_EXTENSIONS


def extract_metadata(file_path):
    """
    Extract basic metadata (artist, album, title) from an audio file using Mutagen.
    Returns a dictionary with the data, or None if metadata extraction fails.
    """
    try:
        audio = MutagenFile(file_path, easy=True)
        if audio is None:
            return None  # File not supported or no metadata available
        # Use default values if keys are missing
        artist = audio.get('artist', ['Unknown Artist'])[0]
        album = audio.get('album', ['Unknown Album'])[0]
        title = audio.get('title', [os.path.basename(file_path)])[0]
        return {
            "path": file_path,
            "artist": artist,
            "album": album,
            "title": title,
        }
    except Exception as e:
        # Print error and skip the file if there is an issue reading metadata.
        print(f"Error processing {file_path}: {e}")
        return None


def scan_ipod(ipod_path):
    """Recursively scan the provided directory for audio files and extract metadata."""
    songs = []
    for root, dirs, files in os.walk(ipod_path):
        for file in files:
            if is_audio_file(file):
                full_path = os.path.join(root, file)
                metadata = extract_metadata(full_path)
                if metadata:
                    songs.append(metadata)
    return songs


def write_text_file(songs, output_file):
    """Write the song metadata into a tab-separated text file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("Title\tArtist\tAlbum\tPath\n")
        for song in songs:
            line = f"{song['title']}\t{song['artist']}\t{song['album']}\t{song['path']}\n"
            f.write(line)


def write_json_file(songs, output_file):
    """Write the song metadata into a JSON file with pretty formatting."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)


def main():
    # Verify that the specified path exists.
    if not os.path.exists(IPOD_PATH):
        print(f"Error: The path {IPOD_PATH} does not exist. Please verify and update the IPOD_PATH variable.")
        sys.exit(1)

    print("Scanning for audio files. This may take a while...")
    songs = scan_ipod(IPOD_PATH)
    print(f"Found {len(songs)} audio files with metadata.")

    print(f"Writing song list to {OUTPUT_TEXT_FILE} ...")
    write_text_file(songs, OUTPUT_TEXT_FILE)
    print("Text file written successfully.")

    print(f"Writing song list to {OUTPUT_JSON_FILE} ...")
    write_json_file(songs, OUTPUT_JSON_FILE)
    print("JSON file written successfully.")


if __name__ == "__main__":
    main()
