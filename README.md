# 🎵 PulsePlay-Ai

> **Intelligent Mood-Based Music Playlist Generation**

[![GitHub](https://img.shields.io/badge/GitHub-vermaShivang/PulsePlay--Ai-blue?logo=github)](https://github.com/vermaShivang/PulsePlay-Ai)
[![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?logo=streamlit)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue?logo=postgresql)](https://www.postgresql.org/)

PulsePlay-Ai is an AI-powered music recommendation system that generates personalized playlists based on your emotional state. Using natural language processing and machine learning, it analyzes your mood and creates the perfect soundtrack for your moment.

## ✨ Features

- **🤖 AI Mood Analysis**: Leverages GPT-4/Gemini to understand your emotional state from natural language
- **🎵 Intelligent Playlist Generation**: Creates curated playlists matching your mood
- **📊 Audio Feature Analysis**: Uses Spotify's audio features (danceability, energy, valence, tempo, etc.)
- **📝 Lyrics Integration**: Analyzes song lyrics for deeper mood understanding
- **👤 User Authentication**: Secure signup and login with hashed passwords
- **💾 Playlist Management**: Save and browse your mood-based playlists
- **🎨 Beautiful UI**: Streamlit-powered web interface with album artwork
- **📈 Data Pipeline**: ETL workflow to populate database with Spotify and Genius data

## 🎯 How It Works

```
1. User enters their mood/feelings in natural language
                    ↓
2. AI (LLM) analyzes the emotional state
                    ↓
3. System determines target music mood
                    ↓
4. Database queries for matching songs
                    ↓
5. Personalized playlist is generated and displayed
```

## 📋 Supported Moods

The system can classify music into the following moods:
- 😊 Happy
- 😢 Sad
- 💕 Romantic
- ⚡ Energetic
- 🧘 Calm
- 😠 Angry
- 🎭 Melancholic
- 💪 Motivational
- 🎉 Party
- 🙏 Devotional
- 😐 Neutral

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Git
- API Keys for:
  - [Spotify Developer](https://developer.spotify.com/)
  - [Genius API](https://genius.com/api-clients)
  - [OpenAI](https://platform.openai.com/) or [Google GenAI](https://ai.google.dev/)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/vermaShivang/PulsePlay-Ai.git
cd PulsePlay-Ai
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Database Setup

```bash
# Create PostgreSQL database
createdb pulseplay_db

# Load schema
psql -U postgres -d pulseplay_db -f schema.sql
```

Or if using a specific user:
```bash
psql -U <your_user> -d pulseplay_db -f schema.sql
```

#### 5. Environment Configuration

Create a `.env` file in the project root:

```env
# PostgreSQL Configuration
POSTGRES_DB=pulseplay_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Spotify API
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

# Genius API
GENIUS_ACCESS_TOKEN=your_genius_token

# LLM Configuration (Choose one)
# For OpenAI:
OPENAI_API_KEY=your_openai_api_key

# For Google Gemini (alternative):
GOOGLE_API_KEY=your_google_api_key

# Optional: Set which LLM to use
# LLM_PROVIDER=openai  # or 'gemini'
```

### Running the Application

```bash
# Activate virtual environment first
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run Streamlit app
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 📊 Project Structure

```
PulsePlay-Ai/
├── app.py                           # Main Streamlit application
├── mood_ai.py                       # AI/LLM engine for mood analysis
├── mood_service.py                  # Service layer for database operations
├── extract_spotify.py               # Spotify API data extraction
├── extract_genius.py                # Genius API lyrics extraction
├── load_to_db.py                    # Load extracted data to PostgreSQL
├── backfill_spotify_metadata.py     # Enhance songs with Spotify metadata
├── main_etl.py                      # ETL pipeline orchestration
├── set_password.py                  # User password management utility
├── forget.py                        # Account deletion/cleanup utility
├── schema.sql                       # PostgreSQL database schema
├── requirements.txt                 # Python dependencies
├── ui.py                            # Alternative UI implementation
├── README.md                        # Project documentation
└── .env                             # Environment variables (create this)
```

## 🔧 Core Components

### 1. **app.py** - Main Application
The Streamlit web interface handling:
- User authentication (signup/login)
- Mood input form
- Playlist generation and display
- Playlist browsing and management
- Navigation sidebar

### 2. **mood_ai.py** - AI Engine
LLM-powered mood classification:
- Analyzes user emotional input
- Classifies songs to mood categories
- Supports OpenAI GPT-4 and Google Gemini
- Returns confidence scores

### 3. **mood_service.py** - Service Layer
Database operations including:
- User management
- Playlist creation and retrieval
- Mood history tracking
- Song filtering by mood

### 4. **ETL Pipeline**
- **extract_spotify.py**: Fetches artist and song data from Spotify
- **extract_genius.py**: Retrieves song lyrics from Genius
- **load_to_db.py**: Loads data into PostgreSQL with error handling
- **backfill_spotify_metadata.py**: Enriches songs with album art and URLs

## 🗄️ Database Schema

### Key Tables

| Table | Purpose |
|-------|---------|
| `users` | User accounts with hashed passwords |
| `artist` | Artist metadata from Spotify |
| `songs` | Song catalog with audio features and lyrics |
| `song_mood` | AI-classified song moods with confidence scores |
| `playlist` | User-created playlists |
| `playlist_song` | Junction table for playlist composition |
| `user_mood` | User mood history |

### Audio Features Tracked
- Danceability, Energy, Valence
- Tempo, Speechiness, Acousticness
- Instrumentalness, Liveness, Loudness
- Key, Mode, Time Signature

See `schema.sql` for complete schema details.

## 🔐 Security

- Passwords are hashed using SHA256
- Environment variables protect sensitive API keys
- PostgreSQL connections use parameterized queries
- User sessions are managed securely in Streamlit

## 📚 API Integration

### Spotify API
- Artist metadata and analytics
- Audio features (acousticness, danceability, energy, etc.)
- Album artwork and preview links

### Genius API
- Song lyrics retrieval
- Artist information

### LLM (OpenAI/Gemini)
- Mood classification for user input
- Song mood categorization
- Confidence scoring

## 🛠️ Utilities

### Set User Password
```bash
python set_password.py
```
Interactive script to set user passwords in the database.

### Delete User Account
```bash
python forget.py
```
Remove user and associated data from the system.

## 📖 Usage Guide

### 1. First Time Setup

```bash
# Run the application
streamlit run app.py

# Navigate to http://localhost:8501
# Sign up with email and password
```

### 2. Generate a Playlist

1. Login to your account
2. Enter your current mood or feelings (e.g., "I'm feeling happy and energetic today")
3. The AI will analyze your mood and recommend music
4. Select number of songs (1-50)
5. Click "Create Playlist"
6. View and interact with your generated playlist

### 3. Browse Playlists

- View all your created playlists on the home page
- Click on any playlist to see full details
- Access Spotify links for preview/listening

### 4. Populate Database with Songs

To add songs to your database:

```bash
# Extract from Spotify
python extract_spotify.py

# Extract lyrics from Genius
python extract_genius.py

# Load to database
python load_to_db.py

# Backfill metadata
python backfill_spotify_metadata.py
```

## ⚙️ Configuration Options

### LLM Provider Selection
In `mood_ai.py`, the system automatically selects based on API keys:
- **OpenAI** (default if `OPENAI_API_KEY` is set)
- **Google Gemini** (if `GOOGLE_API_KEY` is set)

### Customize Mood Categories
Edit the mood list in `mood_ai.py` to add or modify mood categories based on your needs.

### Database Connection
Update `POSTGRES_*` variables in `.env` to connect to your PostgreSQL instance.

## 🐛 Troubleshooting

### Connection Issues

**Error: `psycopg2.OperationalError`**
- Verify PostgreSQL is running
- Check credentials in `.env`
- Ensure database exists: `createdb pulseplay_db`

### API Issues

**Error: `Invalid Spotify credentials`**
- Regenerate API keys from Spotify Developer dashboard
- Update `.env` with new credentials

**Error: `Genius API rate limit`**
- Add delay between requests in `extract_genius.py`
- Consider implementing request caching

### LLM Issues

**Error: `OpenAI API key invalid`**
- Verify key is active at https://platform.openai.com/account/api-keys
- Check for typos in `.env`

**Error: `Gemini API not working`**
- Ensure Google GenAI API is enabled
- Verify `GOOGLE_API_KEY` in `.env`

## 📊 Example Workflow

```python
# User emotion: "I'm feeling really down and need motivation"

# Step 1: AI analysis
mood_analysis = analyze_mood("I'm feeling really down and need motivation")
# Output: {
#   "emotional_state": "sad",
#   "recommended_mood": "motivational",
#   "confidence": 0.92
# }

# Step 2: Query database
songs = get_songs_by_mood("motivational", limit=20)

# Step 3: Create playlist
playlist = create_playlist(user_id=1, mood="motivational", songs=songs)

# Step 4: Display to user
display_playlist(playlist)  # Shows album art, artist, songs
```

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Data from [Spotify API](https://developer.spotify.com/)
- Lyrics from [Genius API](https://genius.com/api-clients)
- AI powered by [OpenAI](https://openai.com/) and [Google GenAI](https://ai.google.dev/)

## 📧 Contact & Support

For issues, questions, or suggestions:
- GitHub Issues: [Create an Issue](https://github.com/vermaShivang/PulsePlay-Ai/issues)
- Author: Shivang Verma
- GitHub: [@vermaShivang](https://github.com/vermaShivang)

## 🚀 Future Enhancements

- [ ] Real-time mood classification during song playback
- [ ] Playlist sharing and collaboration features
- [ ] Advanced analytics dashboard
- [ ] Spotify integration for direct playlist creation
- [ ] Mobile app
- [ ] Social features (friend recommendations, follow users)
- [ ] Mood-based music discovery
- [ ] Custom mood categories per user

---

**Made with ❤️ for music lovers and AI enthusiasts**
