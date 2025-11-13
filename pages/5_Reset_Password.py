import streamlit as st
from utils.supabase import supabase_client
from components.page_layout import apply_page_layout

def reset_password_page():
    apply_page_layout()
    st.title("Reset Password")

    with st.form("reset_password_form"):
        email = st.text_input("Enter your email address")
        submitted = st.form_submit_button("Send Reset Link")

        if submitted:
            if not email:
                st.error("Please enter your email address.")
            else:
                try:
                    supabase_client.auth.reset_password_email(email)
                    st.success("A password reset link has been sent to your email address.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    reset_password_page()
