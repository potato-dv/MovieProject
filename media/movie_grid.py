"""
Movie Grid Display Module
Handles the display of movies and TV shows in a grid layout.
"""
import tkinter as tk
import threading
from services.tmdb_api import get_poster_url
from media.image_utils import download_image


class MovieGrid:
    """Handles displaying movies/TV shows in a grid layout."""
    
    def __init__(self, scrollable_frame, canvas, root, show_details_callback):
        """
        Initialize the MovieGrid.
        
        Args:
            scrollable_frame: The frame to display items in
            canvas: The canvas for scrolling
            root: The root window for threading callbacks
            show_details_callback: Function to call when item is clicked
        """
        self.scrollable_frame = scrollable_frame
        self.canvas = canvas
        self.root = root
        self.show_details_callback = show_details_callback
        self.image_references = []
    
    def display_items(self, items, item_type):
        """
        Display movies or TV shows in a grid layout.
        
        Args:
            items: List of items from TMDb API
            item_type: "movie" or "tv"
        
        Returns:
            Number of items displayed
        """
        row = 0
        col = 0
        max_cols = 4
        
        # Track poster labels for background loading
        poster_labels = []
        
        for item in items:
            # Extract title and year
            if item_type == "movie":
                title = item.get("title", "Unknown Title")
                release_date = item.get("release_date", "")
                year = release_date[:4] if release_date else "N/A"
            else:  # TV show
                title = item.get("name", "Unknown Title")
                first_air_date = item.get("first_air_date", "")
                year = first_air_date[:4] if first_air_date else "N/A"
            
            # Get rating and poster URL
            rating = item.get("vote_average", 0)
            poster_url = get_poster_url(item.get("poster_path"))
            display_title = title if len(title) <= 20 else title[:17] + "..."
            
            # Create item frame
            item_frame = tk.Frame(
                self.scrollable_frame,
                bg="#2d2d2d",
                relief=tk.RAISED,
                borderwidth=1
            )
            item_frame.grid(row=row, column=col, padx=10, pady=10, sticky="n")
            
            # Create poster label with placeholder card initially
            poster_label = tk.Label(
                item_frame,
                width=180,
                height=270,
                bg="#e50914",
                cursor="hand2"
            )
            poster_label.pack(padx=5, pady=5)
            
            # Add placeholder content
            placeholder_frame = tk.Frame(poster_label, bg="#e50914")
            placeholder_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            # Rating badge
            rating_frame = tk.Frame(poster_label, bg="#000000")
            rating_frame.place(x=5, y=5)
            tk.Label(
                rating_frame,
                text=f"⭐ {rating:.1f}",
                font=("Arial", 12, "bold"),
                bg="#000000",
                fg="#FFD700",
                padx=8,
                pady=3
            ).pack()
            
            # Title
            tk.Label(
                placeholder_frame,
                text=display_title,
                font=("Arial", 14, "bold"),
                bg="#e50914",
                fg="#ffffff",
                wraplength=160,
                justify=tk.CENTER
            ).pack()
            
            # Year
            year_frame = tk.Frame(poster_label, bg="#000000")
            year_frame.place(relx=0.5, y=250, anchor=tk.CENTER)
            tk.Label(
                year_frame,
                text=year,
                font=("Arial", 10),
                bg="#000000",
                fg="#ffffff",
                padx=8,
                pady=3
            ).pack()
            
            # Make clickable
            item_id = item.get("id")
            for widget in [poster_label, item_frame]:
                widget.bind("<Button-1>", lambda e, i=item_id, t=item_type, d=item: self.show_details_callback(i, t, d))
                widget.bind("<Enter>", lambda e, w=widget: w.config(bg="#444444"))
                widget.bind("<Leave>", lambda e, w=widget: w.config(bg="#2d2d2d"))
            
            # Store for background loading
            poster_labels.append((poster_label, poster_url, item_id, item_type, item))
            
            # Move to next position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Reset canvas scroll to top and force update
        self.canvas.yview_moveto(0)
        self.root.update_idletasks()
        
        # Load actual posters in background
        self._load_posters_async(poster_labels)
        
        return len(items)
    
    def _load_posters_async(self, poster_labels):
        """
        Load posters in background thread.
        
        Args:
            poster_labels: List of tuples (label, url, id, type, data)
        """
        def load_posters():
            for poster_label, poster_url, item_id, item_type, item_data in poster_labels:
                if poster_url:
                    poster_image = download_image(poster_url, width=180, height=270)
                    if poster_image:
                        # Update UI in main thread
                        def update_poster(label=poster_label, img=poster_image, iid=item_id, itype=item_type, idata=item_data):
                            try:
                                if label.winfo_exists():
                                    self.image_references.append(img)
                                    label.config(image=img, bg="#1a1a1a")
                                    # Clear old placeholder widgets
                                    for child in label.winfo_children():
                                        child.destroy()
                                    # Re-bind click event
                                    label.bind("<Button-1>", lambda e: self.show_details_callback(iid, itype, idata))
                            except:
                                pass
                        
                        self.root.after(0, update_poster)
        
        # Start background loading
        threading.Thread(target=load_posters, daemon=True).start()
    
    def clear(self):
        """Clear all displayed items."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.image_references.clear()
