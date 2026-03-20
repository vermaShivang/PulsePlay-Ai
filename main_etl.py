# # # # # # from extract_spotify import fetch_song_data
# # # # # # from extract_genius import fetch_lyrics
# # # # # # from load_to_db import load_songs

# # # # # # def main():
# # # # # #     print("🔹 Fetching from Spotify...")
# # # # # #     df = fetch_song_data("Arijit Singh", limit=5)
# # # # # #     print("🔹 Fetching lyrics from Genius...")
# # # # # #     df['lyrics'] = df.apply(lambda x: fetch_lyrics(x['title'], x['artist']), axis=1)
# # # # # #     print("🔹 Loading into Database...")
# # # # # #     load_songs(df)
# # # # # #     print("✅ ETL Complete")

# # # # # # if __name__ == "__main__":
# # # # # #     main()


# # # # # from extract_spotify import fetch_song_data
# # # # # from extract_genius import fetch_lyrics
# # # # # from load_to_db import load_songs
# # # # # import pandas as pd

# # # # # def main():
# # # # #     print("🔹 Fetching from Spotify...")
# # # # #     df = fetch_song_data("Arijit Singh", limit=5)

# # # # #     if df.empty:
# # # # #         print("⚠️ No songs fetched from Spotify — skipping ETL.")
# # # # #         return

# # # # #     print("🔹 Fetching lyrics from Genius...")
# # # # #     try:
# # # # #         df['lyrics'] = df.apply(lambda x: fetch_lyrics(x['title'], x['artist']), axis=1)
# # # # #     except Exception as e:
# # # # #         print(f"⚠️ Lyrics fetch failed: {e}")
# # # # #         df['lyrics'] = None

# # # # #     # Drop songs without any data
# # # # #     df.dropna(subset=['title', 'artist'], inplace=True)

# # # # #     print("🔹 Loading into Database...")
# # # # #     try:
# # # # #         load_songs(df)
# # # # #         print("✅ ETL Complete")
# # # # #     except Exception as e:
# # # # #         print(f"❌ Database loading failed: {e}")

# # # # # if __name__ == "__main__":
# # # # #     main()


# # # # from extract_spotify import fetch_song_data
# # # # from extract_genius import fetch_lyrics
# # # # from load_to_db import load_songs
# # # # import pandas as pd
# # # # import random
# # # # import time

# # # # # List of popular artists to auto-cycle through
# # # # ARTISTS = [
# # # #     "Arijit Singh", "Coldplay", "Imagine Dragons", "The Weeknd",
# # # #     "Taylor Swift", "Shreya Ghoshal", "Ed Sheeran", "Pritam",
# # # #     "Adele", "Atif Aslam", "Badshah", "Diljit Dosanjh", "Umair", "Kishore Kumar", "Karan Aujla", "The Local Train", "Lana Del Ray", "Katty Perry", "Drake"
# # # #     "Nusrat Fateh Ali Khan", "Udit Narayan", "Bruno Mars", ""
# # # # ]

# # # # def run_etl_for_artist(artist):
# # # #     print(f"\n🎧 Running ETL for artist: {artist}")
# # # #     df = fetch_song_data(artist, limit=5)
# # # #     if df.empty:
# # # #         print(f"⚠️ No songs found for {artist}, skipping.")
# # # #         return

# # # #     print(f"🔹 Fetching lyrics for {artist}...")
# # # #     try:
# # # #         df['lyrics'] = df.apply(lambda x: fetch_lyrics(x['title'], x['artist']), axis=1)
# # # #     except Exception as e:
# # # #         print(f"⚠️ Lyrics fetch failed for {artist}: {e}")
# # # #         df['lyrics'] = None

# # # #     print(f"💾 Loading {artist}'s songs into database...")
# # # #     try:
# # # #         load_songs(df)
# # # #         print(f"✅ ETL Complete for {artist}")
# # # #     except Exception as e:
# # # #         print(f"❌ Database load failed for {artist}: {e}")

# # # # def main():
# # # #     # Shuffle artists for variety
# # # #     random.shuffle(ARTISTS)

# # # #     for artist in ARTISTS:
# # # #         run_etl_for_artist(artist)
# # # #         time.sleep(5)  # Wait between artists to respect rate limits

# # # # if __name__ == "__main__":
# # # #     main()






# # # from extract_spotify import fetch_artist_data, fetch_songs_for_artist
# # # from extract_genius import fetch_lyrics
# # # from load_to_db import load_artists, load_songs
# # # import pandas as pd
# # # import psycopg2, os
# # # from dotenv import load_dotenv
# # # import time

# # # load_dotenv()

# # # # Seed list for first run (new artists will be pulled from DB afterward)
# # # SEED_ARTISTS = [
# # #     "Arijit Singh", "Shreya Ghoshal", "Coldplay", "Imagine Dragons",
# # #     "The Weeknd", "Taylor Swift", "Atif Aslam", "Adele"
# # # ]

# # # def get_all_artists_from_db():
# # #     conn = psycopg2.connect(
# # #         dbname=os.getenv("POSTGRES_DB"),
# # #         user=os.getenv("POSTGRES_USER"),
# # #         password=os.getenv("POSTGRES_PASSWORD"),
# # #         host=os.getenv("POSTGRES_HOST"),
# # #         port=os.getenv("POSTGRES_PORT")
# # #     )
# # #     cur = conn.cursor()
# # #     cur.execute("SELECT spotify_artist_id, name FROM artist;")
# # #     artists = cur.fetchall()
# # #     cur.close()
# # #     conn.close()
# # #     return artists

# # # def main():
# # #     print("🎼 Starting PulsePlay ETL Run")

# # #     # Step 1: Load/update artist table
# # #     print("🔹 Fetching artist metadata...")
# # #     df_artists = fetch_artist_data(SEED_ARTISTS)
# # #     load_artists(df_artists)

# # #     # Step 2: Get all artists from DB
# # #     artists = get_all_artists_from_db()
# # #     print(f"🔸 Found {len(artists)} artists in DB to process.")

# # #     # Step 3: Fetch songs for each artist
# # #     for spotify_id, name in artists:
# # #         df_songs = fetch_songs_for_artist(spotify_id, name, limit=5)

# # #         if not df_songs.empty:
# # #             df_songs['lyrics'] = df_songs.apply(
# # #                 lambda x: fetch_lyrics(x['title'], name), axis=1
# # #             )
# # #             load_songs(df_songs, name)

# # #         time.sleep(5)  # rate-limit delay between artists

# # #     print("✅ ETL cycle complete. Database up-to-date.")

# # # def discover_new_artists(existing_ids):
# # #     print("🔍 Checking for new related artists...")
# # #     new_artists = []
# # #     for artist_id in existing_ids[:10]:  # limit to avoid rate limit
# # #         try:
# # #             related = sp.artist_related_artists(artist_id)
# # #             for a in related["artists"]:
# # #                 if a["id"] not in existing_ids:
# # #                     new_artists.append(a["name"])
# # #         except Exception:
# # #             continue
# # #     return list(set(new_artists))


# # # if __name__ == "__main__":
# # #     existing = get_all_artists_from_db()
# # #     existing_ids = [a[0] for a in existing]
# # #     new_artist_names = discover_new_artists(existing_ids)
# # #     if new_artist_names:
# # #         df_new = fetch_artist_data(new_artist_names)
# # #         load_artists(df_new)

# # #     main()




# # from extract_spotify import fetch_artist_data, fetch_songs_for_artist
# # from extract_genius import fetch_lyrics
# # from load_to_db import load_artists, load_songs
# # import psycopg2, os, time
# # from dotenv import load_dotenv
# # import pandas as pd
# # import spotipy
# # from spotipy.oauth2 import SpotifyClientCredentials
# # import json
# # load_dotenv()

# # sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
# #     client_id=os.getenv("SPOTIFY_CLIENT_ID"),
# #     client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
# # ))

# # SEED_ARTISTS = [
# #     "Arijit Singh", "Shreya Ghoshal", "Coldplay", "Imagine Dragons",
# #     "The Weeknd", "Taylor Swift", "Atif Aslam", "Adele"
# # ]

# # def get_all_artists_from_db():
# #     conn = psycopg2.connect(
# #         dbname=os.getenv("POSTGRES_DB"),
# #         user=os.getenv("POSTGRES_USER"),
# #         password=os.getenv("POSTGRES_PASSWORD"),
# #         host=os.getenv("POSTGRES_HOST"),
# #         port=os.getenv("POSTGRES_PORT")
# #     )
# #     cur = conn.cursor()
# #     cur.execute("SELECT spotify_artist_id, name FROM artist;")
# #     artists = cur.fetchall()
# #     cur.close()
# #     conn.close()
# #     return artists

# # # def discover_new_artists(existing_ids):
# # #     print("🔍 Checking for related new artists...")
# # #     new_artists = []
# # #     for artist_id in existing_ids[:5]:
# # #         try:
# # #             related = sp.artist_related_artists(artist_id)
# # #             for a in related["artists"]:
# # #                 if a["id"] not in existing_ids:
# # #                     new_artists.append(a["name"])
# # #         except Exception:
# # #             continue
# # #     return list(set(new_artists))

# # def discover_new_artists(existing_ids):
# #     print("🔍 Checking for related new artists...")
# #     new_artists = []
# #     for artist_id in existing_ids[:5]:
# #         try:
# #             related = sp.artist_related_artists(artist_id)
# #             for a in related.get("artists", []):
# #                 if a["id"] not in existing_ids:
# #                     new_artists.append(a["name"])
# #         except Exception as e:
# #             if "404" not in str(e):
# #                 print(f"⚠️ Related artist fetch failed for {artist_id}: {e}")
# #     return list(set(new_artists))


# # def main():
# #     print("🎼 Starting PulsePlay ETL Run")

# #     # Step 1: Update or insert seed artists
# #     print("🔹 Fetching seed artists...")
# #     df_artists = fetch_artist_data(SEED_ARTISTS)
# #     load_artists(df_artists)

# #     # Step 2: Fetch new related artists incrementally
# #     existing = get_all_artists_from_db()
# #     existing_ids = [a[0] for a in existing]
# #     new_artist_names = discover_new_artists(existing_ids)
# #     if new_artist_names:
# #         df_new = fetch_artist_data(new_artist_names)
# #         load_artists(df_new)

# #     # Step 3: Fetch all artists from DB
# #     artists = get_all_artists_from_db()
# #     print(f"🔸 Found {len(artists)} artists in DB to process.")

# #     # Step 4: Fetch songs incrementally
# #     for spotify_id, name in artists:
# #         df_songs = fetch_songs_for_artist(spotify_id, name, limit=5)
# #         if df_songs.empty:
# #             continue
# #         df_songs["lyrics"] = df_songs.apply(
# #             lambda x: fetch_lyrics(x["title"], name), axis=1
# #         )
# #         load_songs(df_songs, name)
# #         time.sleep(5)

# #     print("✅ ETL cycle complete. Database up-to-date.")

# # if __name__ == "__main__":
# #     main()


# from extract_spotify import fetch_artist_data, fetch_songs_for_artist
# from extract_genius import fetch_lyrics
# from load_to_db import load_artists, load_songs
# import psycopg2, os, time
# from dotenv import load_dotenv
# import pandas as pd
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# load_dotenv()

# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
#     client_id=os.getenv("SPOTIFY_CLIENT_ID"),
#     client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
# ))

# SEED_ARTISTS = [
#     "Arijit Singh", "Shreya Ghoshal", "Coldplay", "Imagine Dragons",
#     "The Weeknd", "Taylor Swift", "Atif Aslam", "Adele"
# ]

# def get_all_artists_from_db():
#     conn = psycopg2.connect(
#         dbname=os.getenv("POSTGRES_DB"),
#         user=os.getenv("POSTGRES_USER"),
#         password=os.getenv("POSTGRES_PASSWORD"),
#         host=os.getenv("POSTGRES_HOST"),
#         port=os.getenv("POSTGRES_PORT")
#     )
#     cur = conn.cursor()
#     cur.execute("SELECT spotify_artist_id, name FROM artist;")
#     artists = cur.fetchall()
#     cur.close()
#     conn.close()
#     return artists

# # def discover_new_artists(existing_ids):
# #     print("🔍 Checking for related new artists...")
# #     new_artists = []
# #     for artist_id in existing_ids[:5]:
# #         try:
# #             related = sp.artist_related_artists(artist_id)
# #             for a in related.get("artists", []):
# #                 if a["id"] not in existing_ids:
# #                     new_artists.append(a["name"])
# #         except Exception as e:
# #             if "404" not in str(e):
# #                 print(f"⚠️ Related artist fetch failed for {artist_id}: {e}")
# #     return list(set(new_artists))
# def discover_new_artists(existing_ids):
#     """
#     Discover new artists via featured playlists and new releases.
#     Avoid duplicates by checking existing artist IDs.
#     """
#     print("🔍 Discovering new artists from Spotify catalog...")
#     new_artists = set()

#     # --- Featured playlists discovery ---
#     try:
#         regions = ["IN", "US", "GB", "GLOBAL"]
#         for region in regions:
#             try:
#                 featured = sp.featured_playlists(country=region, limit=5)
#                 for playlist in featured["playlists"]["items"]:
#                     playlist_id = playlist["id"]
#                     tracks = sp.playlist_tracks(playlist_id, limit=20)
#                     for item in tracks["items"]:
#                         track = item.get("track")
#                         if track and "artists" in track:
#                             for artist in track["artists"]:
#                                 if artist["id"] not in existing_ids:
#                                     new_artists.add(artist["name"])
#             except Exception as e:
#                 print(f"⚠️ No featured playlists for region '{region}': {e}")
#     except Exception as e:
#         print(f"⚠️ Featured playlist discovery failed: {e}")

#     # --- New releases discovery ---
#     try:
#         releases = sp.new_releases(country="US", limit=50)
#         for album in releases["albums"]["items"]:
#             for artist in album["artists"]:
#                 if artist["id"] not in existing_ids:
#                     new_artists.add(artist["name"])
#     except Exception as e:
#         print(f"⚠️ New releases discovery failed: {e}")

#     print(f"✅ Discovered {len(new_artists)} potential new artists.")
#     return list(new_artists)

# def get_existing_song_ids(artist_name):
#     conn = psycopg2.connect(
#         dbname=os.getenv("POSTGRES_DB"),
#         user=os.getenv("POSTGRES_USER"),
#         password=os.getenv("POSTGRES_PASSWORD"),
#         host=os.getenv("POSTGRES_HOST"),
#         port=os.getenv("POSTGRES_PORT")
#     )
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT s.spotify_song_id
#         FROM songs s
#         JOIN artist a ON s.artist_id = a.artist_id
#         WHERE a.name = %s;
#     """, (artist_name,))
#     existing = [r[0] for r in cur.fetchall()]
#     cur.close()
#     conn.close()
#     return set(existing)

# def main():
#     print("🎼 Starting PulsePlay ETL Run")

#     # Step 1: Fetch and update seed artists
#     print("🔹 Fetching seed artists...")
#     df_artists = fetch_artist_data(SEED_ARTISTS)
#     load_artists(df_artists)

#     # Step 2: Discover related artists (optional incremental enrichment)
#     existing = get_all_artists_from_db()
    
    
#     # existing_ids = [a[0] for a in existing]
#     # new_artist_names = discover_new_artists(existing_ids)
#     # if new_artist_names:
#     #     df_new = fetch_artist_data(new_artist_names)
#     #     load_artists(df_new)
#     existing_ids = [a[0] for a in existing]
#     new_artist_names = discover_new_artists(existing_ids)
#     if new_artist_names:
#         print(f"🎤 Found {len(new_artist_names)} new artists to add...")
#         df_new = fetch_artist_data(new_artist_names)
#         if not df_new.empty:
#             load_artists(df_new)
#     else:
#         print("⚙️ No new artists discovered this cycle.")







#     # Step 3: Fetch songs incrementally
#     artists = get_all_artists_from_db()
#     print(f"🔸 Found {len(artists)} artists in DB to process.")

#     for spotify_id, name in artists:
#         existing_ids = get_existing_song_ids(name)
#         df_songs = fetch_songs_for_artist(spotify_id, name, limit=10)

#         # Delta comparison (skip existing songs)
#         df_songs = df_songs[~df_songs["spotify_song_id"].isin(existing_ids)]

#         if df_songs.empty:
#             print(f"⚙️ No new songs found for {name}. Skipping.")
#             continue

#         df_songs["lyrics"] = df_songs.apply(
#             lambda x: fetch_lyrics(x["title"], name), axis=1
#         )

#         load_songs(df_songs, name)
#         time.sleep(5)

#     print("✅ ETL cycle complete. Database up-to-date.")

# if __name__ == "__main__":
#     main()


from extract_spotify import fetch_artist_data, fetch_songs_for_artist
from extract_genius import fetch_lyrics
from load_to_db import load_artists, load_songs
import psycopg2, os, time
from dotenv import load_dotenv
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

# ============================================================
#   SEED ARTISTS
# ============================================================
SEED_ARTISTS = [
    "Arijit Singh", "Shreya Ghoshal", "Coldplay", "Imagine Dragons",
    "The Weeknd", "Taylor Swift", "Atif Aslam", "Adele"
]

# ============================================================
#   DATABASE HELPERS
# ============================================================
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

def get_all_artists_from_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT spotify_artist_id, name FROM artist;")
    artists = cur.fetchall()
    cur.close()
    conn.close()
    return artists

def get_existing_song_ids(artist_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.spotify_song_id
        FROM songs s
        JOIN artist a ON s.artist_id = a.artist_id
        WHERE a.name = %s;
    """, (artist_name,))
    existing = [r[0] for r in cur.fetchall()]
    cur.close()
    conn.close()
    return set(existing)


# ============================================================
#   ARTIST DISCOVERY (ALL REGIONS)
# ============================================================
def discover_new_artists(existing_ids):
    print("🌍 Discovering new artists globally...")
    new_artists = set()

    regions = [
        "GLOBAL","AE","AR","AT","AU","BE","BG","BH","BO","BR","CA","CH","CL","CO","CR","CY","CZ",
        "DE","DK","DO","DZ","EC","EE","EG","ES","FI","FR","GB","GR","GT","HK","HN","HU",
        "ID","IE","IL","IN","IS","IT","JO","JP","KW","KZ","LB","LI","LT","LU","LV","MA",
        "MC","MT","MX","MY","NI","NL","NO","NZ","OM","PA","PE","PH","PL","PS","PT","PY",
        "QA","RO","SA","SE","SG","SK","SV","TH","TN","TR","TW","UA","US","UY","VN","ZA"
    ]

    # --- Featured playlists ---
    for region in regions:
        try:
            featured = sp.featured_playlists(country=region, limit=2)
            for playlist in featured["playlists"]["items"]:
                playlist_id = playlist["id"]
                tracks = sp.playlist_tracks(playlist_id, limit=10)
                for item in tracks["items"]:
                    track = item.get("track")
                    if track and "artists" in track:
                        for artist in track["artists"]:
                            if artist["id"] not in existing_ids:
                                new_artists.add(artist["name"])
            time.sleep(0.5)
        except Exception:
            continue

    # --- New Releases ---
    try:
        for region in ["US", "IN", "GB", "BR", "DE", "FR", "JP", "UK", "NZ"]:
            releases = sp.new_releases(country=region, limit=20)
            for album in releases["albums"]["items"]:
                for artist in album["artists"]:
                    if artist["id"] not in existing_ids:
                        new_artists.add(artist["name"])
    except Exception as e:
        print(f"⚠️ New release fetch failed: {e}")

    print(f"✅ Discovered {len(new_artists)} potential new artists.")
    return list(new_artists)


# ============================================================
#   MAIN ETL PIPELINE
# ============================================================
def main():
    print("🎼 Starting PulsePlay ETL Run")

    # Step 1: Update seed artists
    print("🔹 Fetching seed artists...")
    df_artists = fetch_artist_data(SEED_ARTISTS)
    load_artists(df_artists)

    # Step 2: Discover new global artists
    existing = get_all_artists_from_db()
    existing_ids = [a[0] for a in existing]
    new_artist_names = discover_new_artists(existing_ids)
    if new_artist_names:
        print(f"🎤 Found {len(new_artist_names)} new artists to add...")
        df_new = fetch_artist_data(new_artist_names)
        if not df_new.empty:
            load_artists(df_new)
    else:
        print("⚙️ No new artists discovered this cycle.")

    # Step 3: Process songs incrementally
    artists = get_all_artists_from_db()
    print(f"🔸 Found {len(artists)} artists in DB to process.")

    for spotify_id, name in artists:
        existing_ids = get_existing_song_ids(name)
        df_songs = fetch_songs_for_artist(spotify_id, name, limit=10)

        df_songs = df_songs[~df_songs["spotify_song_id"].isin(existing_ids)]
        if df_songs.empty:
            print(f"⚙️ No new songs found for {name}. Skipping.")
            continue

        df_songs["lyrics"] = df_songs.apply(
            lambda x: fetch_lyrics(x["title"], name), axis=1
        )
        load_songs(df_songs, name)
        time.sleep(3)

    print("✅ ETL cycle complete. Database up-to-date.")

if __name__ == "__main__":
    main()
