import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import time
import tekore as tk
from pprint import pprint


def connect_to_spotify():
    load_dotenv()
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
    redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']
    scope = 'user-read-recently-played'

    # conf = (client_id, client_secret, redirect_uri)
    # token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
    #
    # sp = tk.Spotify(token)

    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    #     client_id=client_id,
    #     client_secret=client_secret,
    #     redirect_uri=redirect_uri,
    #     username='pavelkrusek@icloud.com',
    #     scope=scope)
    # )

    # sp = spotipy.Spotify(
    #     client_credentials_manager=SpotifyClientCredentials(
    #         client_id=client_id,
    #         client_secret=client_secret
    #     )
    # )
    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )

    sp = spotipy.Spotify(auth_manager=auth_manager)

    return sp


def main():
    # time.sleep(2.4)
    missing_cantatas = []
    search_results = sp.search(q='Suzuki cantata BWV 4', type='album')
    # search_results = sp.search(q='artist:' + 'Gardiner' + " track:" + 'BWV 4', type='album')
    pprint(search_results)
    if len(search_results['albums']['items']) > 0:
        album_id = search_results['albums']['items'][0]['id']
        # pprint(album_id)
        album_tracks = sp.album_tracks(album_id)
        preview_urls = [track['name'] for track in album_tracks['items']]
        pprint(preview_urls)
        # pprint(album_tracks)
    else:
        pprint('missing')
        missing_cantatas.append('')

    pprint(missing_cantatas)


if __name__ == '__main__':
    sp = connect_to_spotify()
    main()
