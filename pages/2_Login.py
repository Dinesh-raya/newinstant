import streamlit as st
from utils.supabase import supabase_client
from components.page_layout import apply_page_layout

def login_page():
    apply_page_layout()
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if not email or not password:
                st.error("Please fill in both fields.")
            else:
                try:
                    response = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state["user"] = response.user
                    st.success("Logged in successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    st.page_link("pages/5_Reset_Password.py", label="Forgot Password?")

if __name__ == "__main__":
    login_page()
