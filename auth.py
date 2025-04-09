import streamlit as st
import hashlib
import os
import json
from pathlib import Path

# File to store user credentials
USERS_FILE = "users.json"

def init_users():
    """Initialize the users file if it doesn't exist"""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Register a new user"""
    init_users()
    
    # Load existing users
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    
    # Check if username already exists
    if username in users:
        return False, "Username already exists"
    
    # Add new user
    users[username] = hash_password(password)
    
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
    if username in users and users[username] == hash_password(password):
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