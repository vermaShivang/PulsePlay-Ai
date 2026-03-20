import os
import io
import json
import contextlib
import hashlib
from typing import List, Dict, Optional, Tuple

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    import psycopg2

    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(name: str, email: str, password: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            cur.close(); conn.close()
            return False, "User already exists with that email.", None
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING user_id;",
            (name, email, hash_password(password)),
        )
        uid = cur.fetchone()[0]
        conn.commit()
        cur.close(); conn.close()
        return True, "User created", uid
    except Exception as e:
        return False, str(e), None


def verify_user(email: str, password: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, name, password FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close(); conn.close()
        if not row:
            return False, None
        uid, name, pw_hash = row
        if pw_hash == hash_password(password):
            return True, {"user_id": uid, "name": name, "email": email}
        return False, None
    except Exception:
        return False, None


def get_user_playlists(user_id: int) -> List[Dict]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT playlist_id, mood, playlist_name, cover_url, created_at FROM playlist WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    rows = cur.fetchall()
    playlists = []
    for pid, mood, pname, cover_url, created_at in rows:
        playlists.append({"playlist_id": pid, "mood": mood, "playlist_name": pname, "cover_url": cover_url, "created_at": created_at})
    cur.close(); conn.close()
    return playlists


def get_playlist_songs(playlist_id: int) -> List[Dict]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.song_id, s.title, a.name AS artist_name, s.album_image_url, s.spotify_track_url, a.genres
        FROM playlist_song ps
        JOIN songs s ON ps.song_id = s.song_id
        JOIN artist a ON s.artist_id = a.artist_id
        WHERE ps.playlist_id = %s
        """,
        (playlist_id,)
    )
    rows = cur.fetchall()
    cur.close(); conn.close()
    return [
        {"song_id": r[0], "title": r[1], "artist_name": r[2], "album_image_url": r[3], "spotify_track_url": r[4], "genres": r[5]} 
        for r in rows
    ]


def create_playlist_for_user(user_id: int, playlist_name: str, mood: str, song_ids: List[int]):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO playlist (user_id, mood, playlist_name) VALUES (%s, %s, %s) RETURNING playlist_id;", (user_id, mood, playlist_name))
        pid = cur.fetchone()[0]
        for sid in song_ids:
            cur.execute("INSERT INTO playlist_song (playlist_id, song_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (pid, sid))
        # pick representative cover from these songs
        cover_url = None
        if song_ids:
            cur.execute("SELECT album_image_url FROM songs WHERE song_id = ANY(%s) AND album_image_url IS NOT NULL LIMIT 1;", (song_ids,))
            r = cur.fetchone()
            if r:
                cover_url = r[0]
        if cover_url:
            cur.execute("UPDATE playlist SET cover_url = %s WHERE playlist_id = %s", (cover_url, pid))
        conn.commit()
        cur.close(); conn.close()
        return True, "Playlist created", pid
    except Exception as e:
        return False, str(e), None


st.title("PulsePlay — Mood Playlists")

pages = ["Front", "Signup", "Login", "Home", "Playlist"]
if "page" not in st.session_state:
    st.session_state.page = "Front"

if "user" not in st.session_state:
    st.session_state.user = None
if "selected_playlist" not in st.session_state:
    st.session_state.selected_playlist = None


def nav_to(p: str):
    st.session_state.page = p


with st.sidebar:
    st.header("Navigation")
    choice = st.radio("Go to", pages, index=pages.index(st.session_state.page))
    if choice != st.session_state.page:
        nav_to(choice)
    if st.session_state.user:
        st.write(f"Signed in as: {st.session_state.user.get('name')}")
        if st.button("Logout"):
            st.session_state.user = None
            nav_to("Front")
        # Playlists quick-access
        st.markdown("---")
        st.write("Your Playlists")
        try:
            pls = get_user_playlists(st.session_state.user["user_id"])
            if pls:
                # build mapping id -> display
                options = {p["playlist_id"]: f"{p['playlist_name']} ({p['mood']})" for p in pls}
                sel = st.selectbox("Open playlist", options.keys(), format_func=lambda k: options[k])
                if st.button("View Playlist"):
                    st.session_state.selected_playlist = sel
                    nav_to("Playlist")
            else:
                st.write("(no playlists yet)")
        except Exception:
            st.write("Could not load playlists")


if st.session_state.page == "Front":
    st.header("Welcome to PulsePlay")
    st.write("Create mood-based playlists and manage them.")
    st.image("https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=1200&auto=format&fit=crop&q=80", use_column_width=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Get started — Sign up"):
            nav_to("Signup")
    with col2:
        if st.button("Have an account? Log in"):
            nav_to("Login")


elif st.session_state.page == "Signup":
    st.header("Sign up")
    name = st.text_input("Full name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create account"):
        ok, msg, uid = create_user(name, email, password)
        if ok:
            st.success(msg)
            st.session_state.user = {"user_id": uid, "name": name, "email": email}
            nav_to("Home")
        else:
            st.error(msg)


elif st.session_state.page == "Login":
    st.header("Log in")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Log in"):
        ok, user = verify_user(email, password)
        if ok:
            st.success("Logged in")
            st.session_state.user = user
            nav_to("Home")
        else:
            st.error("Invalid credentials")


elif st.session_state.page == "Home":
    if not st.session_state.user:
        st.warning("You must be logged in to use Home. Please sign up or log in.")
        if st.button("Go to Login"):
            nav_to("Login")
    else:
        st.header("Your Mood Assistant")
        st.write("Describe how you're feeling and PulsePlay will suggest a playlist to uplift or match your mood.")
        user_text = st.text_area("How are you feeling?", height=120)
        num_songs = st.slider("Number of songs", 1, 50, 15)
        if st.button("Create playlist from mood"):
            try:
                from mood_ai import analyze_user_mood
            except Exception as e:
                st.error(f"Mood AI module not available: {e}")
            else:
                with st.spinner("Analyzing mood..."):
                    analysis = analyze_user_mood(user_text)
                # Attractive AI output
                st.subheader("Mood Analysis")
                mood = analysis.get("target_music_mood", "neutral").capitalize()
                confidence = analysis.get("confidence", 0.0)
                reason = analysis.get("user_mood_raw", "")
                message = analysis.get("message_to_user", "")
                cols = st.columns((2, 3))
                with cols[0]:
                    st.metric(label="Suggested Music Mood", value=mood)
                    st.progress(confidence)
                with cols[1]:
                    st.write(f"**Why:** {reason}")
                    st.info(message)

                target = analysis.get("target_music_mood") or "happy"
                # fetch songs for target mood
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute(
                        """
                        SELECT s.song_id, s.title, a.name AS artist_name, s.album_image_url
                        FROM songs s
                        JOIN artist a ON s.artist_id = a.artist_id
                        JOIN song_mood sm ON s.song_id = sm.song_id
                        WHERE sm.mood = %s
                        ORDER BY sm.mood_score DESC, RANDOM()
                        LIMIT %s;
                        """,
                        (target, num_songs),
                    )
                    rows = cur.fetchall()
                    if not rows:
                        cur.execute(
                            """
                            SELECT s.song_id, s.title, a.name AS artist_name, s.album_image_url
                            FROM songs s
                            JOIN artist a ON s.artist_id = a.artist_id
                            ORDER BY RANDOM()
                            LIMIT %s;
                            """,
                            (num_songs,),
                        )
                        rows = cur.fetchall()
                    song_ids = [r[0] for r in rows]
                    # create playlist
                    playlist_name = f"Mood Boost - {target.capitalize()}"
                    ok, msg, pid = create_playlist_for_user(st.session_state.user["user_id"], playlist_name, target, song_ids)
                    if ok:
                        st.success(f"Playlist created: {playlist_name}")
                        # select and redirect to playlist view
                        st.session_state.selected_playlist = pid
                        nav_to("Playlist")
                    else:
                        st.error(f"Failed to create playlist: {msg}")
                    cur.close(); conn.close()
                except Exception as e:
                    st.error(f"DB error fetching songs: {e}")

        st.markdown("---")
        st.subheader("Your playlists")
        try:
            playlists = get_user_playlists(st.session_state.user["user_id"])
            if not playlists:
                st.info("You have no playlists yet.")
            for p in playlists:
                cols = st.columns((1, 4))
                songs = get_playlist_songs(p["playlist_id"])
                # prefer stored playlist cover_url, otherwise pick from songs
                cover = p.get("cover_url")
                if not cover and songs:
                    for s in songs:
                        if s.get("album_image_url"):
                            cover = s.get("album_image_url")
                            break
                with cols[0]:
                    if cover:
                        st.image(cover, width=120)
                    else:
                        st.empty()
                with cols[1]:
                    st.markdown(f"### {p['playlist_name']}")
                    st.write(f"Mood: **{p['mood']}** — Created: {p['created_at']}")
                    if songs:
                        # show top 3 song previews with thumbnails
                        for s in songs[:3]:
                            g = s.get("genres") or []
                            gtxt = ", ".join(g) if isinstance(g, (list, tuple)) else str(g)
                            s_cols = st.columns((1, 6))
                            with s_cols[0]:
                                if s.get("album_image_url"):
                                    st.image(s.get("album_image_url"), width=64)
                                else:
                                    st.empty()
                            with s_cols[1]:
                                st.markdown(f"**{s['title']}**")
                                st.write(f"{s['artist_name']}")
                                if s.get("spotify_track_url"):
                                    st.markdown(f"[Open on Spotify]({s['spotify_track_url']})")
                                if gtxt:
                                    st.caption(f"Genres: {gtxt}")
                    else:
                        st.write("(no songs)")
                    if st.button(f"Open {p['playlist_name']}", key=f"open_{p['playlist_id']}"):
                        st.session_state.selected_playlist = p['playlist_id']
                        nav_to("Playlist")
                st.markdown("---")
        except Exception as e:
            st.error(f"Failed to load playlists: {e}")


elif st.session_state.page == "Playlist":
    pid = st.session_state.selected_playlist
    if not pid:
        st.warning("No playlist selected. Choose one from the sidebar or your Home page.")
    else:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT playlist_name, mood, cover_url, created_at FROM playlist WHERE playlist_id = %s", (pid,))
            row = cur.fetchone()
            if not row:
                st.error("Playlist not found")
            else:
                pname, pmood, pcover, pcreated = row
                st.header(pname)
                if pcover:
                    st.image(pcover, width=360)
                st.write(f"Mood: **{pmood}** — Created: {pcreated}")
                songs = get_playlist_songs(pid)
                if not songs:
                    st.info("No songs in this playlist.")
                for s in songs:
                    for s in songs:
                        cols = st.columns((1, 4))
                        with cols[0]:
                            if s.get("album_image_url"):
                                st.image(s.get("album_image_url"), width=140)
                            else:
                                st.empty()
                        with cols[1]:
                            st.markdown(f"**{s['title']}**")
                            st.write(f"Artist: {s['artist_name']}")
                            genres = s.get("genres") or []
                            if genres:
                                gtxt = ", ".join(genres) if isinstance(genres, (list, tuple)) else str(genres)
                                st.caption(f"Genres: {gtxt}")
                            if s.get("spotify_track_url"):
                                st.markdown(f"[Open on Spotify]({s['spotify_track_url']})")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Failed to load playlist: {e}")
        finally:
            try:
                cur.close(); conn.close()
            except Exception:
                pass


