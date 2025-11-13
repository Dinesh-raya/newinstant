import streamlit as st

def sidebar():
    with st.sidebar:
        st.header("InstantNote")
        if "user" in st.session_state:
            st.page_link("app.py", label="Dashboard")
            st.page_link("pages/3_Editor.py", label="New Note")
            st.page_link("pages/4_Profile.py", label="Profile")
            if st.button("Logout"):
                del st.session_state["user"]
                st.rerun()
        else:
            st.page_link("pages/2_Login.py", label="Login")
            st.page_link("pages/1_Register.py", label="Register")

def theme_toggle():
    with st.sidebar:
        if "theme" not in st.session_state:
            st.session_state.theme = "dark"

        if st.session_state.theme == "dark":
            if st.button("Light Mode"):
                st.session_state.theme = "light"
                st.rerun()
        else:
            if st.button("Dark Mode"):
                st.session_state.theme = "dark"
                st.rerun()
