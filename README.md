# 🎵 SoundVault – Music Library

A full-stack CRUD web app to save, search, edit, and manage your personal YouTube music collection. Built with **Flask** + **SQLite** on the backend and vanilla **HTML/CSS/JS** on the frontend.

---

## Features

- ➕ **Add** songs with title, artist, and YouTube URL
- 🔍 **Search** your library by title or artist
- ✏️ **Edit** any song's details via a modal
- 🗑️ **Delete** songs from your library
- ⭐ **Favourite** songs to mark them
- ▶️ **Play** songs inline via the embedded YouTube player

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite (via `sqlite3`) |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Player | YouTube iFrame API |

---

## Project Structure

```
Music-Library/
│
├── app.py              # Flask routes (CRUD API)
├── database.py         # SQLite setup & table creation
├── requirements.txt    # Python dependencies
│
├── templates/
│   └── index.html      # Main UI (SoundVault frontend)
│
├── static/
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic (fetch calls, DOM)
│
└── instance/
    └── music.db        # Auto-created SQLite database
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/adiwadh/Music-Library.git
cd Music-Library
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

Then open your browser at **http://127.0.0.1:5000**

> The `instance/music.db` database is created automatically on first run.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the main HTML page |
| `POST` | `/add_song` | Add a new song |
| `GET` | `/search?q=query` | Search songs by title or artist |
| `GET` | `/library` | Get all songs |
| `GET` | `/favorite/<id>` | Mark a song as favourite |
| `PUT` | `/update/<id>` | Update a song's details |
| `DELETE` | `/delete/<id>` | Delete a song |

---

## Usage

1. Go to the **Add Song** tab → fill in title, artist, and a YouTube URL → click **Add to Library**
2. Go to **Library** to see all your saved songs
3. Click the **✏️ edit** button on any song to update its details
4. Click the **🗑️ delete** button to remove a song
5. Click a song's play button to load it in the embedded player on the right
6. Use the **Search** tab to find songs by name or artist

---

## Notes

- The database file (`instance/music.db`) is excluded from version control via `.gitignore` (recommended)
- The app runs in debug mode by default — disable this before any production deployment by setting `debug=False` in `app.py`
 MADE BY ADITYA WADHAWAN  2401010023