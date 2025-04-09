import streamlit as st
from auth import login_user, register_user, is_authenticated, request_password_reset, reset_password

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

# Create tabs for login, registration, and forgot password
tab1, tab2, tab3 = st.tabs(["Login", "Register", "Forgot Password"])

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

# Forgot Password tab
with tab3:
    st.markdown("### Request Password Reset")
    with st.form("forgot_password_form"):
        reset_username = st.text_input("Enter your username")
        submit = st.form_submit_button("Request Reset Token")
        
        if submit:
            success, message = request_password_reset(reset_username)
            if success:
                st.success(message)
                st.info("In a production environment, this token would be sent to your email.")
            else:
                st.error(message)
    
    st.markdown("### Reset Password")
    with st.form("reset_password_form"):
        reset_token = st.text_input("Enter your reset token")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        submit = st.form_submit_button("Reset Password")
        
        if submit:
            if new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                success, message = reset_password(reset_token, new_password)
                if success:
                    st.success(message)
                    st.info("You can now log in with your new password.")
                else:
                    st.error(message) 