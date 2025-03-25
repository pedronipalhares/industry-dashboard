import streamlit as st

def init_navigation():
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"

def set_page(page_name):
    st.session_state.page = page_name

def render_navigation():
    st.sidebar.markdown("# Navigation")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.button(
            "📊 Dashboard", 
            type="primary" if st.session_state.page == "Dashboard" else "secondary",
            on_click=set_page, 
            args=("Dashboard",)
        )

    with col2:
        st.button(
            "📥 Download", 
            type="primary" if st.session_state.page == "Download Data" else "secondary",
            on_click=set_page, 
            args=("Download Data",)
        )

    st.sidebar.markdown("---") 