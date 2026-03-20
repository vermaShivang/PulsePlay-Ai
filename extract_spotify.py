# # # # # import os
# # # # # import spotipy
# # # # # import pandas as pd
# # # # # # from spotipy.oauth2 import SpotifyClientCredentials
# # # # # # import pandas as pd
# # # # # # from dotenv import load_dotenv

# # # # # # load_dotenv()

# # # # # # client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
# # # # # #     client_id=os.getenv("SPOTIFY_CLIENT_ID"),
# # # # # #     client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
# # # # # # ))

# # # # # from spotipy.oauth2 import SpotifyClientCredentials
# # # # # import spotipy, os
# # # # # from dotenv import load_dotenv
# # # # # load_dotenv()

# # # # # client_credentials_manager = SpotifyClientCredentials(
# # # # #     client_id=os.getenv("SPOTIFY_CLIENT_ID"),
# # # # #     client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
# # # # # )
# # # # # sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# # # # # # def fetch_song_data(artist_name, limit=10):
# # # # # #     results = client.search(q=artist_name, type='track', limit=limit)
# # # # # #     songs = []
# # # # # #     for item in results['tracks']['items']:
# # # # # #         songs.append({
# # # # # #             'title': item['name'],
# # # # # #             'artist': item['artists'][0]['name'],
# # # # # #             'spotify_id': item['id'],
# # # # # #             'audio_feature': client.audio_features(item['id'])[0]
# # # # # #         })
# # # # # #     return pd.DataFrame(songs)
# # # # # def fetch_song_data(artist_name, limit=10):
# # # # #     results = sp.search(q=artist_name, type='track', limit=limit)
# # # # #     songs = []
# # # # #     for item in results['tracks']['items']:
# # # # #         try:
# # # # #             features = sp.audio_features([item['id']])
# # # # #             songs.append({
# # # # #                 'title': item['name'],
# # # # #                 'artist': item['artists'][0]['name'],
# # # # #                 'spotify_id': item['id'],
# # # # #                 'audio_feature': features[0] if features and features[0] else {}
# # # # #             })
# # # # #         except Exception as e:
# # # # #             print(f"⚠️ Skipping {item['name']}: {e}")
# # # # #     return pd.DataFrame(songs)


# # # # import os
# # # # import spotipy
# # # # import pandas as pd
# # # # import time
# # # # from spotipy.oauth2 import SpotifyClientCredentials
# # # # from dotenv import load_dotenv

# # # # load_dotenv()

# # # # # Authenticate
# # # # sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
# # # #     client_id=os.getenv("SPOTIFY_CLIENT_ID"),
# # # #     client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
# # # # ))

# # # # def fetch_song_data(artist_name, limit=10):
# # # #     """
# # # #     Fetch songs and audio features from Spotify with error handling.
# # # #     Returns a DataFrame (may contain partial results).
# # # #     """
# # # #     print(f"🔹 Fetching songs for artist: {artist_name}")
# # # #     results = sp.search(q=artist_name, type='track', limit=limit)
# # # #     songs = []

# # # #     for item in results['tracks']['items']:
# # # #         track_id = item['id']
# # # #         title = item['name']
# # # #         artist = item['artists'][0]['name']

# # # #         try:
# # # #             # Try fetching audio features safely
# # # #             features = sp.audio_features([track_id])
# # # #             audio_feature = features[0] if features and features[0] else {}
# # # #         except Exception as e:
# # # #             print(f"⚠️ Skipping {title}: {e}")
# # # #             audio_feature = {}

# # # #         songs.append({
# # # #             'title': title,
# # # #             'artist': artist,
# # # #             'spotify_id': track_id,
# # # #             'audio_feature': audio_feature
# # # #         })

# # # #         # Respect API rate limits
# # # #         time.sleep(0.2)

# # # #     if not songs:
# # # #         print("⚠️ No songs fetched from Spotify.")
# # # #         return pd.DataFrame()

# # # #     df = pd.DataFrame(songs)
# # # #     print(f"✅ Successfully fetched {len(df)} songs.")
# # # #     return df


# # # # new version
# # # import os
# # # import spotipy
# # # import pandas as pd
# # # import time
# # # from spotipy.oauth2 import SpotifyClientCredentials
# # # from dotenv import load_dotenv

# # # load_dotenv()

# # # sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
# # #     client_id=os.getenv("SPOTIFY_CLIENT_ID"),
# # #     client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
# # # ))

# # # def fetch_artist_data(seed_artists):
# # #     """
# # #     Fetch artist metadata (id, genres, followers, popularity) for each artist name.
# # #     """
# # #     artist_records = []
# # #     for name in seed_artists:
# # #         try:
# # #             result = sp.search(q=f"artist:{name}", type="artist", limit=1)
# # #             items = result['artists']['items']
# # #             if not items:
# # #                 print(f"⚠️ No artist found for: {name}")
# # #                 continue
# # #             a = items[0]
# # #             artist_records.append({
# # #                 'name': a['name'],
# # #                 'spotify_artist_id': a['id'],
# # #                 'genres': a.get('genres', []),
# # #                 'followers': a['followers']['total'],
# # #                 'popularity': a['popularity']
# # #             })
# # #         except Exception as e:
# # #             print(f"⚠️ Failed to fetch artist {name}: {e}")
# # #         time.sleep(0.2)
# # #     return pd.DataFrame(artist_records)


# # # # def fetch_songs_for_artist(spotify_artist_id, artist_name, limit=10):
# # # #     """
# # # #     Fetch top tracks for an artist by their Spotify ID.
# # # #     """
# # # #     songs = []
# # # #     try:
# # # #         results = sp.artist_top_tracks(spotify_artist_id)
# # # #         for item in results['tracks'][:limit]:
# # # #             try:
# # # #                 features = sp.audio_features([item['id']])
# # # #                 songs.append({
# # # #                     'title': item['name'],
# # # #                     'artist_name': artist_name,
# # # #                     'spotify_song_id': item['id'],
# # # #                     'audio_feature': features[0] if features and features[0] else {}
# # # #                 })
# # # #             except Exception as e:
# # # #                 print(f"⚠️ Audio features failed for {item['name']}: {e}")
# # # #     except Exception as e:
# # # #         print(f"⚠️ Error fetching songs for {artist_name}: {e}")
# # # #     return pd.DataFrame(songs)



# # # # def fetch_songs_for_artist(spotify_artist_id, artist_name, limit=10):
# # # #     songs = []
# # # #     try:
# # # #         results = sp.artist_top_tracks(spotify_artist_id)
# # # #         for item in results['tracks'][:limit]:
# # # #             # default empty features
# # # #             audio_feature = {}

# # # #             try:
# # # #                 features = sp.audio_features([item['id']])
# # # #                 if features and features[0]:
# # # #                     audio_feature = features[0]
# # # #             except Exception as e:
# # # #                 # specifically handle 403s
# # # #                 if "403" in str(e):
# # # #                     print(f"⚠️ Audio features unavailable (403) for {item['name']}, skipping.")
# # # #                 else:
# # # #                     print(f"⚠️ Audio feature error for {item['name']}: {e}")

# # # #             songs.append({
# # # #                 'title': item['name'],
# # # #                 'artist_name': artist_name,
# # # #                 'spotify_song_id': item['id'],
# # # #                 'audio_feature': audio_feature
# # # #             })
# # # #     except Exception as e:
# # # #         print(f"⚠️ Error fetching songs for {artist_name}: {e}")
# # # #     return pd.DataFrame(songs)


# # # def fetch_songs_for_artist(spotify_artist_id, artist_name, limit=10):
# # #     """
# # #     Fetch top tracks and extract key audio features like danceability, energy, valence, etc.
# # #     """
# # #     songs = []
# # #     try:
# # #         results = sp.artist_top_tracks(spotify_artist_id)
# # #         for item in results['tracks'][:limit]:
# # #             track_id = item['id']
# # #             title = item['name']

# # #             audio_feature = {}
# # #             features = None

# # #             try:
# # #                 features = sp.audio_features([track_id])
# # #                 if features and features[0]:
# # #                     f = features[0]
# # #                     audio_feature = {
# # #                         "danceability": f.get("danceability"),
# # #                         "energy": f.get("energy"),
# # #                         "valence": f.get("valence"),
# # #                         "tempo": f.get("tempo"),
# # #                         "speechiness": f.get("speechiness"),
# # #                         "acousticness": f.get("acousticness"),
# # #                         "instrumentalness": f.get("instrumentalness"),
# # #                         "liveness": f.get("liveness"),
# # #                         "loudness": f.get("loudness"),
# # #                         "mode": f.get("mode"),
# # #                         "key": f.get("key"),
# # #                         "duration_ms": f.get("duration_ms"),
# # #                         "time_signature": f.get("time_signature")
# # #                     }
# # #             except Exception as e:
# # #                 if "403" in str(e):
# # #                     print(f"⚠️ Audio features unavailable (403) for {title}, skipping.")
# # #                 else:
# # #                     print(f"⚠️ Audio feature error for {title}: {e}")

# # #             songs.append({
# # #                 "title": title,
# # #                 "artist_name": artist_name,
# # #                 "spotify_song_id": track_id,
# # #                 **audio_feature  # unpack the dict into individual columns
# # #                 # "audio_feature": audio_feature
# # #             })

# # #     except Exception as e:
# # #         print(f"⚠️ Error fetching songs for {artist_name}: {e}")
# # #     return pd.DataFrame(songs)


# # import os
# # import spotipy
# # import pandas as pd
# # import time
# # from spotipy.oauth2 import SpotifyClientCredentials
# # from dotenv import load_dotenv

# # load_dotenv()

# # sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
# #     client_id=os.getenv("SPOTIFY_CLIENT_ID"),
# #     client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
# # ))

# # def fetch_artist_data(seed_artists):
# #     artist_records = []
# #     for name in seed_artists:
# #         try:
# #             result = sp.search(q=f"artist:{name}", type="artist", limit=1)
# #             items = result['artists']['items']
# #             if not items:
# #                 print(f"⚠️ No artist found for: {name}")
# #                 continue
# #             a = items[0]
# #             artist_records.append({
# #                 'name': a['name'],
# #                 'spotify_artist_id': a['id'],
# #                 'genres': a.get('genres', []),
# #                 'followers': a['followers']['total'],
# #                 'popularity': a['popularity']
# #             })
# #         except Exception as e:
# #             print(f"⚠️ Failed to fetch artist {name}: {e}")
# #         time.sleep(0.2)
# #     return pd.DataFrame(artist_records)

# # # def fetch_songs_for_artist(spotify_artist_id, artist_name, limit=10):
# # #     songs = []
# # #     try:
# # #         results = sp.artist_top_tracks(spotify_artist_id)
# # #         for item in results['tracks'][:limit]:
# # #             track_id = item['id']
# # #             title = item['name']

# # #             f = None
# # #             try:
# # #                 features = sp.audio_features([track_id])
# # #                 f = features[0] if features and features[0] else {}
# # #             except Exception as e:
# # #                 if "403" in str(e):
# # #                     print(f"⚠️ Audio features unavailable (403) for {title}, skipping.")
# # #                     continue

# # #             songs.append({
# # #                 "title": title,
# # #                 "artist_name": artist_name,
# # #                 "spotify_song_id": track_id,
# # #                 "danceability": f.get("danceability"),
# # #                 "energy": f.get("energy"),
# # #                 "valence": f.get("valence"),
# # #                 "tempo": f.get("tempo"),
# # #                 "speechiness": f.get("speechiness"),
# # #                 "acousticness": f.get("acousticness"),
# # #                 "instrumentalness": f.get("instrumentalness"),
# # #                 "liveness": f.get("liveness"),
# # #                 "loudness": f.get("loudness"),
# # #                 "mode": f.get("mode"),
# # #                 "key": f.get("key"),
# # #                 "duration_ms": f.get("duration_ms"),
# # #                 "time_signature": f.get("time_signature")
# # #             })
# # #             time.sleep(0.2)
# # #     except Exception as e:
# # #         print(f"⚠️ Error fetching songs for {artist_name}: {e}")
# # #     return pd.DataFrame(songs)

# # # def fetch_songs_for_artist(spotify_artist_id, artist_name, limit=10):
# # #     songs = []
# # #     try:
# # #         results = sp.artist_top_tracks(spotify_artist_id, country="UK")  # ✅ region fallback
# # #         # for item in results['tracks'][:limit]:
# # #         #     track_id = item['id']
# # #         #     title = item['name']

# # #         #     try:
# # #         #         features = sp.audio_features(tracks=[track_id])
# # #         #         if not features or not features[0]:
# # #         #             continue  # skip missing
# # #         #         f = features[0]
# # #         #     except Exception as e:
# # #         #         if "403" in str(e):
# # #         #             print(f"⚠️ Audio features unavailable for {title} (region locked).")
# # #         #             continue
# # #         #         else:
# # #         #             print(f"⚠️ Unexpected error for {title}: {e}")
# # #         #             continue
# # #         for item in results['tracks'][:limit]:
# # #             track_id = item['id']
# # #             title = item['name']
# # #             try:
# # #                 for attempt in range(3):
# # #                     try:
# # #                         features = sp.audio_features([track_id])
# # #                         if features and features[0]:
# # #                             f = features[0]
# # #                             break
# # #                         time.sleep(random.uniform(1, 3))
# # #                     except Exception as e:
# # #                         if "403" in str(e) and attempt < 2:
# # #                             print(f"⚠️ Retrying {title} due to 403...")
# # #                             time.sleep(3 ** attempt)
# # #                             continue
# # #                         raise e
# # #             except Exception as e:
# # #                 if "403" in str(e):
# # #                     print(f"⚠️ Audio features unavailable for {title} (region locked).")
# # #                     continue
# # #                 else:
# # #                     print(f"⚠️ Unexpected error for {title}: {e}")
# # #                     continue

# # #             songs.append({
# # #                 "title": title,
# # #                 "artist_name": artist_name,
# # #                 "spotify_song_id": track_id,
# # #                 "danceability": f.get("danceability"),
# # #                 "energy": f.get("energy"),
# # #                 "valence": f.get("valence"),
# # #                 "tempo": f.get("tempo"),
# # #                 "speechiness": f.get("speechiness"),
# # #                 "acousticness": f.get("acousticness"),
# # #                 "instrumentalness": f.get("instrumentalness"),
# # #                 "liveness": f.get("liveness"),
# # #                 "loudness": f.get("loudness"),
# # #                 "mode": f.get("mode"),
# # #                 "key": f.get("key"),
# # #                 "duration_ms": f.get("duration_ms"),
# # #                 "time_signature": f.get("time_signature")
# # #             })
# # #             time.sleep(0.2)
# # #     except Exception as e:
# # #         print(f"⚠️ Error fetching songs for {artist_name}: {e}")
# # #     return pd.DataFrame(songs)


# # def fetch_songs_for_artist(spotify_artist_id, artist_name, limit=10):
# #     songs = []
# #     try:
# #         results = sp.artist_top_tracks(spotify_artist_id, country="IN")
# #         for item in results['tracks'][:limit]:
# #             songs.append({
# #                 "title": item["name"],
# #                 "artist_name": artist_name,
# #                 "spotify_song_id": item["id"],
# #                 # Set placeholder audio features to 0
# #                 "danceability": 0,
# #                 "energy": 0,
# #                 "valence": 0,
# #                 "tempo": 0,
# #                 "speechiness": 0,
# #                 "acousticness": 0,
# #                 "instrumentalness": 0,
# #                 "liveness": 0,
# #                 "loudness": 0,
# #                 "mode": 0,
# #                 "key": 0,
# #                 "duration_ms": item.get("duration_ms", 0),
# #                 "time_signature": 0
# #             })
# #             time.sleep(0.2)
# #     except Exception as e:
# #         print(f"⚠️ Error fetching songs for {artist_name}: {e}")
# #     return pd.DataFrame(songs)


import os
import spotipy
import pandas as pd
import time
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

def fetch_artist_data(seed_artists):
    """
    Fetch artist metadata (id, genres, followers, popularity) for each artist name.
    """
    artist_records = []
    for name in seed_artists:
        try:
            result = sp.search(q=f"artist:{name}", type="artist", limit=1)
            items = result['artists']['items']
            if not items:
                print(f"⚠️ No artist found for: {name}")
                continue
            a = items[0]
            artist_records.append({
                'name': a['name'],
                'spotify_artist_id': a['id'],
                'genres': a.get('genres', []),
                'followers': a['followers']['total'],
                'popularity': a['popularity']
            })
        except Exception as e:
            print(f"⚠️ Failed to fetch artist {name}: {e}")
        time.sleep(0.2)
    return pd.DataFrame(artist_records)

# this portion ffetches songs per artist 


# def fetch_songs_for_artist(spotify_artist_id, artist_name, limit=10):
#     """
#     Fetch top tracks for an artist, skipping audio features (set all to 0 for now).
#     """
#     songs = []
#     try:
#         results = sp.artist_top_tracks(spotify_artist_id, country="IN")
#         for item in results['tracks'][:limit]:
#             songs.append({
#                 "title": item["name"],
#                 "artist_name": artist_name,
#                 "spotify_song_id": item["id"],
#                 # Temporarily disabling audio features
#                 "danceability": 0,
#                 "energy": 0,
#                 "valence": 0,
#                 "tempo": 0,
#                 "speechiness": 0,
#                 "acousticness": 0,
#                 "instrumentalness": 0,
#                 "liveness": 0,
#                 "loudness": 0,
#                 "mode": 0,
#                 "key": 0,
#                 "duration_ms": item.get("duration_ms", 0),
#                 "time_signature": 0
#             })
#             time.sleep(0.2)
#     except Exception as e:
#         print(f"⚠️ Error fetching songs for {artist_name}: {e}")
#     return pd.DataFrame(songs)


# CHANGING TO ADD URL+IMAGE 
def fetch_songs_for_artist(spotify_artist_id, artist_name, limit=10):
    songs = []
    try:
        results = sp.artist_top_tracks(spotify_artist_id, country="IN")
        for item in results['tracks'][:limit]:
            album = item.get("album", {}) or {}
            images = album.get("images", []) or []
            image_url = images[0]["url"] if images else None

            songs.append({
                "title": item["name"],
                "artist_name": artist_name,
                "spotify_song_id": item["id"],

                # NEW: album + URLs
                "album_name": album.get("name"),
                "album_image_url": image_url,
                "spotify_track_url": item.get("external_urls", {}).get("spotify"),
                "preview_url": item.get("preview_url"),

                # audio features placeholders (you can fill later)
                "danceability": 0,
                "energy": 0,
                "valence": 0,
                "tempo": 0,
                "speechiness": 0,
                "acousticness": 0,
                "instrumentalness": 0,
                "liveness": 0,
                "loudness": 0,
                "mode": 0,
                "key": 0,
                "duration_ms": item.get("duration_ms", 0),
                "time_signature": 0,
            })
            time.sleep(0.2)
    except Exception as e:
        print(f"⚠️ Error fetching songs for {artist_name}: {e}")
    return pd.DataFrame(songs)



# import os
# import spotipy
# import pandas as pd
# import time, random
# from spotipy.oauth2 import SpotifyClientCredentials
# from dotenv import load_dotenv

# load_dotenv()

# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
#     client_id=os.getenv("SPOTIFY_CLIENT_ID"),
#     client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
# ))

# # ============================================================
# #   ARTIST METADATA FETCH
# # ============================================================
# def fetch_artist_data(seed_artists):
#     artist_records = []
#     for name in seed_artists:
#         try:
#             result = sp.search(q=f"artist:{name}", type="artist", limit=1)
#             items = result['artists']['items']
#             if not items:
#                 print(f"⚠️ No artist found for: {name}")
#                 continue
#             a = items[0]
#             artist_records.append({
#                 'name': a['name'],
#                 'spotify_artist_id': a['id'],
#                 'genres': a.get('genres', []),
#                 'followers': a['followers']['total'],
#                 'popularity': a['popularity']
#             })
#         except Exception as e:
#             print(f"⚠️ Failed to fetch artist {name}: {e}")
#         time.sleep(0.2)
#     return pd.DataFrame(artist_records)


# # ============================================================
# #   SONGS + AUDIO FEATURES FETCH
# # ============================================================
# def fetch_songs_for_artist(spotify_artist_id, artist_name, limit=10):
#     songs = []
#     try:
#         results = sp.artist_top_tracks(spotify_artist_id, country="US")
#         for item in results['tracks'][:limit]:
#             track_id = item['id']
#             title = item['name']
#             f = {}

#             # Try fetching audio features with retry & backoff
#             for attempt in range(3):
#                 try:
#                     features = sp.audio_features([track_id])
#                     if features and features[0]:
#                         f = features[0]
#                         break
#                     else:
#                         time.sleep(1)
#                 except Exception as e:
#                     if "403" in str(e):
#                         print(f"⚠️ Audio features unavailable for {title}. Retrying...")
#                         time.sleep(3 ** attempt)
#                     else:
#                         print(f"⚠️ Unexpected error for {title}: {e}")
#                         break

#             songs.append({
#                 "title": title,
#                 "artist_name": artist_name,
#                 "spotify_song_id": track_id,
#                 "danceability": f.get("danceability", 0),
#                 "energy": f.get("energy", 0),
#                 "valence": f.get("valence", 0),
#                 "tempo": f.get("tempo", 0),
#                 "speechiness": f.get("speechiness", 0),
#                 "acousticness": f.get("acousticness", 0),
#                 "instrumentalness": f.get("instrumentalness", 0),
#                 "liveness": f.get("liveness", 0),
#                 "loudness": f.get("loudness", 0),
#                 "mode": f.get("mode", 0),
#                 "key": f.get("key", 0),
#                 "duration_ms": f.get("duration_ms", 0),
#                 "time_signature": f.get("time_signature", 0)
#             })
#             time.sleep(random.uniform(0.1, 0.3))
#     except Exception as e:
#         print(f"⚠️ Error fetching songs for {artist_name}: {e}")
#     return pd.DataFrame(songs)
