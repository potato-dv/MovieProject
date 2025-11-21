# 🎬 Movies & TV Shows Browser

A Python Tkinter desktop application that allows users to browse popular movies and TV shows using The Movie Database (TMDb) API. Features a secure login system with SQLite database and password hashing.

## 📋 Project Overview

This application was created as a school project and demonstrates:

- **Secure User Authentication**: SQLite database with salted and hashed passwords
- **API Integration**: Real-time data from TMDb API
- **GUI Development**: Clean and modern Tkinter interface
- **Image Processing**: Dynamic poster loading with Pillow
- **Modular Code Structure**: Well-organized and maintainable codebase

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
TMDB_API_KEY = "sheesh1234"
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

   - Run `python main.py`
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



## 📄 License

This project is created for educational purposes. TMDb API data is provided by The Movie Database and subject to their terms of use.

## Acknowledgments

- [The Movie Database (TMDb)](https://www.themoviedb.org/) for the API
- Python community for excellent libraries

---
