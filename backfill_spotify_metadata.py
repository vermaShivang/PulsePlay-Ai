import os
import time
from typing import Optional, Dict

import psycopg2
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()


# ==============================================
# DB & Spotify clients
# ==============================================

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )


def get_spotify_client():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError(
            "Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET in environment."
        )

    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret,
    )
    return spotipy.Spotify(auth_manager=auth_manager)


# ==============================================
# Helper to fetch track metadata from Spotify
# ==============================================

def fetch_track_metadata(sp, spotify_song_id: str) -> Optional[Dict]:
    """
    Given a Spotify track ID, fetch album & URL metadata.

    Returns dict or None if track not found.
    """
    try:
        track = sp.track(spotify_song_id)
    except Exception as e:
        print(f"⚠️ Error fetching track {spotify_song_id} from Spotify: {e}")
        return None

    if not track:
        print(f"⚠️ No track found for spotify_song_id={spotify_song_id}")
        return None

    album = track.get("album", {}) or {}
    images = album.get("images", []) or []
    image_url = images[0]["url"] if images else None

    metadata = {
        "album_name": album.get("name"),
        "album_image_url": image_url,
        "spotify_track_url": (track.get("external_urls") or {}).get("spotify"),
        "preview_url": track.get("preview_url"),
    }
    return metadata


# ==============================================
# Main backfill logic
# ==============================================

def backfill_song_metadata(batch_sleep: float = 0.3):
    """
    Backfill album_name, album_image_url, spotify_track_url, preview_url
    for songs that don't have them yet.

    Only songs with a non-null spotify_song_id are processed.
    """

    conn = get_db_connection()
    cur = conn.cursor()

    # 1) Find songs that are missing any of these fields
    #    Adjust this WHERE clause if you only want to backfill
    #    completely empty rows.
    cur.execute(
        """
        SELECT song_id, spotify_song_id, title
        FROM songs
        WHERE
            spotify_song_id IS NOT NULL
            AND (
                album_name IS NULL
                OR album_image_url IS NULL
                OR spotify_track_url IS NULL
                OR preview_url IS NULL
            )
        ORDER BY song_id;
        """
    )
    rows = cur.fetchall()

    if not rows:
        print("✅ No songs require metadata backfill. All good!")
        cur.close()
        conn.close()
        return

    print(f"🎨 Found {len(rows)} songs needing Spotify metadata backfill.")

    sp = get_spotify_client()

    updated_count = 0
    skipped_count = 0

    for song_id, spotify_song_id, title in rows:
        if not spotify_song_id:
            print(f"⚠️ Song {song_id} '{title}' has no spotify_song_id, skipping.")
            skipped_count += 1
            continue

        print(f"\n🎵 Backfilling song_id={song_id}, title='{title}' "
              f"(spotify_id={spotify_song_id})")

        meta = fetch_track_metadata(sp, spotify_song_id)
        if not meta:
            print("   ⚠️ No metadata received, skipping update.")
            skipped_count += 1
            continue

        # 2) Update the row in DB
        cur.execute(
            """
            UPDATE songs
            SET
                album_name = COALESCE(%s, album_name),
                album_image_url = COALESCE(%s, album_image_url),
                spotify_track_url = COALESCE(%s, spotify_track_url),
                preview_url = COALESCE(%s, preview_url),
                last_updated = NOW()
            WHERE song_id = %s;
            """,
            (
                meta["album_name"],
                meta["album_image_url"],
                meta["spotify_track_url"],
                meta["preview_url"],
                song_id,
            ),
        )
        conn.commit()
        updated_count += 1

        print(
            f"   ✅ Updated: album='{meta['album_name']}', "
            f"cover={bool(meta['album_image_url'])}, "
            f"spotify_url={bool(meta['spotify_track_url'])}, "
            f"preview={bool(meta['preview_url'])}"
        )

        # Be nice to Spotify API
        time.sleep(batch_sleep)

    cur.close()
    conn.close()

    print("\n🎉 Backfill complete.")
    print(f"   ✅ Updated songs : {updated_count}")
    print(f"   ⚠️ Skipped songs : {skipped_count}")


if __name__ == "__main__":
    backfill_song_metadata()
