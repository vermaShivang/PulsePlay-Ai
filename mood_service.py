# # mood_service.py
# import os
# from typing import List, Dict, Tuple
# import psycopg2
# from dotenv import load_dotenv
# from mood_ai import analyze_user_mood

# load_dotenv()


# def get_connection():
#     return psycopg2.connect(
#         dbname=os.getenv("POSTGRES_DB"),
#         user=os.getenv("POSTGRES_USER"),
#         password=os.getenv("POSTGRES_PASSWORD"),
#         host=os.getenv("POSTGRES_HOST"),
#         port=os.getenv("POSTGRES_PORT"),
#     )


# # ============================================================
# #   HELPER QUERIES
# # ============================================================
# def log_user_mood(user_id: int, mood: str, mood_score: float) -> None:
#     """
#     Insert a row into user_mood table.
#     """
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         INSERT INTO user_mood (user_id, mood, mood_score)
#         VALUES (%s, %s, %s);
#         """,
#         (user_id, mood, mood_score),
#     )
#     conn.commit()
#     cur.close()
#     conn.close()


# def get_songs_for_target_mood(target_mood: str, limit: int = 20) -> List[Dict]:
#     """
#     Fetch songs whose song_mood matches the target_mood.
#     If nothing found, fallback to any 'happy' or random songs.
#     """
#     conn = get_connection()
#     cur = conn.cursor()

#     # Primary: exact mood match
#     cur.execute(
#         """
#         SELECT s.song_id, s.title, a.name AS artist_name
#         FROM songs s
#         JOIN artist a ON s.artist_id = a.artist_id
#         JOIN song_mood sm ON s.song_id = sm.song_id
#         WHERE sm.mood = %s
#         ORDER BY sm.mood_score DESC, RANDOM()
#         LIMIT %s;
#         """,
#         (target_mood, limit),
#     )
#     rows = cur.fetchall()
#     if not rows:
#         # Try 'happy' as universal uplift fallback
#         cur.execute(
#             """
#             SELECT s.song_id, s.title, a.name AS artist_name
#             FROM songs s
#             JOIN artist a ON s.artist_id = a.artist_id
#             JOIN song_mood sm ON s.song_id = sm.song_id
#             WHERE sm.mood = 'happy'
#             ORDER BY sm.mood_score DESC, RANDOM()
#             LIMIT %s;
#             """,
#             (limit,),
#         )
#         rows = cur.fetchall()

#     if not rows:
#         # Final fallback: any random songs
#         cur.execute(
#             """
#             SELECT s.song_id, s.title, a.name AS artist_name
#             FROM songs s
#             JOIN artist a ON s.artist_id = a.artist_id
#             ORDER BY RANDOM()
#             LIMIT %s;
#             """,
#             (limit,),
#         )
#         rows = cur.fetchall()

#     cur.close()
#     conn.close()

#     songs = []
#     for song_id, title, artist_name in rows:
#         songs.append(
#             {"song_id": song_id, "title": title, "artist_name": artist_name}
#         )
#     return songs


# def create_playlist(
#     user_id: int, mood: str, songs: List[Dict], playlist_name: str
# ) -> Tuple[int, str]:
#     """
#     Create a playlist for a user with given songs.
#     Returns (playlist_id, playlist_name).
#     """
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute(
#         """
#         INSERT INTO playlist (user_id, mood)
#         VALUES (%s, %s)
#         RETURNING playlist_id;
#         """,
#         (user_id, mood),
#     )
#     playlist_id = cur.fetchone()[0]

#     # Insert songs into playlist_song
#     for s in songs:
#         cur.execute(
#             """
#             INSERT INTO playlist_song (playlist_id, song_id)
#             VALUES (%s, %s)
#             ON CONFLICT (playlist_id, song_id) DO NOTHING;
#             """,
#             (playlist_id, s["song_id"]),
#         )

#     conn.commit()
#     cur.close()
#     conn.close()

#     return playlist_id, playlist_name


# def get_playlists_for_user(user_id: int) -> List[Dict]:
#     """
#     Return all playlists for a given user with basic info.
#     """
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         SELECT playlist_id, mood, created_at
#         FROM playlist
#         WHERE user_id = %s
#         ORDER BY created_at DESC;
#         """,
#         (user_id,),
#     )
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()

#     playlists = []
#     for pid, mood, created_at in rows:
#         playlists.append(
#             {
#                 "playlist_id": pid,
#                 "mood": mood,
#                 "created_at": created_at.isoformat()
#                 if hasattr(created_at, "isoformat")
#                 else str(created_at),
#             }
#         )
#     return playlists


# # ============================================================
# #   MAIN ENTRYPOINT: CHAT STYLE MOOD → PLAYLIST
# # ============================================================
# def handle_user_mood_and_create_playlist(
#     user_id: int, user_text: str, num_songs: int = 15
# ) -> Dict:
#     """
#     Core logic for:
#     - Analyse user mood via LLM
#     - Log mood in user_mood
#     - Pick songs for uplift target mood
#     - Create playlist and return info
#     """
#     # 1) LLM mood analysis
#     analysis = analyze_user_mood(user_text)
#     user_mood_label = analysis["user_mood_label"]
#     target_mood = analysis["target_music_mood"]
#     confidence = analysis["confidence"]
#     message_to_user = analysis["message_to_user"]
#     user_mood_raw = analysis["user_mood_raw"]

#     # 2) Log user mood in DB
#     log_user_mood(user_id, user_mood_label, confidence)

#     # 3) Fetch songs for target mood
#     songs = get_songs_for_target_mood(target_mood, limit=num_songs)

#     # 4) Create playlist
#     playlist_name = f"Mood Boost - {target_mood.capitalize()}"
#     playlist_id, _ = create_playlist(user_id, target_mood, songs, playlist_name)

#     return {
#         "user_mood_raw": user_mood_raw,
#         "user_mood_label": user_mood_label,
#         "target_mood": target_mood,
#         "confidence": confidence,
#         "message_to_user": message_to_user,
#         "playlist_id": playlist_id,
#         "playlist_name": playlist_name,
#         "songs": songs,
#     }


# # ============================================================
# #   SIMPLE CLI-STYLE CHAT LOOP (for testing)
# # ============================================================
# if __name__ == "__main__":
#     print("👋 Welcome to PulsePlay Mood Assistant!")
#     uid = input("Enter your user_id (numeric from users table): ").strip()
#     user_id = int(uid)

#     while True:
#         print("\nHow are you feeling today? (type 'exit' to quit)")
#         text = input("You: ").strip()
#         if text.lower() in ("exit", "quit"):
#             break

#         result = handle_user_mood_and_create_playlist(user_id, text)

#         print("\nAssistant:", result["message_to_user"])
#         print(
#             f"Detected mood: {result['user_mood_label']} "
#             f"→ Target playlist mood: {result['target_mood']}"
#         )
#         print(
#             f"Created playlist #{result['playlist_id']} "
#             f"({result['playlist_name']}) with {len(result['songs'])} songs:"
#         )
#         for s in result["songs"]:
#             print(f"  - {s['title']} — {s['artist_name']}")

#         print("\nYour playlists so far:")
#         for pl in get_playlists_for_user(user_id):
#             print(f"  • #{pl['playlist_id']} [{pl['mood']}] at {pl['created_at']}")
# mood_service.py
import os
from typing import List, Dict, Tuple
import psycopg2
from dotenv import load_dotenv
from mood_ai import analyze_user_mood
from datetime import datetime

load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )


# ============================================================
#   HELPER QUERIES
# ============================================================
# def log_user_mood(user_id: int, mood: str, mood_score: float) -> None:
#     """
#     Insert a row into user_mood table.
#     """
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         INSERT INTO user_mood (user_id, mood, mood_score)
#         VALUES (%s, %s, %s);
#         """,
#         (user_id, mood, mood_score),
#     )
#     conn.commit()
#     cur.close()
#     conn.close()

def log_user_mood(
    user_id: int,
    mood: str,
    mood_score: float,
    mood_input_text: str,
) -> None:
    """
    Store user mood label + score + the raw text they typed.
    timestamp is auto-filled by DB.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO user_mood (user_id, mood, mood_score, mood_input_text)
        VALUES (%s, %s, %s, %s);
        """,
        (user_id, mood, mood_score, mood_input_text),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_songs_for_target_mood(target_mood: str, limit: int = 20) -> List[Dict]:
    """
    Fetch songs whose song_mood matches the target_mood.
    If nothing found, fallback to any 'happy' or random songs.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Primary: exact mood match
    cur.execute(
        """
        SELECT s.song_id, s.title, a.name AS artist_name
        FROM songs s
        JOIN artist a ON s.artist_id = a.artist_id
        JOIN song_mood sm ON s.song_id = sm.song_id
        WHERE sm.mood = %s
        ORDER BY sm.mood_score DESC, RANDOM()
        LIMIT %s;
        """,
        (target_mood, limit),
    )
    rows = cur.fetchall()
    if not rows:
        # Try 'happy' as universal uplift fallback
        cur.execute(
            """
            SELECT s.song_id, s.title, a.name AS artist_name
            FROM songs s
            JOIN artist a ON s.artist_id = a.artist_id
            JOIN song_mood sm ON s.song_id = sm.song_id
            WHERE sm.mood = 'happy'
            ORDER BY sm.mood_score DESC, RANDOM()
            LIMIT %s;
            """,
            (limit,),
        )
        rows = cur.fetchall()

    if not rows:
        # Final fallback: any random songs
        cur.execute(
            """
            SELECT s.song_id, s.title, a.name AS artist_name
            FROM songs s
            JOIN artist a ON s.artist_id = a.artist_id
            ORDER BY RANDOM()
            LIMIT %s;
            """,
            (limit,),
        )
        rows = cur.fetchall()

    cur.close()
    conn.close()

    songs = []
    for song_id, title, artist_name in rows:
        songs.append(
            {"song_id": song_id, "title": title, "artist_name": artist_name}
        )
    return songs

# yaha par ab hum change kar rahe hai to accept the playlist name as welll

# def create_playlist(
#     user_id: int, mood: str, songs: List[Dict], playlist_name: str
# ) -> Tuple[int, str]:
#     """
#     Create a playlist for a user with given songs.
#     Returns (playlist_id, playlist_name).
#     """
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute(
#         """
#         INSERT INTO playlist (user_id, mood)
#         VALUES (%s, %s)
#         RETURNING playlist_id;
#         """,
#         (user_id, mood),
#     )
#     playlist_id = cur.fetchone()[0]

#     # Insert songs into playlist_song
#     for s in songs:
#         cur.execute(
#             """
#             INSERT INTO playlist_song (playlist_id, song_id)
#             VALUES (%s, %s)
#             ON CONFLICT (playlist_id, song_id) DO NOTHING;
#             """,
#             (playlist_id, s["song_id"]),
#         )

#     conn.commit()
#     cur.close()
#     conn.close()

#     return playlist_id, playlist_name
def create_playlist_for_user(
    user_id: int,
    mood: str,
    song_ids: List[int],
    playlist_name: str,
) -> Dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO playlist (user_id, mood, playlist_name)
        VALUES (%s, %s, %s)
        RETURNING playlist_id;
        """,
        (user_id, mood, playlist_name),
    )
    playlist_id = cur.fetchone()[0]

    for sid in song_ids:
        cur.execute(
            """
            INSERT INTO playlist_song (playlist_id, song_id)
            VALUES (%s, %s)
            ON CONFLICT (playlist_id, song_id) DO NOTHING;
            """,
            (playlist_id, sid),
        )

    conn.commit()
    cur.close()
    conn.close()

    return {
        "playlist_id": playlist_id,
        "mood": mood,
        "playlist_name": playlist_name,
    }


def create_playlist(
    user_id: int,
    mood: str,
    song_ids: List[int],
    playlist_name: str,
) -> Dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO playlist (user_id, mood, playlist_name)
        VALUES (%s, %s, %s)
        RETURNING playlist_id;
        """,
        (user_id, mood, playlist_name),
    )
    playlist_id = cur.fetchone()[0]

    for sid in song_ids:
        cur.execute(
            """
            INSERT INTO playlist_song (playlist_id, song_id)
            VALUES (%s, %s)
            ON CONFLICT (playlist_id, song_id) DO NOTHING;
            """,
            (playlist_id, sid),
        )

    conn.commit()
    cur.close()
    conn.close()

    return {
        "playlist_id": playlist_id,
        "mood": mood,
        "playlist_name": playlist_name,
    }


# def get_playlists_for_user(user_id: int) -> List[Dict]:
#     """
#     Return all playlists for a given user with basic info.
#     """
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         SELECT playlist_id, mood, created_at
#         FROM playlist
#         WHERE user_id = %s
#         ORDER BY created_at DESC;
#         """,
#         (user_id,),
#     )
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()

#     playlists = []
#     for pid, mood, created_at in rows:
#         playlists.append(
#             {
#                 "playlist_id": pid,
#                 "mood": mood,
#                 "created_at": created_at.isoformat()
#                 if hasattr(created_at, "isoformat")
#                 else str(created_at),
#             }
#         )
#     return playlists



# def get_playlists_for_user(user_id: int) -> List[Dict]:
#     """
#     Return all playlists for a given user with basic info.
#     """
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         SELECT playlist_id, playlist_name, mood, created_at
#         FROM playlist
#         WHERE user_id = %s
#         ORDER BY created_at DESC;
#         """,
#         (user_id,),
#     )
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()

#     playlists = []
#     for pid, pname, mood, created_at in rows:
#         playlists.append(
#             {
#                 "playlist_id": pid,
#                 "playlist_name": pname,
#                 "mood": mood,
#                 "created_at": created_at.isoformat()
#                 if hasattr(created_at, "isoformat")
#                 else str(created_at),
#             }
#         )
#     return playlists

import random

def get_playlists_for_user(user_id: int) -> List[Dict]:
    """
    Return all playlists for a given user with basic info, including random cover image from playlist songs.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT playlist_id, playlist_name, mood, created_at
        FROM playlist
        WHERE user_id = %s
        ORDER BY created_at DESC;
        """,
        (user_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    playlists = []
    for pid, pname, mood, created_at in rows:
        # Fetch the songs in this playlist
        playlist_songs = get_playlist_with_songs(pid)["songs"]
        if playlist_songs:
            # Pick a random song to get its cover image
            random_song = random.choice(playlist_songs)
            cover_image_url = random_song.get("cover_image_url", None)
        else:
            cover_image_url = None
        
        playlists.append(
            {
                "playlist_id": pid,
                "playlist_name": pname,
                "mood": mood,
                "created_at": created_at.isoformat()
                if hasattr(created_at, "isoformat")
                else str(created_at),
                "cover_image_url": cover_image_url,  # Add cover image URL here
            }
        )
    return playlists



# ============================================================
#   MAIN ENTRYPOINT: CHAT STYLE MOOD → PLAYLIST
# ============================================================
# def handle_user_mood_and_create_playlist(
#     user_id: int, user_text: str, num_songs: int = 15
# ) -> Dict:
#     """
#     Core logic for:
#     - Analyse user mood via LLM
#     - Log mood in user_mood
#     - Pick songs for uplift target mood
#     - Create playlist and return info
#     """
#     # 1) LLM mood analysis
#     analysis = analyze_user_mood(user_text)
#     user_mood_label = analysis["user_mood_label"]
#     target_mood = analysis["target_music_mood"]
#     confidence = analysis["confidence"]
#     message_to_user = analysis["message_to_user"]
#     user_mood_raw = analysis["user_mood_raw"]

#     # 2) Log user mood in DB
#     log_user_mood(user_id, user_mood_label, confidence,user_text)

#     # 3) Fetch songs for target mood
#     songs = get_songs_for_target_mood(target_mood, limit=num_songs)

#     # 4) Create playlist
#     playlist_name = f"Mood Boost - {target_mood.capitalize()}"
#     playlist_id, _ = create_playlist(user_id, target_mood, songs, playlist_name)

#     return {
#         "user_mood_raw": user_mood_raw,
#         "user_mood_label": user_mood_label,
#         "target_mood": target_mood,
#         "confidence": confidence,
#         "message_to_user": message_to_user,
#         "playlist_id": playlist_id,
#         "playlist_name": playlist_name,
#         "songs": songs,
#     }


def handle_user_mood_and_create_playlist(
    user_id: int, user_text: str, num_songs: int = 15
) -> Dict:
    """
    Core logic for:
    - Analyse user mood via LLM
    - Log mood in user_mood
    - Pick songs for uplift target mood
    - Create playlist and return info
    """
    # 1) LLM mood analysis
    analysis = analyze_user_mood(user_text)
    user_mood_label = analysis["user_mood_label"]
    target_mood = analysis["target_music_mood"]
    confidence = analysis["confidence"]
    message_to_user = analysis["message_to_user"]
    user_mood_raw = analysis["user_mood_raw"]

    # 2) Log user mood in DB (with raw input text)
    log_user_mood(user_id, user_mood_label, confidence, user_text)

    # 3) Fetch songs for target mood
    songs = get_songs_for_target_mood(target_mood, limit=num_songs)

    # Build list of song_ids for playlist_song table
    song_ids = [s["song_id"] for s in songs]

    # 4) Generate a descriptive playlist name
    playlist_name = generate_playlist_name(
        user_mood_label=user_mood_label,
        target_music_mood=target_mood,
    )

    # 5) Create playlist in DB
    playlist = create_playlist(
        user_id=user_id,
        mood=target_mood,
        song_ids=song_ids,
        playlist_name=playlist_name,
    )

    return {
        "user_mood_raw": user_mood_raw,
        "user_mood_label": user_mood_label,
        "target_mood": target_mood,
        "confidence": confidence,
        "message_to_user": message_to_user,
        "playlist_id": playlist["playlist_id"],
        "playlist_name": playlist["playlist_name"],
        "songs": songs,  # full dicts including title + artist_name
    }



# generate playlist name
def generate_playlist_name(user_mood_label: str, target_music_mood: str) -> str:
    """
    Create a descriptive playlist name based on detected mood and target mood.
    Example: "Happy Boost • from stressed • 17 Nov 2025, 22:15"
    """
    ts = datetime.now().strftime("%d %b %Y, %H:%M")
    return f"{target_music_mood.capitalize()} Boost • from {user_mood_label} • {ts}"


# ============================================
# HELPER TO FETCH SONG DETAILS
# ===============================================
def get_playlist_with_songs(playlist_id: int) -> Dict:
    """
    Return playlist header + full song info including cover image and URLs.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Playlist header
    cur.execute(
        """
        SELECT p.playlist_id, p.playlist_name, p.mood, p.created_at, u.name
        FROM playlist p
        JOIN users u ON p.user_id = u.user_id
        WHERE p.playlist_id = %s;
        """,
        (playlist_id,),
    )
    header = cur.fetchone()
    if not header:
        cur.close()
        conn.close()
        return {}

    playlist = {
        "playlist_id": header[0],
        "playlist_name": header[1],
        "mood": header[2],
        "created_at": header[3],
        "user_name": header[4],
        "songs": [],
    }

    # Songs with artist + cover
    cur.execute(
        """
        SELECT
            s.song_id,
            s.title,
            a.name AS artist_name,
            a.genres,
            s.album_name,
            s.album_image_url,
            s.spotify_track_url,
            s.preview_url
        FROM playlist_song ps
        JOIN songs s ON ps.song_id = s.song_id
        JOIN artist a ON s.artist_id = a.artist_id
        WHERE ps.playlist_id = %s
        ORDER BY s.title;
        """,
        (playlist_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    for r in rows:
        playlist["songs"].append({
            "song_id": r[0],
            "title": r[1],
            "artist_name": r[2],
            "artist_genres": r[3],
            "album_name": r[4],
            "cover_image_url": r[5],
            "spotify_url": r[6],
            "preview_url": r[7],
        })

    return playlist


# ============================================================
#   SIMPLE CLI-STYLE CHAT LOOP (for testing)
# ============================================================
if __name__ == "__main__":
    print("👋 Welcome to PulsePlay Mood Assistant!")
    uid = input("Enter your user_id (numeric from users table): ").strip()
    user_id = int(uid)

    while True:
        print("\nHow are you feeling today? (type 'exit' to quit)")
        text = input("You: ").strip()
        if text.lower() in ("exit", "quit"):
            break

        result = handle_user_mood_and_create_playlist(user_id, text)

        print("\nAssistant:", result["message_to_user"])
        print(
            f"Detected mood: {result['user_mood_label']} "
            f"→ Target playlist mood: {result['target_mood']}"
        )
        print(
            f"Created playlist #{result['playlist_id']} "
            f"({result['playlist_name']}) with {len(result['songs'])} songs:"
        )
        for s in result["songs"]:
            print(f"  - {s['title']} — {s['artist_name']}")

        print("\nYour playlists so far:")
        # for pl in get_playlists_for_user(user_id):
        #     print(f"  • #{pl['playlist_id']} [{pl['mood']}] at {pl['created_at']}")
        for pl in get_playlists_for_user(user_id):
            print(
                    f"  • #{pl['playlist_id']} {pl['playlist_name']} "
                    f"[{pl['mood']}] at {pl['created_at']}"
                )



