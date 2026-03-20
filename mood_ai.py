# # mood_ai.py
# import os
# import json
# from typing import Optional, List, Dict

# # --- OpenAI client ---
# try:
#     from openai import OpenAI
# except ImportError:
#     OpenAI = None

# # --- Gemini client ---
# try:
#     import google.generativeai as genai
# except ImportError:
#     genai = None
# mood_ai.py
import os
import json
from typing import Optional, List, Dict

from dotenv import load_dotenv
load_dotenv()   # ✅ ensure .env is loaded before reading LLM_PROVIDER

# --- OpenAI client ---
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# --- Gemini client ---
try:
    import google.generativeai as genai
except ImportError:
    genai = None

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
print("Using LLM provider:", LLM_PROVIDER)

# LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
SONG_MOOD_LABELS = [
    "happy", "sad", "romantic", "energetic", "calm",
    "angry", "melancholic", "motivational", "party",
    "devotional", "neutral"
]

_user_mood_labels = [
    "very_happy", "happy", "calm", "relaxed",
    "stressed", "anxious", "sad", "angry", "tired", "lonely"
]


# ============================================================
#   INTERNAL: CLIENT HELPERS
# ============================================================
_openai_client = None
_gemini_model = None


def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        if OpenAI is None:
            raise RuntimeError("openai package not installed. pip install openai")
        _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _openai_client


def _get_gemini_model():
    global _gemini_model
    if _gemini_model is None:
        if genai is None:
            raise RuntimeError("google-generativeai not installed. pip install google-generativeai")
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        _gemini_model = genai.GenerativeModel("gemini-2.5-flash")
    return _gemini_model


# ============================================================
#   SONG MOOD CLASSIFICATION
# ============================================================
def _build_song_prompt(
    title: str,
    lyrics: Optional[str],
    artist_name: Optional[str],
    genres: Optional[List[str]]
) -> str:
    parts = [
        f"Song title: {title}",
        f"Artist: {artist_name or 'Unknown'}",
        f"Genres: {', '.join(genres) if genres else 'Unknown'}",
    ]
    if lyrics:
        # Truncate very long lyrics to save tokens
        snippet = lyrics[:3000]
        parts.append("Lyrics:")
        parts.append(snippet)
    return "\n".join(parts)


def classify_song_mood(
    title: str,
    lyrics: Optional[str] = None,
    artist_name: Optional[str] = None,
    genres: Optional[List[str]] = None
) -> Dict:
    """
    Use LLM (OpenAI/Gemini) to classify song mood.

    Returns:
        {
          "mood": "<one of SONG_MOOD_LABELS>",
          "confidence": 0.0-1.0,
          "reason": "<short explanation>"
        }
    """
    prompt_body = _build_song_prompt(title, lyrics, artist_name, genres)
    instruction = (
        "You are a music psychologist. "
        "Given song metadata and optional lyrics, classify the primary emotional mood of the song. "
        f"Choose ONE mood from this list only: {', '.join(SONG_MOOD_LABELS)}.\n\n"
        "Return a strict JSON object with keys:\n"
        '{ "mood": "<label>", "confidence": <0-1 float>, "reason": "<short explanation>" }.\n'
        "Do not add any extra text."
    )

    if LLM_PROVIDER == "gemini":
        model = _get_gemini_model()
        resp = model.generate_content(instruction + "\n\n" + prompt_body)
        content = resp.text
    else:
        client = _get_openai_client()
        model_name = os.getenv("OPENAI_MOOD_MODEL", "gpt-4o-mini")
        resp = client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": prompt_body},
            ],
            temperature=0.2,
        )
        content = resp.choices[0].message.content

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Very defensive fallback
        data = {"mood": "neutral", "confidence": 0.5, "reason": "Fallback due to parse error."}

    mood = (data.get("mood") or "neutral").lower().strip()
    if mood not in SONG_MOOD_LABELS:
        mood = "neutral"

    try:
        confidence = float(data.get("confidence", 0.7))
    except (TypeError, ValueError):
        confidence = 0.7
    confidence = max(0.0, min(confidence, 1.0))

    reason = data.get("reason", "")
    return {"mood": mood, "confidence": confidence, "reason": reason}


# ============================================================
#   USER MOOD ANALYSIS (CHAT INPUT)
# ============================================================
def analyze_user_mood(user_text: str) -> Dict:
    """
    Analyse how the user is feeling based on free-form text,
    and propose a target mood to uplift them.

    Returns:
        {
          "user_mood_raw": "<short phrase>",
          "user_mood_label": "<one of _user_mood_labels>",
          "target_music_mood": "<one of SONG_MOOD_LABELS>",
          "confidence": 0.0-1.0,
          "message_to_user": "<1-2 line empathetic response>"
        }
    """

    instruction = (
        "You are an empathetic mood analyst and music coach. "
        "A user describes how they feel. "
        "1) Summarise their mood in a short phrase (user_mood_raw).\n"
        f"2) Map it to ONE label from: {', '.join(_user_mood_labels)} (user_mood_label).\n"
        f"3) Choose ONE music mood from: {', '.join(SONG_MOOD_LABELS)} "
        "(target_music_mood) that would best uplift or comfort them.\n"
        "4) Give a short, friendly 1-2 line message (message_to_user).\n\n"
        "Respond ONLY as a JSON object with keys:\n"
        '{ "user_mood_raw": "...", '
        '"user_mood_label": "...", '
        '"target_music_mood": "...", '
        '"confidence": 0.0-1.0, '
        '"message_to_user": "..." }'
    )

    if LLM_PROVIDER == "gemini":
        model = _get_gemini_model()
        resp = model.generate_content(instruction + "\n\nUser text:\n" + user_text)
        content = resp.text
    else:
        client = _get_openai_client()
        model_name = os.getenv("OPENAI_MOOD_MODEL", "gpt-4o-mini")
        resp = client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": user_text},
            ],
            temperature=0.3,
        )
        content = resp.choices[0].message.content

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = {
            "user_mood_raw": "not sure",
            "user_mood_label": "neutral",
            "target_music_mood": "happy",
            "confidence": 0.5,
            "message_to_user": "I hope some cheerful music can lift your mood today 💛",
        }

    # Normalise labels
    label = (data.get("user_mood_label") or "neutral").lower().strip()
    if label not in _user_mood_labels:
        label = "neutral"

    target = (data.get("target_music_mood") or "happy").lower().strip()
    if target not in SONG_MOOD_LABELS:
        target = "happy"

    try:
        conf = float(data.get("confidence", 0.7))
    except (TypeError, ValueError):
        conf = 0.7
    conf = max(0.0, min(conf, 1.0))

    return {
        "user_mood_raw": data.get("user_mood_raw", ""),
        "user_mood_label": label,
        "target_music_mood": target,
        "confidence": conf,
        "message_to_user": data.get("message_to_user", ""),
    }
