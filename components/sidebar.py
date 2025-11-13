import streamlit as st

def sidebar():
    st.sidebar.title("InstantNote")

    st.sidebar.page_link("app.py", label="Home")

    if "user" in st.session_state:
        st.sidebar.page_link("pages/3_Editor.py", label="New Note")
        st.sidebar.page_link("pages/4_Profile.py", label="Profile")

        if st.sidebar.button("Logout"):
            del st.session_state["user"]
            st.switch_page("app.py")
    else:
        st.sidebar.page_link("pages/2_Login.py", label="Login")
        st.sidebar.page_link("pages/1_Register.py", label="Register")

def theme_toggle():
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    if st.sidebar.toggle("Light Mode", value=(st.session_state.theme == "light")):
        st.session_state.theme = "light"
    else:
        st.session_state.theme = "dark"
