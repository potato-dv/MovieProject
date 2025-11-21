"""
Main Entry Point
Movie & TV Shows Browser Application
Run this file to start the application.
"""
import tkinter as tk
from database.db import create_users_table
from database.user_auth import add_test_user
from ui.login_window import LoginWindow
from ui.movie_app import MovieApp


def main():
    """Main application entry point."""
    # Initialize database and test user
    create_users_table()
    add_test_user()
    
    def on_login_success(username):
        """Callback when login is successful."""
        app_root = tk.Tk()
        MovieApp(app_root, username)
        app_root.mainloop()
    
    # Show login window
    login_root = tk.Tk()
    LoginWindow(login_root, on_login_success)
    login_root.mainloop()


if __name__ == "__main__":
    main()

