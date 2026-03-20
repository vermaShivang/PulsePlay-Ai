# import os
# import lyricsgenius
# from dotenv import load_dotenv

# load_dotenv()
# genius = lyricsgenius.Genius(os.getenv("GENIUS_ACCESS_TOKEN"))

# def fetch_lyrics(title, artist):
#     try:
#         song = genius.search_song(title, artist)
#         return song.lyrics if song else None
#     except Exception as e:
#         print(f"Error fetching lyrics: {e}")
#         return None


import os
import lyricsgenius
from dotenv import load_dotenv

load_dotenv()

genius = lyricsgenius.Genius(os.getenv("GENIUS_ACCESS_ TOKEN"),
                             timeout=10,
                             skip_non_songs=True,
                             remove_section_headers=True)

def fetch_lyrics(title, artist):
    """
    Fetch lyrics safely from Genius API.
    """
    try:
        song = genius.search_song(title, artist)
        if song:
            return song.lyrics
        else:
            return None
    except Exception as e:
        print(f"⚠️ Error fetching lyrics for {title}: {e}")
        return None
