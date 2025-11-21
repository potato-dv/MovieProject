import hashlib
import os
from .db import connect_db

def hash_password(password, salt=None):
    """
    Hash a password with a salt using SHA-256.
    If no salt is provided, generate a new one.
    Returns the salt and hashed password as a combined string.
    """
    if salt is None:
        salt = os.urandom(32).hex()  # Generate a random 32-byte salt
    
    # Combine password and salt, then hash
    password_with_salt = (password + salt).encode()
    hashed = hashlib.sha256(password_with_salt).hexdigest()
    
    # Return salt:hash format for storage
    return f"{salt}:{hashed}"

def verify_user(username, password):
    """
    Verify a user's credentials against the database.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        return False
    
    stored_password = result[0]
    
    # Extract salt and hash from stored password
    if ':' in stored_password:
        salt, _ = stored_password.split(':', 1)
        hashed_input = hash_password(password, salt)
        return hashed_input == stored_password
    else:
        # Fallback for old format (if any exist)
        return hashlib.sha256(password.encode()).hexdigest() == stored_password

# Optional: pre-insert a test user
def add_test_user():
    """
    Add a test user (admin/admin123) for demonstration purposes.
    """
    conn = connect_db()
    cursor = conn.cursor()
    test_user = ("admin", hash_password("admin123"))
    try:
        cursor.execute("INSERT INTO users(username,password) VALUES (?,?)", test_user)
        conn.commit()
    except:
        pass  # User already exists
    conn.close()
