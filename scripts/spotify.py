import os
import subprocess
import json
import platform
from dotenv import load_dotenv

def get_spotify_token(client_id, client_secret):
    command = [
        "curl", "-X", "POST", "https://accounts.spotify.com/api/token",
        "-H", "Content-Type: application/x-www-form-urlencoded",
        "-d", f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        try:
            response_json = json.loads(result.stdout)
            return response_json.get("access_token")
        except json.JSONDecodeError:
            print("Failed to parse response:", result.stdout)
    else:
        print("Error:", result.stderr)
    return None

def get_spotify_playlist(playlist_id, spotify_token):
    command = [
        "curl", "-X", "GET", f"https://api.spotify.com/v1/playlists/{playlist_id}",
        "-H", f"Authorization: Bearer {spotify_token}"
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        try:
            response_json = json.loads(result.stdout)
            return response_json
        except json.JSONDecodeError:
            print("Failed to parse response:", result.stdout)
    else:
        print("Error:", result.stderr)
    return None

def get_spotify_playlists(username, spotify_token):
    command = [
        "curl", "-X", "GET", f"https://api.spotify.com/v1/users/{username}/playlists",
        "-H", f"Authorization: Bearer {spotify_token}"
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        try:
            response_json = json.loads(result.stdout)
            return response_json
        except json.JSONDecodeError:
            print("Failed to parse response:", result.stdout)
    else:
        print("Error:", result.stderr)
    return None

def get_playlist_tracks(playlist_id, spotify_token):
    command = [
        "curl", "-X", "GET", f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        "-H", f"Authorization: Bearer {spotify_token}"
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        try:
            response_json = json.loads(result.stdout)
            return response_json
        except json.JSONDecodeError:
            print("Failed to parse response:", result.stdout)
    else:
        print("Error:", result.stderr)
    return None

def extract_tracks_from_playlist(playlist_tracks):
    tracks = []
    for track in playlist_tracks.get("items", []):
        track_info = track.get("track")
        if track_info:
            track_name = track_info.get("name")
            track_id = track_info.get("id")
            track_artist = track_info.get("artists")[0].get("name")
            track_isrc = track_info.get("external_ids").get("isrc")
            tracks.append({"id": track_id, "isrc": track_isrc, "name": track_name, "artist": track_artist})
    return tracks

def main():
    system_platform = platform.system() # Linux, Darwin, Windows

    # retrieve secrets locally, but for actions we'll do auto from onepassword    
    if not load_dotenv(".env"):
        print("Failed to load .env file")
        return

    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    spotify_token = get_spotify_token(client_id, client_secret)

    music_library = []

    json_playlists = get_spotify_playlists(username="ianuriegas", spotify_token=spotify_token)

    for playlist in json_playlists.get("items", []):
        if playlist:
            name, playlist_id, tracks = playlist.get("name"), playlist.get("id"), []
            playlist_tracks = get_playlist_tracks(playlist_id, spotify_token)
            if playlist_tracks:
                tracks = extract_tracks_from_playlist(playlist_tracks=playlist_tracks)
            music_library.append({"id": playlist_id, "name": name, "tracks": tracks})

    print(json.dumps(music_library, indent=4, ensure_ascii=False))
    
if __name__ == "__main__":
    main()

