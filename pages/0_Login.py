import streamlit as st
from auth import login_user, register_user, is_authenticated

# Set page config
st.set_page_config(
    page_title="Login - Industry Dashboard",
    page_icon="🔒",
    layout="centered"
)

# Redirect if already logged in
if is_authenticated():
    st.switch_page("Home.py")

# Title
st.title("🔒 Login to Industry Dashboard")

# Create tabs for login and registration
tab1, tab2 = st.tabs(["Login", "Register"])

# Login tab
with tab1:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            success, message = login_user(username, password)
            if success:
                st.session_state["username"] = username
                st.success(message)
                st.switch_page("Home.py")
            else:
                st.error(message)

# Register tab
with tab2:
    with st.form("register_form"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Register")
        
        if submit:
            if new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                success, message = register_user(new_username, new_password)
                if success:
                    st.success(message)
                else:
                    st.error(message) 