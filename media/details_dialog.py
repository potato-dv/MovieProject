"""
Movie/TV Show Details Dialog
Shows detailed information including overview, cast, trailer, etc.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from services.tmdb_api import (
    get_movie_details, get_tv_details, 
    get_movie_videos, get_tv_videos,
    get_youtube_url, get_backdrop_url, get_poster_url
)
from media.image_utils import download_image, get_placeholder_image

class DetailsDialog:
    """Dialog window showing detailed information about a movie or TV show."""
    
    def __init__(self, parent, item_id, item_type, item_data):
        """
        Initialize the details dialog.
        
        Args:
            parent: Parent window
            item_id: TMDb ID of the movie/TV show
            item_type: "movie" or "tv"
            item_data: Basic item data from the listing
        """
        self.item_id = item_id
        self.item_type = item_type
        self.item_data = item_data
        self.image_references = []
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Loading...")
        self.dialog.geometry("800x600")
        self.dialog.configure(bg="#1a1a1a")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_window()
        
        # Show loading screen
        self.show_loading()
        
        # Load details in background
        self.dialog.after(100, self.load_details)
    
    def center_window(self):
        """Center the dialog on screen."""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def show_loading(self):
        """Display loading indicator."""
        self.loading_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        self.loading_frame.pack(fill=tk.BOTH, expand=True)
        
        # Loading spinner (text-based)
        self.loading_label = tk.Label(
            self.loading_frame,
            text="⏳ Loading details...",
            font=("Arial", 16),
            bg="#1a1a1a",
            fg="#ffffff"
        )
        self.loading_label.pack(expand=True)
        
        # Animated dots
        self.loading_dots = 0
        self.animate_loading()
    
    def animate_loading(self):
        """Animate loading text."""
        if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
            dots = "." * (self.loading_dots % 4)
            self.loading_label.config(text=f"⏳ Loading details{dots}")
            self.loading_dots += 1
            self.dialog.after(300, self.animate_loading)
    
    def load_details(self):
        """Load detailed information from TMDb API."""
        try:
            # Fetch details
            if self.item_type == "movie":
                details = get_movie_details(self.item_id)
                videos = get_movie_videos(self.item_id)
            else:
                details = get_tv_details(self.item_id)
                videos = get_tv_videos(self.item_id)
            
            if details:
                self.show_details(details, videos)
            else:
                self.show_error("Failed to load details. Please try again.")
                
        except Exception as e:
            print(f"Error loading details: {e}")
            self.show_error(f"Error: {e}")
    
    def show_error(self, message):
        """Show error message."""
        if hasattr(self, 'loading_frame'):
            self.loading_frame.destroy()
        
        error_label = tk.Label(
            self.dialog,
            text=f"❌ {message}",
            font=("Arial", 12),
            bg="#1a1a1a",
            fg="#ff4444"
        )
        error_label.pack(expand=True)
    
    def show_details(self, details, videos):
        """Display the detailed information."""
        # Remove loading screen
        if hasattr(self, 'loading_frame'):
            self.loading_frame.destroy()
        
        # Update title
        title = details.get('title') if self.item_type == "movie" else details.get('name')
        self.dialog.title(title)
        
        # Create scrollable content
        canvas = tk.Canvas(self.dialog, bg="#1a1a1a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.dialog, orient=tk.VERTICAL, command=canvas.yview)
        content_frame = tk.Frame(canvas, bg="#1a1a1a")
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        
        # Header with backdrop
        backdrop_path = details.get('backdrop_path')
        if backdrop_path:
            backdrop_url = get_backdrop_url(backdrop_path)
            backdrop_img = download_image(backdrop_url, width=780, height=300)
            if backdrop_img:
                self.image_references.append(backdrop_img)
                backdrop_label = tk.Label(content_frame, image=backdrop_img, bg="#1a1a1a")
                backdrop_label.pack(pady=0)
        
        # Info section
        info_frame = tk.Frame(content_frame, bg="#2d2d2d")
        info_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Title
        tk.Label(
            info_frame,
            text=title,
            font=("Arial", 24, "bold"),
            bg="#2d2d2d",
            fg="#ffffff",
            wraplength=700,
            justify=tk.LEFT
        ).pack(anchor=tk.W, padx=15, pady=(15, 5))
        
        # Metadata
        if self.item_type == "movie":
            release_date = details.get('release_date', 'N/A')
            runtime = details.get('runtime', 0)
            runtime_text = f"{runtime} min" if runtime else "N/A"
            metadata = f"📅 {release_date} • ⏱️ {runtime_text}"
        else:
            first_air_date = details.get('first_air_date', 'N/A')
            seasons = details.get('number_of_seasons', 0)
            episodes = details.get('number_of_episodes', 0)
            metadata = f"📅 {first_air_date} • 📺 {seasons} Seasons, {episodes} Episodes"
        
        rating = details.get('vote_average', 0)
        metadata += f" • ⭐ {rating:.1f}/10"
        
        tk.Label(
            info_frame,
            text=metadata,
            font=("Arial", 11),
            bg="#2d2d2d",
            fg="#aaaaaa"
        ).pack(anchor=tk.W, padx=15, pady=(0, 10))
        
        # Genres
        genres = details.get('genres', [])
        if genres:
            genre_text = " | ".join([g['name'] for g in genres[:5]])
            tk.Label(
                info_frame,
                text=genre_text,
                font=("Arial", 10),
                bg="#2d2d2d",
                fg="#e50914"
            ).pack(anchor=tk.W, padx=15, pady=(0, 15))
        
        # Overview
        overview = details.get('overview', 'No overview available.')
        tk.Label(
            info_frame,
            text="Overview",
            font=("Arial", 14, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        ).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        tk.Label(
            info_frame,
            text=overview,
            font=("Arial", 11),
            bg="#2d2d2d",
            fg="#cccccc",
            wraplength=700,
            justify=tk.LEFT
        ).pack(anchor=tk.W, padx=15, pady=(0, 15))
        
        # Trailer section
        if videos:
            # Find official trailer
            trailer = None
            for video in videos:
                if video.get('site') == 'YouTube' and video.get('type') in ['Trailer', 'Teaser']:
                    trailer = video
                    break
            
            if not trailer and videos:
                # Use first available video
                trailer = videos[0]
            
            if trailer:
                tk.Label(
                    info_frame,
                    text="🎬 Trailer",
                    font=("Arial", 14, "bold"),
                    bg="#2d2d2d",
                    fg="#ffffff"
                ).pack(anchor=tk.W, padx=15, pady=(10, 5))
                
                trailer_btn = tk.Button(
                    info_frame,
                    text=f"▶ Watch {trailer.get('name', 'Trailer')}",
                    font=("Arial", 12, "bold"),
                    bg="#e50914",
                    fg="white",
                    cursor="hand2",
                    relief=tk.FLAT,
                    padx=20,
                    pady=10,
                    command=lambda: self.open_trailer(trailer['key'])
                )
                trailer_btn.pack(anchor=tk.W, padx=15, pady=(5, 15))
        
        # Additional info
        additional_frame = tk.Frame(content_frame, bg="#1a1a1a")
        additional_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        if self.item_type == "movie":
            # Budget and revenue
            budget = details.get('budget', 0)
            revenue = details.get('revenue', 0)
            
            if budget > 0:
                self.add_info_row(additional_frame, "Budget", f"${budget:,}")
            if revenue > 0:
                self.add_info_row(additional_frame, "Revenue", f"${revenue:,}")
            
            # Production companies
            companies = details.get('production_companies', [])
            if companies:
                company_names = ", ".join([c['name'] for c in companies[:3]])
                self.add_info_row(additional_frame, "Production", company_names)
        else:
            # TV specific info
            status = details.get('status', 'N/A')
            self.add_info_row(additional_frame, "Status", status)
            
            networks = details.get('networks', [])
            if networks:
                network_names = ", ".join([n['name'] for n in networks])
                self.add_info_row(additional_frame, "Network", network_names)
        
        # Close button
        close_btn = tk.Button(
            content_frame,
            text="Close",
            font=("Arial", 12),
            bg="#444444",
            fg="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.dialog.destroy
        )
        close_btn.pack(pady=20)
    
    def add_info_row(self, parent, label, value):
        """Add an information row."""
        row_frame = tk.Frame(parent, bg="#2d2d2d")
        row_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            row_frame,
            text=f"{label}:",
            font=("Arial", 11, "bold"),
            bg="#2d2d2d",
            fg="#ffffff",
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT, padx=15)
        
        tk.Label(
            row_frame,
            text=value,
            font=("Arial", 11),
            bg="#2d2d2d",
            fg="#cccccc",
            wraplength=600,
            justify=tk.LEFT
        ).pack(side=tk.LEFT, padx=5)
    
    def open_trailer(self, video_key):
        """Open trailer in web browser."""
        try:
            url = get_youtube_url(video_key)
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open trailer: {e}")
