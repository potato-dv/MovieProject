"""
TMDb API Service Module
Handles all interactions with The Movie Database API.
"""
import requests
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TMDB_API_KEY, REQUEST_TIMEOUT

BASE_URL = "https://api.themoviedb.org/3/"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/"

def get_popular_movies(page=1):
    """
    Fetch popular movies from TMDb.
    
    Args:
        page: The page number to fetch (default: 1)
    
    Returns:
        List of movie dictionaries with title, release_date, poster_path, etc.
    """
    url = f"{BASE_URL}movie/popular?api_key={TMDB_API_KEY}&language=en-US&page={page}"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movies: {e}")
        return []

def get_popular_tv(page=1):
    """
    Fetch popular TV shows from TMDb.
    
    Args:
        page: The page number to fetch (default: 1)
    
    Returns:
        List of TV show dictionaries with name, first_air_date, poster_path, etc.
    """
    url = f"{BASE_URL}tv/popular?api_key={TMDB_API_KEY}&language=en-US&page={page}"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TV shows: {e}")
        return []

def get_poster_url(poster_path, size="w500"):
    """
    Build the full URL for a movie/TV show poster.
    
    Args:
        poster_path: The poster path from TMDb API
        size: Image size (w92, w154, w185, w342, w500, w780, original)
    
    Returns:
        Full URL to the poster image, or None if poster_path is None
    """
    if poster_path:
        return f"{IMAGE_BASE_URL}{size}{poster_path}"
    return None

def search_movies(query):
    """
    Search for movies by title.
    
    Args:
        query: The search term
    
    Returns:
        List of movie dictionaries matching the search
    """
    url = f"{BASE_URL}search/movie?api_key={TMDB_API_KEY}&language=en-US&query={query}&page=1"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error searching movies: {e}")
        return []

def search_tv(query):
    """
    Search for TV shows by title.
    
    Args:
        query: The search term
    
    Returns:
        List of TV show dictionaries matching the search
    """
    url = f"{BASE_URL}search/tv?api_key={TMDB_API_KEY}&language=en-US&query={query}&page=1"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error searching TV shows: {e}")
        return []

def get_movie_details(movie_id):
    """
    Get detailed information about a specific movie.
    
    Args:
        movie_id: The TMDb movie ID
    
    Returns:
        Dictionary with movie details including runtime, genres, overview, etc.
    """
    url = f"{BASE_URL}movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie details: {e}")
        return None

def get_tv_details(tv_id):
    """
    Get detailed information about a specific TV show.
    
    Args:
        tv_id: The TMDb TV show ID
    
    Returns:
        Dictionary with TV show details including seasons, genres, overview, etc.
    """
    url = f"{BASE_URL}tv/{tv_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TV show details: {e}")
        return None

def get_movie_videos(movie_id):
    """
    Get videos (trailers, teasers, etc.) for a specific movie.
    
    Args:
        movie_id: The TMDb movie ID
    
    Returns:
        List of video dictionaries with keys, types, and sites
    """
    url = f"{BASE_URL}movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie videos: {e}")
        return []

def get_tv_videos(tv_id):
    """
    Get videos (trailers, teasers, etc.) for a specific TV show.
    
    Args:
        tv_id: The TMDb TV show ID
    
    Returns:
        List of video dictionaries with keys, types, and sites
    """
    url = f"{BASE_URL}tv/{tv_id}/videos?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TV show videos: {e}")
        return []

def get_youtube_url(video_key):
    """
    Build YouTube URL from TMDb video key.
    
    Args:
        video_key: The YouTube video key from TMDb
    
    Returns:
        Full YouTube URL
    """
    return f"https://www.youtube.com/watch?v={video_key}"

def get_backdrop_url(backdrop_path, size="w1280"):
    """
    Build the full URL for a movie/TV show backdrop image.
    
    Args:
        backdrop_path: The backdrop path from TMDb API
        size: Image size (w300, w780, w1280, original)
    
    Returns:
        Full URL to the backdrop image, or None if backdrop_path is None
    """
    if backdrop_path:
        return f"{IMAGE_BASE_URL}{size}{backdrop_path}"
    return None

