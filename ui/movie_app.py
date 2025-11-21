"""
Movie App Window Module
Main application window for browsing movies and TV shows.
"""
import tkinter as tk
from tkinter import ttk
import threading
from services.tmdb_api import get_popular_movies, get_popular_tv
from media.movie_grid import MovieGrid
from media.details_dialog import DetailsDialog


class MovieApp:
    """Main application class for the Movie & TV Show browser."""
    
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.current_view = "movies"
        self.loading = False
        self.loading_animation_id = None
        
        # Initialize movie grid handler
        self.movie_grid = None
        
        self.setup_ui()
        self.load_movies()
    
    def setup_ui(self):
        """Initialize the user interface."""
        self.root.title("Movies & TV Shows Browser")
        
        # Set fullscreen mode
        self.root.state('zoomed')  # Windows fullscreen
        self.root.configure(bg="#1a1a1a")
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2d2d2d", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"Welcome, {self.username}!",
            font=("Arial", 18, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        ).pack(side=tk.LEFT, padx=20, pady=20)
        
        # Button frame
        button_frame = tk.Frame(header_frame, bg="#2d2d2d")
        button_frame.pack(side=tk.RIGHT, padx=20)
        
        self.movies_btn = tk.Button(
            button_frame,
            text="🎬 Movies",
            font=("Arial", 12, "bold"),
            bg="#e50914",
            fg="white",
            width=12,
            height=2,
            command=self.load_movies,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.movies_btn.pack(side=tk.LEFT, padx=5)
        
        self.tv_btn = tk.Button(
            button_frame,
            text="📺 TV Shows",
            font=("Arial", 12),
            bg="#444444",
            fg="white",
            width=12,
            height=2,
            command=self.load_tv_shows,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.tv_btn.pack(side=tk.LEFT, padx=5)
        
        # Content area with scrollbar
        content_frame = tk.Frame(self.root, bg="#1a1a1a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(content_frame)
        self.canvas = tk.Canvas(content_frame, bg="#1a1a1a", highlightthickness=0)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1a1a1a")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initialize movie grid handler
        self.movie_grid = MovieGrid(self.scrollable_frame, self.canvas, self.root, self.show_details)
        
        # Enable mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Loading movies...",
            font=("Arial", 10),
            bg="#2d2d2d",
            fg="#aaaaaa",
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def clear_content(self):
        """Clear all content from the scrollable frame."""
        if self.movie_grid:
            self.movie_grid.clear()
    
    def update_button_styles(self, active_button):
        """Update button styles to highlight active view."""
        if active_button == "movies":
            self.movies_btn.config(bg="#e50914", font=("Arial", 12, "bold"))
            self.tv_btn.config(bg="#444444", font=("Arial", 12))
        else:
            self.tv_btn.config(bg="#e50914", font=("Arial", 12, "bold"))
            self.movies_btn.config(bg="#444444", font=("Arial", 12))
    
    def load_movies(self):
        """Load and display popular movies."""
        if self.loading:
            return
        
        self.current_view = "movies"
        self.update_button_styles("movies")
        self.clear_content()
        self.show_loading("Loading popular movies")
        
        # Load in background thread
        def fetch_movies():
            movies = get_popular_movies()
            self.root.after(0, lambda: self.on_movies_loaded(movies))
        
        threading.Thread(target=fetch_movies, daemon=True).start()
    
    def on_movies_loaded(self, movies):
        """Callback when movies are loaded."""
        self.hide_loading()
        
        if not movies:
            self.status_label.config(text="Failed to load movies. Check your API key and internet connection.")
            tk.Label(
                self.scrollable_frame,
                text="No movies available. Please check your TMDb API key in config.py",
                font=("Arial", 12),
                bg="#1a1a1a",
                fg="#ffffff"
            ).pack(pady=50)
            return
        
        # Use movie_grid to display items
        count = self.movie_grid.display_items(movies, "movie")
        self.status_label.config(text=f"Showing {count} popular movies - Click any poster for details")
    
    def load_tv_shows(self):
        """Load and display popular TV shows."""
        if self.loading:
            return
        
        self.current_view = "tv"
        self.update_button_styles("tv")
        self.clear_content()
        self.show_loading("Loading popular TV shows")
        
        # Load in background thread
        def fetch_tv():
            tv_shows = get_popular_tv()
            self.root.after(0, lambda: self.on_tv_loaded(tv_shows))
        
        threading.Thread(target=fetch_tv, daemon=True).start()
    
    def on_tv_loaded(self, tv_shows):
        """Callback when TV shows are loaded."""
        self.hide_loading()
        
        if not tv_shows:
            self.status_label.config(text="Failed to load TV shows. Check your API key and internet connection.")
            tk.Label(
                self.scrollable_frame,
                text="No TV shows available. Please check your TMDb API key in config.py",
                font=("Arial", 12),
                bg="#1a1a1a",
                fg="#ffffff"
            ).pack(pady=50)
            return
        
        # Use movie_grid to display items
        count = self.movie_grid.display_items(tv_shows, "tv")
        self.status_label.config(text=f"Showing {count} popular TV shows - Click any poster for details")
    
    def show_loading(self, message="Loading"):
        """Show loading indicator."""
        self.loading = True
        self.clear_content()
        
        # Loading container
        self.loading_frame = tk.Frame(self.scrollable_frame, bg="#1a1a1a")
        self.loading_frame.pack(expand=True, fill=tk.BOTH, pady=100)
        
        # Spinner
        self.loading_label = tk.Label(
            self.loading_frame,
            text=f"⏳ {message}",
            font=("Arial", 16),
            bg="#1a1a1a",
            fg="#ffffff"
        )
        self.loading_label.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.loading_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=20)
        self.progress.start(10)
        
        # Animate loading text
        self.loading_dots = 0
        self.animate_loading()
        
        self.status_label.config(text=f"{message}...")
    
    def animate_loading(self):
        """Animate loading text with dots."""
        if self.loading and hasattr(self, 'loading_label'):
            try:
                if self.loading_label.winfo_exists():
                    base_text = self.loading_label.cget("text").split(".")[0]
                    dots = "." * (self.loading_dots % 4)
                    self.loading_label.config(text=f"{base_text}{dots}")
                    self.loading_dots += 1
                    self.loading_animation_id = self.root.after(400, self.animate_loading)
            except:
                pass
    
    def hide_loading(self):
        """Hide loading indicator."""
        self.loading = False
        if self.loading_animation_id:
            self.root.after_cancel(self.loading_animation_id)
            self.loading_animation_id = None
        if hasattr(self, 'progress'):
            try:
                self.progress.stop()
            except:
                pass
        # Remove the loading frame from the UI
        if hasattr(self, 'loading_frame'):
            try:
                self.loading_frame.destroy()
            except:
                pass
    
    def show_details(self, item_id, item_type, item_data):
        """Show detailed information dialog."""
        DetailsDialog(self.root, item_id, item_type, item_data)
