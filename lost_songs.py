import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# -------------------------------
# Configuration
# -------------------------------

# Update these with your Spotify app credentials.
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
SPOTIFY_REDIRECT_URI = ''
# You can use a scope that suits your needs; for search only, a minimal scope is fine.
SPOTIFY_SCOPE = 'user-read-private'

# Input and output files
SONGS_JSON_FILE = "ipod_song_list.json"
OUTPUT_MISSING_FILE = "spotify_missing_songs.txt"

# -------------------------------
# Functions
# -------------------------------

def load_songs(json_file):
    """
    Load songs from a JSON file.
    The JSON file should be a list of dictionaries with at least
    'title', 'artist', and 'album' keys.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        songs = json.load(f)
    return songs

def write_missing_songs(file_path, missing_songs):
    """
    Write songs that were not found on Spotify into a text file.
    Each line includes the title, artist, and album.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("Title\tArtist\tAlbum\n")
        for song in missing_songs:
            line = f"{song.get('title', 'Unknown Title')}\t{song.get('artist', 'Unknown Artist')}\t{song.get('album', 'Unknown Album')}\n"
            f.write(line)

def find_missing_songs(songs):
    """
    For each song, use the Spotify API to search for the track.
    Returns a list of songs (from the input list) not found on Spotify.
    """
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE
    ))
    
    missing_songs = []
    for song in songs:
        # Construct a query using the song title and artist.
        # This query format can be refined if needed.
        query = f"track:{song['title']} artist:{song['artist']}"
        try:
            results = sp.search(q=query, type='track', limit=1)
        except Exception as e:
            print(f"Error searching for '{song['title']}' by {song['artist']}: {e}")
            continue
        
        tracks = results.get("tracks", {}).get("items", [])
        if not tracks:
            missing_songs.append(song)
            print(f"NOT FOUND: {song['title']} by {song['artist']}")
        else:
            print(f"Found: {song['title']} by {song['artist']}")
    
    return missing_songs

# -------------------------------
# Main Execution
# -------------------------------

if __name__ == "__main__":
    # Verify the JSON file exists.
    if not os.path.exists(SONGS_JSON_FILE):
        print(f"Error: The JSON file '{SONGS_JSON_FILE}' does not exist.")
        exit(1)
    
    # Load songs from JSON.
    songs = load_songs(SONGS_JSON_FILE)
    print(f"Loaded {len(songs)} songs from {SONGS_JSON_FILE}.")

    # Find songs not recognized on Spotify.
    missing_songs = find_missing_songs(songs)
    print(f"\nTotal songs not found on Spotify: {len(missing_songs)}")
    
    # Write the missing songs to the output file.
    write_missing_songs(OUTPUT_MISSING_FILE, missing_songs)
    print(f"Missing songs have been written to '{OUTPUT_MISSING_FILE}'.")
