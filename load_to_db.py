# # # import psycopg2
# # # import json
# # # import pandas as pd
# # # import os
# # # from dotenv import load_dotenv

# # # load_dotenv()

# # # def load_songs(df):
# # #     conn = psycopg2.connect(
# # #         dbname=os.getenv("POSTGRES_DB"),
# # #         user=os.getenv("POSTGRES_USER"),
# # #         password=os.getenv("POSTGRES_PASSWORD"),
# # #         host=os.getenv("POSTGRES_HOST"),
# # #         port=os.getenv("POSTGRES_PORT")
# # #     )
# # #     cur = conn.cursor()
# # #     for _, row in df.iterrows():
# # #         cur.execute("""
# # #         INSERT INTO songs (title, artist, lyrics, audio_feature)
# # #         VALUES (%s, %s, %s, %s)
# # #         ON CONFLICT DO NOTHING;
# # #         """, (row['title'], row['artist'], row.get('lyrics', None), json.dumps(row['audio_feature'])))
# # #     conn.commit()
# # #     cur.close()
# # #     conn.close()


# # import psycopg2
# # import json
# # import pandas as pd
# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # def load_songs(df):
# #     """
# #     Load songs into PostgreSQL database safely.
# #     """
# #     conn = psycopg2.connect(
# #         dbname=os.getenv("POSTGRES_DB"),
# #         user=os.getenv("POSTGRES_USER"),
# #         password=os.getenv("POSTGRES_PASSWORD"),
# #         host=os.getenv("POSTGRES_HOST"),
# #         port=os.getenv("POSTGRES_PORT")
# #     )
# #     cur = conn.cursor()

# #     print(f"📦 Loading {len(df)} records into database...")

# #     for _, row in df.iterrows():
# #         cur.execute("""
# #         INSERT INTO songs (title, artist, lyrics, audio_feature)
# #         VALUES (%s, %s, %s, %s)
# #         ON CONFLICT DO NOTHING;
# #         """, (
# #             row['title'],
# #             row['artist'],
# #             row.get('lyrics', None),
# #             json.dumps(row['audio_feature'])
# #         ))

# #     conn.commit()
# #     cur.close()
# #     conn.close()
# #     print("✅ Data successfully loaded into database.")


# import psycopg2
# import json
# import pandas as pd
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def get_connection():
#     return psycopg2.connect(
#         dbname=os.getenv("POSTGRES_DB"),
#         user=os.getenv("POSTGRES_USER"),
#         password=os.getenv("POSTGRES_PASSWORD"),
#         host=os.getenv("POSTGRES_HOST"),
#         port=os.getenv("POSTGRES_PORT")
#     )

# def load_artists(df):
#     """
#     Load artist metadata into database.
#     """
#     if df.empty:
#         print("⚠️ No artist data to load.")
#         return
#     conn = get_connection()
#     cur = conn.cursor()
#     print(f"📦 Loading {len(df)} artists...")
#     for _, row in df.iterrows():
#         cur.execute("""
#             INSERT INTO artist (spotify_artist_id, name, genres, followers, popularity)
#             VALUES (%s, %s, %s, %s, %s)
#             ON CONFLICT (spotify_artist_id) DO UPDATE
#             SET name = EXCLUDED.name,
#                 genres = EXCLUDED.genres,
#                 followers = EXCLUDED.followers,
#                 popularity = EXCLUDED.popularity,
#                 last_updated = NOW();
#         """, (
#             row['spotify_artist_id'], row['name'], json.dumps(row['genres']),
#             row['followers'], row['popularity']
#         ))
#     conn.commit()
#     cur.close()
#     conn.close()
#     print("✅ Artists loaded successfully.")

# # def load_songs(df, artist_name):
# #     """
# #     Load songs into database, linking them with artist_id.
# #     """
# #     if df.empty:
# #         print(f"⚠️ No songs to load for {artist_name}.")
# #         return
# #     conn = get_connection()
# #     cur = conn.cursor()
# #     print(f"📀 Loading {len(df)} songs for {artist_name}...")
# #     cur.execute("SELECT artist_id FROM artist WHERE name = %s;", (artist_name,))
# #     artist_row = cur.fetchone()
# #     if not artist_row:
# #         print(f"⚠️ Artist {artist_name} not found in DB — skipping song load.")
# #         conn.close()
# #         return
# #     artist_id = artist_row[0]

# #     for _, row in df.iterrows():
# #         cur.execute("""
# #             INSERT INTO songs (title, artist_id, spotify_song_id, audio_feature)
# #             VALUES (%s, %s, %s, %s)
# #             ON CONFLICT (spotify_song_id) DO NOTHING;
# #         """, (
# #             row['title'], artist_id, row['spotify_song_id'],
# #             json.dumps(row['audio_feature'])
# #         ))
# #     conn.commit()
# #     cur.close()
# #     conn.close()
# #     print(f"✅ Songs loaded for {artist_name}.")


# def load_songs(df, artist_name):
#     if df.empty:
#         print(f"⚠️ No songs to load for {artist_name}.")
#         return

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT artist_id FROM artist WHERE name = %s;", (artist_name,))
#     artist_row = cur.fetchone()

#     if not artist_row:
#         print(f"⚠️ Artist {artist_name} not found in DB.")
#         conn.close()
#         return

#     artist_id = artist_row[0]

#     for _, row in df.iterrows():
#         af = row.get("audio_feature", {}) or {}

#         cur.execute("""
#             INSERT INTO songs (
#                 title, artist_id, spotify_song_id, lyrics,
#                 danceability, energy, valence, tempo, speechiness,
#                 acousticness, instrumentalness, liveness, loudness,
#                 mode, key, duration_ms, time_signature, last_updated
#             )
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
#             ON CONFLICT (spotify_song_id) DO UPDATE
#             SET lyrics = EXCLUDED.lyrics,
#                 danceability = EXCLUDED.danceability,
#                 energy = EXCLUDED.energy,
#                 valence = EXCLUDED.valence,
#                 tempo = EXCLUDED.tempo,
#                 speechiness = EXCLUDED.speechiness,
#                 acousticness = EXCLUDED.acousticness,
#                 instrumentalness = EXCLUDED.instrumentalness,
#                 liveness = EXCLUDED.liveness,
#                 loudness = EXCLUDED.loudness,
#                 mode = EXCLUDED.mode,
#                 key = EXCLUDED.key,
#                 duration_ms = EXCLUDED.duration_ms,
#                 time_signature = EXCLUDED.time_signature,
#                 last_updated = NOW();
#         """, (
#             row["title"], artist_id, row["spotify_song_id"], row.get("lyrics"),
#             af.get("danceability"), af.get("energy"), af.get("valence"),
#             af.get("tempo"), af.get("speechiness"), af.get("acousticness"),
#             af.get("instrumentalness"), af.get("liveness"), af.get("loudness"),
#             af.get("mode"), af.get("key"), af.get("duration_ms"), af.get("time_signature")
#         ))

#     conn.commit()
#     cur.close()
#     conn.close()
#     print(f"✅ Songs updated for {artist_name}.")


import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv
import json

load_dotenv()
from mood_ai import classify_song_mood

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

def load_artists(df):
    if df.empty:
        print("⚠️ No artist data to load.")
        return
    conn = get_connection()
    cur = conn.cursor()
    print(f"📦 Loading {len(df)} artists...")
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO artist (spotify_artist_id, name, genres, followers, popularity)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (spotify_artist_id) DO UPDATE
            SET name = EXCLUDED.name,
                genres = EXCLUDED.genres,
                followers = EXCLUDED.followers,
                popularity = EXCLUDED.popularity,
                last_updated = NOW();
        """, (
            row['spotify_artist_id'],
            row['name'],
            json.dumps(row['genres']),
            row['followers'],
            row['popularity']
        ))
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Artists loaded successfully.")

# def load_songs(df, artist_name):
#     if df.empty:
#         print(f"⚠️ No songs to load for {artist_name}.")
#         return
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT artist_id FROM artist WHERE name = %s;", (artist_name,))
#     artist_row = cur.fetchone()
#     if not artist_row:
#         print(f"⚠️ Artist {artist_name} not found in DB — skipping.")
#         conn.close()
#         return
#     artist_id = artist_row[0]

#     print(f"📀 Loading {len(df)} songs for {artist_name}...")

#     for _, row in df.iterrows():
#         cur.execute("""
#             INSERT INTO songs (
#                 title, artist_id, spotify_song_id, lyrics,
#                 danceability, energy, valence, tempo, speechiness,
#                 acousticness, instrumentalness, liveness, loudness,
#                 mode, key, duration_ms, time_signature, last_updated
#             )
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
#             ON CONFLICT (spotify_song_id) DO UPDATE
#             SET lyrics = EXCLUDED.lyrics,
#                 danceability = EXCLUDED.danceability,
#                 energy = EXCLUDED.energy,
#                 valence = EXCLUDED.valence,
#                 tempo = EXCLUDED.tempo,
#                 speechiness = EXCLUDED.speechiness,
#                 acousticness = EXCLUDED.acousticness,
#                 instrumentalness = EXCLUDED.instrumentalness,
#                 liveness = EXCLUDED.liveness,
#                 loudness = EXCLUDED.loudness,
#                 mode = EXCLUDED.mode,
#                 key = EXCLUDED.key,
#                 duration_ms = EXCLUDED.duration_ms,
#                 time_signature = EXCLUDED.time_signature,
#                 last_updated = NOW();
#         """, (
#             row.get("title"),
#             artist_id,
#             row.get("spotify_song_id"),
#             row.get("lyrics"),
#             row.get("danceability"),
#             row.get("energy"),
#             row.get("valence"),
#             row.get("tempo"),
#             row.get("speechiness"),
#             row.get("acousticness"),
#             row.get("instrumentalness"),
#             row.get("liveness"),
#             row.get("loudness"),
#             row.get("mode"),
#             row.get("key"),
#             row.get("duration_ms"),
#             row.get("time_signature")
#         ))

#     conn.commit()
#     cur.close()
#     conn.close()
#     print(f"✅ Songs updated for {artist_name}.")


# def load_songs(df, artist_name):
#     if df.empty:
#         print(f"⚠️ No songs to load for {artist_name}.")
#         return

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT artist_id FROM artist WHERE name = %s;", (artist_name,))
#     artist_row = cur.fetchone()

#     if not artist_row:
#         print(f"⚠️ Artist {artist_name} not found in DB — skipping.")
#         conn.close()
#         return
#     artist_id = artist_row[0]

#     print(f"📀 Loading {len(df)} songs for {artist_name}...")

#     for _, row in df.iterrows():
#         sql = """
#         INSERT INTO songs (
#             title, artist_id, spotify_song_id, lyrics,
#             danceability, energy, valence, tempo, speechiness,
#             acousticness, instrumentalness, liveness, loudness,
#             mode, key, duration_ms, time_signature, last_updated
#         )
#         VALUES (
#             %s, %s, %s, %s,
#             %s, %s, %s, %s, %s,
#             %s, %s, %s, %s,
#             %s, %s, %s, %s, NOW()
#         )
#         ON CONFLICT (spotify_song_id) DO UPDATE
#         SET lyrics = EXCLUDED.lyrics,
#             danceability = EXCLUDED.danceability,
#             energy = EXCLUDED.energy,
#             valence = EXCLUDED.valence,
#             tempo = EXCLUDED.tempo,
#             speechiness = EXCLUDED.speechiness,
#             acousticness = EXCLUDED.acousticness,
#             instrumentalness = EXCLUDED.instrumentalness,
#             liveness = EXCLUDED.liveness,
#             loudness = EXCLUDED.loudness,
#             mode = EXCLUDED.mode,
#             key = EXCLUDED.key,
#             duration_ms = EXCLUDED.duration_ms,
#             time_signature = EXCLUDED.time_signature,
#             last_updated = NOW();
#         """

#         params = (
#             row.get("title"),
#             artist_id,
#             row.get("spotify_song_id"),
#             row.get("lyrics"),
#             row.get("danceability"),
#             row.get("energy"),
#             row.get("valence"),
#             row.get("tempo"),
#             row.get("speechiness"),
#             row.get("acousticness"),
#             row.get("instrumentalness"),
#             row.get("liveness"),
#             row.get("loudness"),
#             row.get("mode"),
#             row.get("key"),
#             row.get("duration_ms"),
#             row.get("time_signature"),
#         )

#         cur.execute(sql, params)

#     conn.commit()
#     cur.close()
#     conn.close()
#     print(f"✅ Songs updated for {artist_name}.")









# yaha se ai mood ke baaad ke changes hai
def load_songs(df, artist_name):
    if df.empty:
        print(f"⚠️ No songs to load for {artist_name}.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT artist_id FROM artist WHERE name = %s;", (artist_name,))
    artist_row = cur.fetchone()

    if not artist_row:
        print(f"⚠️ Artist {artist_name} not found in DB — skipping.")
        conn.close()
        return
    artist_id = artist_row[0]

    # print(f"📀 Loading {len(df)} songs for {artist_name}...")

    # for _, row in df.iterrows():
    #     sql = """
    #     INSERT INTO songs (
    #         title, artist_id, spotify_song_id, lyrics,
    #         danceability, energy, valence, tempo, speechiness,
    #         acousticness, instrumentalness, liveness, loudness,
    #         mode, key, duration_ms, time_signature, last_updated
    #     )
    #     VALUES (
    #         %s, %s, %s, %s,
    #         %s, %s, %s, %s, %s,
    #         %s, %s, %s, %s,
    #         %s, %s, %s, %s, NOW()
    #     )
    #     ON CONFLICT (spotify_song_id) DO UPDATE
    #     SET lyrics = EXCLUDED.lyrics,
    #         danceability = EXCLUDED.danceability,
    #         energy = EXCLUDED.energy,
    #         valence = EXCLUDED.valence,
    #         tempo = EXCLUDED.tempo,
    #         speechiness = EXCLUDED.speechiness,
    #         acousticness = EXCLUDED.acousticness,
    #         instrumentalness = EXCLUDED.instrumentalness,
    #         liveness = EXCLUDED.liveness,
    #         loudness = EXCLUDED.loudness,
    #         mode = EXCLUDED.mode,
    #         key = EXCLUDED.key,
    #         duration_ms = EXCLUDED.duration_ms,
    #         time_signature = EXCLUDED.time_signature,
    #         last_updated = NOW();
    #     """

    #     params = (
    #         row.get("title"),
    #         artist_id,
    #         row.get("spotify_song_id"),
    #         row.get("lyrics"),
    #         row.get("danceability"),
    #         row.get("energy"),
    #         row.get("valence"),
    #         row.get("tempo"),
    #         row.get("speechiness"),
    #         row.get("acousticness"),
    #         row.get("instrumentalness"),
    #         row.get("liveness"),
    #         row.get("loudness"),
    #         row.get("mode"),
    #         row.get("key"),
    #         row.get("duration_ms"),
    #         row.get("time_signature"),
    #     )

    #     cur.execute(sql, params)

    # conn.commit()
    # cur.close()
    # conn.close()
    # print(f"✅ Songs updated for {artist_name}.")
    print(f"📀 Loading {len(df)} songs for {artist_name}...")

    for _, row in df.iterrows():
        # sql = """
        # INSERT INTO songs (
        #     title, artist_id, spotify_song_id, lyrics,
        #     danceability, energy, valence, tempo, speechiness,
        #     acousticness, instrumentalness, liveness, loudness,
        #     mode, key, duration_ms, time_signature, last_updated
        # )
        # VALUES (
        #     %s, %s, %s, %s,
        #     %s, %s, %s, %s, %s,
        #     %s, %s, %s, %s,
        #     %s, %s, %s, %s, NOW()
        # )
        #  ON CONFLICT (spotify_song_id) DO UPDATE
        # SET
        #     lyrics = EXCLUDED.lyrics,
        #     danceability = EXCLUDED.danceability,
        #     energy = EXCLUDED.energy,
        #     valence = EXCLUDED.valence,
        #     tempo = EXCLUDED.tempo,
        #     speechiness = EXCLUDED.speechiness,
        #     acousticness = EXCLUDED.acousticness,
        #     instrumentalness = EXCLUDED.instrumentalness,
        #     liveness = EXCLUDED.liveness,
        #     loudness = EXCLUDED.loudness,
        #     mode = EXCLUDED.mode,
        #     key = EXCLUDED.key,
        #     duration_ms = EXCLUDED.duration_ms,
        #     time_signature = EXCLUDED.time_signature,
        #     last_updated = NOW();
        # """
        sql="""
                INSERT INTO songs (
            title, artist_id, spotify_song_id, lyrics,
            danceability, energy, valence, tempo, speechiness,
            acousticness, instrumentalness, liveness, loudness,
            mode, key, duration_ms, time_signature,
            album_name, album_image_url, spotify_track_url, preview_url,
            last_updated
        )
                VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            NOW()
        )
        ON CONFLICT (spotify_song_id) DO UPDATE
        SET lyrics = EXCLUDED.lyrics,
            danceability = EXCLUDED.danceability,
            energy = EXCLUDED.energy,
            valence = EXCLUDED.valence,
            tempo = EXCLUDED.tempo,
            speechiness = EXCLUDED.speechiness,
            acousticness = EXCLUDED.acousticness,
            instrumentalness = EXCLUDED.instrumentalness,
            liveness = EXCLUDED.liveness,
            loudness = EXCLUDED.loudness,
            mode = EXCLUDED.mode,
            key = EXCLUDED.key,
            duration_ms = EXCLUDED.duration_ms,
            time_signature = EXCLUDED.time_signature,
            album_name = EXCLUDED.album_name,
            album_image_url = EXCLUDED.album_image_url,
            spotify_track_url = EXCLUDED.spotify_track_url,
            preview_url = EXCLUDED.preview_url,
            last_updated = NOW();


       """

        # params = (
        #     row.get("title"),
        #     artist_id,
        #     row.get("spotify_song_id"),
        #     row.get("lyrics"),
        #     row.get("danceability"),
        #     row.get("energy"),
        #     row.get("valence"),
        #     row.get("tempo"),
        #     row.get("speechiness"),
        #     row.get("acousticness"),
        #     row.get("instrumentalness"),
        #     row.get("liveness"),
        #     row.get("loudness"),
        #     row.get("mode"),
        #     row.get("key"),
        #     row.get("duration_ms"),
        #     row.get("time_signature"),
        # )

        params = (
            row.get("title"),
            artist_id,
            row.get("spotify_song_id"),
            row.get("lyrics"),
            row.get("danceability"),
            row.get("energy"),
            row.get("valence"),
            row.get("tempo"),
            row.get("speechiness"),
            row.get("acousticness"),
            row.get("instrumentalness"),
            row.get("liveness"),
            row.get("loudness"),
            row.get("mode"),
            row.get("key"),
            row.get("duration_ms"),
            row.get("time_signature"),
            row.get("album_name"),
            row.get("album_image_url"),
            row.get("spotify_track_url"),
            row.get("preview_url"),
        )


        # 1) Upsert song
        cur.execute(sql, params)

        # 2) Get song_id for this spotify_song_id
        cur.execute(
            "SELECT song_id FROM songs WHERE spotify_song_id = %s;",
            (row.get("spotify_song_id"),),
        )
        song_row = cur.fetchone()
        if not song_row:
            continue  # very unlikely, but safe
        song_id = song_row[0]

        # 3) Check if we already have mood for this song
        cur.execute(
            "SELECT 1 FROM song_mood WHERE song_id = %s LIMIT 1;",
            (song_id,),
        )
        already_has_mood = cur.fetchone() is not None

        if already_has_mood:
            continue  # don’t spend tokens twice

        # 4) Call Gemini/OpenAI to classify mood
        try:
            mood_result = classify_song_mood(
                title=row.get("title"),
                lyrics=row.get("lyrics"),
                artist_name=artist_name,
                genres=None,  # or fetch genres from artist table if you want
            )

              # ✅ PRINT HERE
            print(
                f"   🎧 Mood classified for '{row.get('title')}' by {artist_name}: "
                f"{mood_result['mood']} (conf={mood_result['confidence']:.2f})"
            )
            # insert into song_mood 
            cur.execute(
                """
                INSERT INTO song_mood (song_id, mood, mood_score)
                VALUES (%s, %s, %s)
                ON CONFLICT (song_id, mood) DO UPDATE
                SET mood_score = EXCLUDED.mood_score,
                    classified_at = NOW();
                """,
                (
                    song_id,
                    mood_result["mood"],
                    mood_result["confidence"],
                ),
            )
        except Exception as e:
            # Don’t break ETL if LLM call fails
            print(f"⚠️ Could not classify mood for {row.get('title')}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Songs updated for {artist_name}.")


