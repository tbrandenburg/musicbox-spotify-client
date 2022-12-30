import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-follow-read," \
        "user-library-read," \
        "user-library-modify," \
        "user-modify-playback-state," \
        "user-read-playback-state," \
        "user-read-currently-playing," \
        "app-remote-control," \
        "playlist-read-private," \
        "playlist-read-collaborative," \
        "playlist-modify-public," \
        "playlist-modify-private," \
        "streaming"
        
token_expired = True
sp_oauth = None

print("  Refreshing token...")

while token_expired:
  try:
    sp_oauth=SpotifyOAuth(scope=scope, open_browser=False)
    print(" OAuth URL: " + str(sp_oauth.get_authorize_url()))
    sp_token_info = sp_oauth.get_access_token()
    print(" Access token: " + str(sp_token_info))
    token_expired = sp_oauth.is_token_expired(sp_token_info)
    print(" Access token expired?: " + str(token_expired))
  except Exception as e:
    print(e)
    token_expired = True
    print("  Next try...")

print("  Token refreshed!")

print("  Getting devices...")

device_fail = True

while device_fail:
  try:
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    devices = sp.devices()
    for _, item in enumerate(devices['devices']):
        print("    Found device: " + item['name'])
  except Exception as e:
    print(e)
    device_fail = True
