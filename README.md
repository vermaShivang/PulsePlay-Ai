# PulsePlay — Admin UI

This repository now includes a simple Streamlit admin UI at `app.py` to run metadata backfills, analyze user mood via the LLM helper, and create playlists from DB results.

Quick start

1. Create a Python virtual environment and activate it.

   On Windows PowerShell:

```powershell
python -m venv pulseplay_venv
; .\pulseplay_venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy or verify your `.env` file contains the required variables (see existing `.env` in repo):

- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`
- `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` (for backfill)
- `GENIUS_ACCESS_TOKEN` (if using lyrics extraction)
- `OPENAI_API_KEY` or `GOOGLE_API_KEY` depending on `LLM_PROVIDER`

3. Run the UI

```powershell
streamlit run app.py
```

Notes

- The UI calls local Python modules (`backfill_spotify_metadata`, `mood_ai`, `main_etl`) — these must be importable and their dependencies installed.
- The `Mood Assistant` tab uses `mood_ai.analyze_user_mood`. The DB must contain `songs`, `artist`, and `song_mood` tables populated according to `schema.sql`.
- Playlist creation currently uses `user_id = 1` as a placeholder; change in `app.py` as needed.

If you want, I can:

- Add auth / simple token gating for the UI
- Convert the UI into a small Flask app with REST endpoints
- Improve playlist creation to accept a selectable user and preview songs before inserting
