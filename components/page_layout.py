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

    # Define CSS variables for dark and light themes based on design assets
    dark_theme = {
        "--primary-color": "#0B090C",
        "--secondary-color": "#1F1B24",
        "--text-color": "#F2E9F4",
        "--accent-color": "#A01A7D",
        "--border-color": "#3C3546",
        "--sidebar-color": "#1F1B24",
        "--input-bg": "#120E16",
        "--button-bg": "#A01A7D",
        "--button-hover-bg": "#8a176b",
        "--button-text-color": "#ffffff",
        "--header-bg": "#1F1B24",
        "--note-bg": "#120E16",
        "--note-border": "#3C3546",
        "--note-date-color": "#8b949e",
    }

    light_theme = {
        "--primary-color": "#F4F6F3",
        "--secondary-color": "#E0E4DB",
        "--text-color": "#0D160B",
        "--accent-color": "#2E8B57",
        "--border-color": "#C3CAD9",
        "--sidebar-color": "#E0E4DB",
        "--input-bg": "#EDF1E9",
        "--button-bg": "#2E8B57",
        "--button-hover-bg": "#297a4d",
        "--button-text-color": "#ffffff",
        "--header-bg": "#E0E4DB",
        "--note-bg": "#EDF1E9",
        "--note-border": "#C3CAD9",
        "--note-date-color": "#586069",
    }

    # Select theme based on session state
    theme_variables = dark_theme if st.session_state.theme == "dark" else light_theme

    # Create the <style> block
    style_str = "<style>:root {"
    for key, value in theme_variables.items():
        style_str += f"{key}: {value};"
    style_str += "}</style>"

    # Inject the <style> block using st.markdown
    st.markdown(style_str, unsafe_allow_html=True)

    sidebar()
    theme_toggle()
