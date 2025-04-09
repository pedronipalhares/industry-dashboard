import streamlit as st
import hashlib
import os
import json
from pathlib import Path
import secrets
import string
import re

# File to store user credentials
USERS_FILE = "users.json"
# File to store reset tokens
RESET_TOKENS_FILE = "reset_tokens.json"

def init_users():
    """Initialize the users file if it doesn't exist"""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
            
def init_reset_tokens():
    """Initialize the reset tokens file if it doesn't exist"""
    if not os.path.exists(RESET_TOKENS_FILE):
        with open(RESET_TOKENS_FILE, "w") as f:
            json.dump({}, f)

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    """Check if the email format is valid"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def register_user(username, email, password):
    """Register a new user"""
    init_users()
    
    # Validate email
    if not is_valid_email(email):
        return False, "Invalid email format"
    
    # Load existing users
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    
    # Check if username already exists
    if username in users:
        return False, "Username already exists"
    
    # Check if email already exists
    for user_data in users.values():
        if isinstance(user_data, dict) and user_data.get('email') == email:
            return False, "Email already registered"
    
    # Add new user with email
    users[username] = {
        'password': hash_password(password),
        'email': email
    }
    
    # Save updated users
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)
    
    return True, "User registered successfully"

def login_user(username, password):
    """Login a user"""
    init_users()
    
    # Load users
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    
    # Check if username exists and password is correct
    if username in users:
        user_data = users[username]
        # Handle both old format (just password) and new format (dict with password and email)
        stored_password = user_data['password'] if isinstance(user_data, dict) else user_data
        if stored_password == hash_password(password):
            return True, "Login successful"
    
    return False, "Invalid username or password"

def logout_user():
    """Logout the current user"""
    if "username" in st.session_state:
        del st.session_state["username"]
        st.experimental_rerun()

def is_authenticated():
    """Check if the user is authenticated"""
    return "username" in st.session_state

def require_auth():
    """Decorator to require authentication for a page"""
    if not is_authenticated():
        st.error("You must be logged in to access this page")
        st.stop()

def generate_reset_token():
    """Generate a random reset token"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def request_password_reset(email):
    """Request a password reset for a user by email"""
    init_users()
    init_reset_tokens()
    
    # Load users
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    
    # Find username by email
    username = None
    for uname, user_data in users.items():
        if isinstance(user_data, dict) and user_data.get('email') == email:
            username = uname
            break
    
    if not username:
        # Don't reveal if email exists or not for security
        return True, "If your email is registered, you will receive a password reset link."
    
    # Generate reset token
    token = generate_reset_token()
    
    # Load existing tokens
    with open(RESET_TOKENS_FILE, "r") as f:
        tokens = json.load(f)
    
    # Add token with username
    tokens[token] = username
    
    # Save updated tokens
    with open(RESET_TOKENS_FILE, "w") as f:
        json.dump(tokens, f)
    
    # In a real application, you would send this token via email
    # For this demo, we'll just return it
    return True, f"Password reset token: {token}"

def reset_password(token, new_password):
    """Reset a user's password using a token"""
    init_reset_tokens()
    init_users()
    
    # Load tokens
    with open(RESET_TOKENS_FILE, "r") as f:
        tokens = json.load(f)
    
    # Check if token exists
    if token not in tokens:
        return False, "Invalid or expired token"
    
    # Get username from token
    username = tokens[token]
    
    # Load users
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    
    # Update password
    if isinstance(users[username], dict):
        users[username]['password'] = hash_password(new_password)
    else:
        # Handle old format
        users[username] = {
            'password': hash_password(new_password),
            'email': ''  # Default empty email for old accounts
        }
    
    # Save updated users
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)
    
    # Remove used token
    del tokens[token]
    
    # Save updated tokens
    with open(RESET_TOKENS_FILE, "w") as f:
        json.dump(tokens, f)
    
    return True, "Password reset successful" 