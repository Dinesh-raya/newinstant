import streamlit as st
from utils.supabase import supabase_client
from components.page_layout import apply_page_layout

def register_page():
    apply_page_layout()
    st.title("Register")

    with st.form("register_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            if not email or not password or not confirm_password:
                st.error("Please fill in all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif len(password) < 7:
                st.error("Password must be at least 7 characters long.")
            else:
                try:
                    user = supabase_client.auth.sign_up({"email": email, "password": password})
                    st.success("Registration successful! Please check your email to verify your account.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    register_page()
