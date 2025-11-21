"""
Login Window Module
Handles user authentication UI.
"""
import tkinter as tk
from tkinter import messagebox
from database.user_auth import verify_user
from PIL import Image, ImageTk, ImageFilter


class LoginWindow:
    """Login window for user authentication."""
    
    def __init__(self, root, on_success_callback):
        """
        Initialize login window.
        
        Args:
            root: The tkinter root window
            on_success_callback: Function to call with username on successful login
        """
        self.root = root
        self.on_success_callback = on_success_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the login interface."""
        self.root.title("Movies & TV Shows Browser - Login")
        
        # Set fullscreen mode
        self.root.state('zoomed')
        self.root.configure(bg="#000000")
        
        # Load background image
        try:
            bg_image = Image.open("assets/images/moviebg.jpg")
            # Resize to screen size
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            # Darken the image slightly
            bg_image = bg_image.point(lambda p: int(p * 0.6))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            # Background label
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            # Fallback to solid dark background
            self.root.configure(bg="#141414")
        
        # Center login container with semi-transparent black background
        login_container = tk.Frame(self.root, bg="#000000")
        login_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Inner container with padding
        inner_frame = tk.Frame(login_container, bg="#000000")
        inner_frame.pack(padx=60, pady=50)
        
        # MOVIEFLIX logo inside container
        tk.Label(
            inner_frame,
            text="MOVIEFLIX",
            font=("Arial", 36, "bold"),
            bg="#000000",
            fg="#e50914"
        ).pack(pady=(0, 30))
        
        # Sign In title
        tk.Label(
            inner_frame,
            text="Sign In",
            font=("Arial", 28, "bold"),
            bg="#000000",
            fg="#ffffff"
        ).pack(pady=(0, 30))
        
        # Username field
        self.username_entry = tk.Entry(
            inner_frame,
            font=("Arial", 14),
            width=28,
            bg="#333333",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            bd=0
        )
        self.username_entry.insert(0, "Email or phone number")
        self.username_entry.config(fg="#8c8c8c")
        self.username_entry.bind("<FocusIn>", self._on_username_focus_in)
        self.username_entry.bind("<FocusOut>", self._on_username_focus_out)
        self.username_entry.pack(ipady=12, pady=(0, 15))
        
        # Password field
        self.password_entry = tk.Entry(
            inner_frame,
            font=("Arial", 14),
            width=28,
            show="",
            bg="#333333",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            bd=0
        )
        self.password_entry.insert(0, "Password")
        self.password_entry.config(fg="#8c8c8c")
        self.password_entry.bind("<FocusIn>", self._on_password_focus_in)
        self.password_entry.bind("<FocusOut>", self._on_password_focus_out)
        self.password_entry.pack(ipady=12, pady=(0, 25))
        
        # Sign In button (Netflix red)
        sign_in_btn = tk.Button(
            inner_frame,
            text="Sign In",
            font=("Arial", 15, "bold"),
            bg="#e50914",
            fg="white",
            activebackground="#f40612",
            activeforeground="white",
            command=self.login,
            cursor="hand2",
            relief=tk.FLAT,
            bd=0
        )
        sign_in_btn.pack(fill=tk.X, ipady=10, pady=(0, 15))
        
        # Test user info
        tk.Label(
            inner_frame,
            text="Demo: admin / admin123",
            font=("Arial", 9),
            bg="#000000",
            fg="#737373"
        ).pack(pady=(5, 0))
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
    
    def _on_username_focus_in(self, event):
        """Clear placeholder on focus."""
        if self.username_entry.get() == "Email or phone number":
            self.username_entry.delete(0, tk.END)
            self.username_entry.config(fg="#ffffff")
    
    def _on_username_focus_out(self, event):
        """Restore placeholder if empty."""
        if not self.username_entry.get():
            self.username_entry.insert(0, "Email or phone number")
            self.username_entry.config(fg="#8c8c8c")
    
    def _on_password_focus_in(self, event):
        """Clear placeholder and enable password masking on focus."""
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(show="●", fg="#ffffff")
    
    def _on_password_focus_out(self, event):
        """Restore placeholder if empty."""
        if not self.password_entry.get():
            self.password_entry.config(show="")
            self.password_entry.insert(0, "Password")
            self.password_entry.config(fg="#8c8c8c")
    
    def login(self):
        """Handle login button click."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Remove placeholders
        if username == "Email or phone number":
            username = ""
        if password == "Password":
            password = ""
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if verify_user(username, password):
            self.root.destroy()
            self.on_success_callback(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(show="")
            self.password_entry.insert(0, "Password")
            self.password_entry.config(fg="#8c8c8c")
            self.username_entry.focus()
