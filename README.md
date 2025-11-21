# 🎬 Movies & TV Shows Browser

A Python Tkinter desktop application that allows users to browse popular movies and TV shows using The Movie Database (TMDb) API. Features a secure login system with SQLite database and password hashing.

## 📋 Project Overview

This application was created as a school project and demonstrates:

- **Secure User Authentication**: SQLite database with salted and hashed passwords
- **API Integration**: Real-time data from TMDb API
- **GUI Development**: Clean and modern Tkinter interface
- **Image Processing**: Dynamic poster loading with Pillow
- **Modular Code Structure**: Well-organized and maintainable codebase

## ✨ Features

- 🔐 **Secure Login System**

  - Username/password authentication
  - SHA-256 password hashing with salt
  - SQLite database for user storage
  - Pre-configured test account (admin/admin123)

- 🎥 **Movie & TV Show Browser**

  - View popular movies and TV shows
  - Display poster images, titles, release years, and ratings
  - Scrollable gallery layout
  - Real-time data from TMDb API
  - **Click any poster to see detailed information**

- 📽️ **Interactive Details & Trailers**

  - Click movie/TV show posters for full details
  - View overview, runtime, release date, genres
  - Watch official trailers on YouTube
  - See budget, revenue, production info
  - Beautiful backdrop images

- 🎨 **Modern UI with Loading Indicators**
  - Clean, dark-themed interface
  - Responsive grid layout
  - Smooth scrolling
  - Visual feedback for active selections
  - **Animated loading screens** so users don't get frustrated
  - **Progress bars** during data fetching
  - **Hover effects** on clickable elements

## 🚀 Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Internet connection (for API calls and poster downloads)

### Step 1: Install Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:

- `requests` - For API calls
- `Pillow` - For image processing

### Step 2: Get Your TMDb API Key

1. Go to [The Movie Database](https://www.themoviedb.org/)
2. Create a free account
3. Navigate to Settings → API
4. Request an API key (choose "Developer" option)
5. Copy your API key

### Step 3: Configure the API Key

**Option 1: Using config.py (Recommended)**

Open `config.py` and replace the placeholder with your actual API key:

```python
# Line 11 in config.py
TMDB_API_KEY = "YOUR_TMDB_API_KEY_HERE"  # Replace this with your actual key
```

**Example:**

```python
TMDB_API_KEY = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
```

**Option 2: Direct configuration**

Alternatively, you can edit `services/tmdb_api.py` directly (though config.py is cleaner).

### Step 4: Run the Application

Run the login script:

```bash
python login.py
```

## 🔑 Default Login Credentials

For testing purposes, a default user is created automatically:

- **Username**: `admin`
- **Password**: `admin123`

## 📁 Project Structure

```
MovieProject/
│
├── login.py                 # Login window entry point
├── main.py                  # Main application window
├── config.py               # Configuration file (API key here!)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── QUICK_START.txt         # Quick reference guide
├── check_setup.py          # Setup verification script
├── manage_users.py         # User management utility
│
├── database/               # Database module
│   ├── __init__.py
│   ├── db.py              # Database connection
│   └── user_auth.py       # Authentication logic
│
├── services/              # External services
│   └── tmdb_api.py       # TMDb API integration
│
├── media/                 # Media handling
│   ├── __init__.py
│   ├── movies.py         # Movie/TV data processing
│   └── image_utils.py    # Image download and processing
│
└── assets/               # Static assets
    └── images/
        ├── icons/
        └── posters/      # Cached poster images
```

## 🔒 Security Features

### Password Hashing

The application uses **SHA-256** hashing with a unique salt for each password:

- **Salt**: Random 32-byte hex string generated for each user
- **Hash Algorithm**: SHA-256
- **Storage Format**: `salt:hash` in the database

### Password Storage Flow

1. User enters password
2. System generates random salt
3. Password + salt is hashed with SHA-256
4. `salt:hash` is stored in database
5. Never stores plain-text passwords

### Password Verification Flow

1. User enters credentials
2. System retrieves stored `salt:hash` from database
3. Entered password is hashed with the stored salt
4. Hashes are compared for authentication

## 🎯 How to Use

1. **Login**

   - Run `python login.py`
   - Enter username and password
   - Click "Login"

2. **Browse Movies**

   - Click the "🎬 Movies" button
   - Scroll through popular movies
   - View posters, titles, years, and ratings
   - **Click any poster to see full details and trailer**

3. **Browse TV Shows**

   - Click the "📺 TV Shows" button
   - Scroll through popular TV shows
   - View posters, titles, years, and ratings
   - **Click any poster to see full details and trailer**

4. **View Details & Trailers**
   - Click on any movie or TV show poster
   - View detailed information including:
     - Overview and synopsis
     - Release date and runtime
     - Genres and ratings
     - Budget and revenue (for movies)
     - Number of seasons/episodes (for TV)
   - Click "▶ Watch Trailer" to view on YouTube
   - Close the dialog to return to browsing

## 🛠️ Customization

### Changing Poster Size

In `media/image_utils.py`, modify the `download_image()` function:

```python
def download_image(url, width=180, height=270):  # Adjust these values
```

### Changing Grid Layout

In `main.py`, modify the `max_cols` variable in `display_items()`:

```python
max_cols = 4  # Change to 3, 5, etc.
```

### Adding More Pages of Results

In `main.py`, modify the API calls to fetch multiple pages:

```python
movies_page1 = get_popular_movies(page=1)
movies_page2 = get_popular_movies(page=2)
all_movies = movies_page1 + movies_page2
```

## 🐛 Troubleshooting

### "Failed to load movies"

- Check your internet connection
- Verify your TMDb API key is correct in `config.py`
- Ensure the API key is active (newly created keys may take a few minutes)
- Run `python check_setup.py` to verify your configuration

### "No module named 'PIL'"

- Install Pillow: `pip install Pillow`

### "No module named 'requests'"

- Install requests: `pip install requests`

### Database Issues

- Delete `users.db` and restart the application to recreate the database
- Or run `python manage_users.py` to manage users

### Images Not Loading

- Check internet connection
- Some movies/shows may not have poster images available

### Quick Setup Check

Run the setup checker to verify everything:

```bash
python check_setup.py
```

## 📚 Learning Resources

- [TMDb API Documentation](https://developers.themoviedb.org/3)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [Hashlib Documentation](https://docs.python.org/3/library/hashlib.html)

## 📝 Code Quality

This project follows Python best practices:

- ✅ Modular code structure
- ✅ Comprehensive docstrings
- ✅ Error handling
- ✅ Clean and readable code
- ✅ Proper separation of concerns

## 🎓 School Project Notes

This application demonstrates:

- **Database Management**: SQLite for persistent user storage
- **Security**: Password hashing and salting
- **API Integration**: RESTful API consumption
- **GUI Development**: Event-driven programming
- **Image Processing**: Dynamic content loading
- **Error Handling**: Graceful failure management

## 📄 License

This project is created for educational purposes. TMDb API data is provided by The Movie Database and subject to their terms of use.

## 🙏 Acknowledgments

- [The Movie Database (TMDb)](https://www.themoviedb.org/) for the API
- Python community for excellent libraries

---

**Created by**: Lauris  
**Date**: November 2025  
**Purpose**: School Project
