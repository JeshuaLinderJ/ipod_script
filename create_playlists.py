import json
import os

# -----------------------
# Spotify Setup
# -----------------------
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace these with your Spotify app credentials.
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
SPOTIFY_REDIRECT_URI = ''
SPOTIFY_SCOPE = 'playlist-modify-public'

def create_spotify_playlist(songs, playlist_name="My IPod Playlist"):
    """
    Create a Spotify playlist and add tracks based on song metadata.
    The function searches Spotify for each track using the song title and artist.
    """
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE
    ))
    
    user = sp.current_user()
    user_id = user['id']
    print(f"Logged in as: {user['display_name']} ({user_id})")
    
    # Create a new playlist.
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    playlist_id = playlist['id']
    print(f"Created Spotify playlist: {playlist['external_urls']['spotify']}")
    
    track_ids = []
    for song in songs:
        # Construct a search query (you can refine this query as needed).
        query = f"track:{song['title']} artist:{song['artist']}"
        results = sp.search(q=query, type='track', limit=1)
        tracks = results.get('tracks', {}).get('items', [])
        if tracks:
            track_id = tracks[0]['id']
            track_ids.append(track_id)
            print(f"Found on Spotify: {song['title']} by {song['artist']}")
        else:
            print(f"Not found on Spotify: {song['title']} by {song['artist']}")
    
    # Spotify allows adding tracks in batches (max 100 at a time).
    for i in range(0, len(track_ids), 100):
        sp.playlist_add_items(playlist_id, track_ids[i:i+100])
    
    print("Spotify playlist creation complete.")


# -----------------------
# YouTube Setup
# -----------------------
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Path to your YouTube client secrets file.
YOUTUBE_CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_youtube_service():
    """
    Authenticate the user and return an authorized YouTube API client.
    This will open a browser window for OAuth if not already authenticated.
    """
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)
    return youtube

def create_youtube_playlist(songs, playlist_title="My IPod Playlist on YouTube", playlist_description="A playlist created automatically."):
    """
    Create a YouTube playlist and search for videos matching each song.
    Adds the first search result for each song into the playlist.
    """
    youtube = get_youtube_service()
    
    # Create the playlist.
    playlist_request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_title,
                "description": playlist_description
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    )
    playlist_response = playlist_request.execute()
    playlist_id = playlist_response["id"]
    print(f"Created YouTube playlist with ID: {playlist_id}")
    
    # Search for each song and add the video to the playlist.
    for song in songs:
        query = f"{song['artist']} - {song['title']}"
        search_request = youtube.search().list(
            part="snippet",
            maxResults=1,
            q=query,
            type="video"
        )
        search_response = search_request.execute()
        items = search_response.get("items", [])
        if items:
            video_id = items[0]["id"]["videoId"]
            # Add the video to the playlist.
            add_request = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            add_request.execute()
            print(f"Added to YouTube: {song['title']} by {song['artist']}")
        else:
            print(f"No YouTube result for: {song['title']} by {song['artist']}")
    
    print("YouTube playlist creation complete.")


# -----------------------
# Main Execution
# -----------------------

def load_songs(json_file):
    """
    Load the songs from the given JSON file.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        songs = json.load(f)
    return songs

if __name__ == "__main__":
    # Update the filename if necessary.
    json_file = "ipod_song_list.json"
    
    if not os.path.exists(json_file):
        print(f"JSON file not found: {json_file}")
        exit(1)
    
    songs = load_songs(json_file)
    print(f"Loaded {len(songs)} songs from JSON.")
    
    # Create the Spotify playlist.
    print("\n--- Creating Spotify Playlist ---")
    create_spotify_playlist(songs, playlist_name="My IPod Playlist")
    
    # Create the YouTube playlist.
    print("\n--- Creating YouTube Playlist ---")
    create_youtube_playlist(songs, playlist_title="My IPod Playlist on YouTube")
