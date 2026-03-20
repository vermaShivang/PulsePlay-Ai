-- -- USERS
-- CREATE TABLE IF NOT EXISTS users (
--   user_id SERIAL PRIMARY KEY,
--   name VARCHAR(100) NOT NULL,
--   email VARCHAR(150) UNIQUE NOT NULL,
--   password VARCHAR(100) NOT NULL,
--   created_at TIMESTAMP DEFAULT NOW()
-- );
-- CREATE TABLE IF NOT EXISTS artist (
--   artist_id SERIAL PRIMARY KEY,
--   spotify_artist_id VARCHAR(50) UNIQUE,
--   name VARCHAR(150) NOT NULL,
--   genres JSONB,
--   followers BIGINT,
--   popularity INT,
--   last_updated TIMESTAMP DEFAULT NOW()
-- );

-- -- CREATE TABLE IF NOT EXISTS songs (
-- --   song_id SERIAL PRIMARY KEY,
-- --   title VARCHAR(200),
-- --   artist_id INT REFERENCES artist(artist_id) ON DELETE CASCADE,
-- --   spotify_song_id VARCHAR(50) UNIQUE,
-- --   lyrics TEXT,
-- --   audio_feature JSONB,
-- --   last_updated TIMESTAMP DEFAULT NOW()
-- -- );

-- -- SONGS
-- -- CREATE TABLE IF NOT EXISTS songs (
-- --   song_id SERIAL PRIMARY KEY,
-- --   title VARCHAR(200) NOT NULL,
-- --   artist VARCHAR(150) NOT NULL,
-- --   lyrics TEXT,
-- --   audio_feature JSONB,
-- --   last_updated TIMESTAMP DEFAULT NOW(),
-- --   UNIQUE (title, artist)  -- Prevent duplicate songs by same artist
-- -- );

-- DROP TABLE IF EXISTS songs CASCADE;

-- CREATE TABLE IF NOT EXISTS songs (
--   song_id SERIAL PRIMARY KEY,
--   title VARCHAR(200) NOT NULL,
--   artist_id INT REFERENCES artist(artist_id) ON DELETE CASCADE,
--   spotify_song_id VARCHAR(50) UNIQUE,
--   lyrics TEXT,
--   danceability FLOAT,
--   energy FLOAT,
--   valence FLOAT,
--   tempo FLOAT,
--   speechiness FLOAT,
--   acousticness FLOAT,
--   instrumentalness FLOAT,
--   liveness FLOAT,
--   loudness FLOAT,
--   mode INT,
--   key INT,
--   duration_ms BIGINT,
--   time_signature INT,
--   last_updated TIMESTAMP DEFAULT NOW()
-- );



-- -- SONG MOOD CLASSIFICATIONS
-- CREATE TABLE IF NOT EXISTS song_mood (
--   song_id INT NOT NULL REFERENCES songs(song_id) ON DELETE CASCADE,
--   mood VARCHAR(50) NOT NULL,
--   mood_score FLOAT CHECK (mood_score >= 0 AND mood_score <= 1),
--   classified_at TIMESTAMP DEFAULT NOW(),
--   PRIMARY KEY (song_id, mood)  -- Prevent duplicate mood entries for same song
-- );

-- -- PLAYLISTS
-- CREATE TABLE IF NOT EXISTS playlist (
--   playlist_id SERIAL PRIMARY KEY,
--   user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
--   mood VARCHAR(50),
--   created_at TIMESTAMP DEFAULT NOW(),
--   UNIQUE (user_id, mood, created_at)  -- Optional: avoids multiple identical playlists
-- );

-- -- PLAYLIST-SONG RELATIONSHIP
-- CREATE TABLE IF NOT EXISTS playlist_song (
--   playlist_song_id SERIAL PRIMARY KEY,
--   playlist_id INT NOT NULL REFERENCES playlist(playlist_id) ON DELETE CASCADE,
--   song_id INT NOT NULL REFERENCES songs(song_id) ON DELETE CASCADE,
--   UNIQUE (playlist_id, song_id)  -- Prevent adding same song twice to one playlist
-- );

-- -- USER MOOD HISTORY
-- CREATE TABLE IF NOT EXISTS user_mood (
--   user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
--   mood VARCHAR(50) NOT NULL,
--   mood_score FLOAT CHECK (mood_score >= 0 AND mood_score <= 1),
--   timestamp TIMESTAMP DEFAULT NOW(),
--   PRIMARY KEY (user_id, timestamp)  -- Prevent duplicate timestamps for same user
-- );



-- USERS
CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  password VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- ARTISTS
CREATE TABLE IF NOT EXISTS artist (
  artist_id SERIAL PRIMARY KEY,
  spotify_artist_id VARCHAR(50) UNIQUE,
  name VARCHAR(150) NOT NULL,
  genres JSONB,
  followers BIGINT,
  popularity INT,
  last_updated TIMESTAMP DEFAULT NOW()
);

-- SONGS (flattened audio features)
CREATE TABLE IF NOT EXISTS songs (
  song_id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  artist_id INT REFERENCES artist(artist_id) ON DELETE CASCADE,
  spotify_song_id VARCHAR(50) UNIQUE,
  lyrics TEXT,
  danceability FLOAT,
  energy FLOAT,
  valence FLOAT,
  tempo FLOAT,
  speechiness FLOAT,
  acousticness FLOAT,
  instrumentalness FLOAT,
  liveness FLOAT,
  loudness FLOAT,
  mode INT,
  key INT,
  duration_ms BIGINT,
  time_signature INT,
  album_name VARCHAR(255), --new
  album_image_url TEXT, --new
  spotify_track_url TEXT,--new
   preview_url TEXT, -- new
  last_updated TIMESTAMP DEFAULT NOW()
);

-- SONG MOOD CLASSIFICATIONS
CREATE TABLE IF NOT EXISTS song_mood (
  song_id INT NOT NULL REFERENCES songs(song_id) ON DELETE CASCADE,
  mood VARCHAR(50) NOT NULL,
  mood_score FLOAT CHECK (mood_score >= 0 AND mood_score <= 1),
  classified_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (song_id, mood)
);

-- PLAYLISTS
CREATE TABLE IF NOT EXISTS playlist (
  playlist_id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  mood VARCHAR(50),
  playlist_name VARCHAR(255), --new
  cover_url TEXT, -- new: representative cover image for playlist
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE (user_id, mood, created_at)
);

-- PLAYLIST-SONG RELATIONSHIP
CREATE TABLE IF NOT EXISTS playlist_song (
  playlist_song_id SERIAL PRIMARY KEY,
  playlist_id INT NOT NULL REFERENCES playlist(playlist_id) ON DELETE CASCADE,
  song_id INT NOT NULL REFERENCES songs(song_id) ON DELETE CASCADE,
  UNIQUE (playlist_id, song_id)
);

-- USER MOOD HISTORY
CREATE TABLE IF NOT EXISTS user_mood (
  user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  mood VARCHAR(50) NOT NULL,
  mood_score FLOAT CHECK (mood_score >= 0 AND mood_score <= 1),
  mood_input_text TEXT, --new
  timestamp TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (user_id, timestamp)
);
