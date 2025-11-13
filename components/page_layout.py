import streamlit as st
from components.sidebar import sidebar, theme_toggle
from utils.load_css import load_css

def apply_page_layout():
    """
    Applies the theme and renders the sidebar on every page.
    """
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"  # Default theme

    st.set_page_config(
        page_title="InstantNote",
        page_icon="🗒️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    load_css("style.css")

    st.markdown(f'<div data-theme="{st.session_state.theme}"></div>', unsafe_allow_html=True)

    sidebar()
    theme_toggle()
