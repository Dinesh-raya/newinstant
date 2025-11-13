import streamlit as st
from utils.supabase import supabase_client
from components.page_layout import apply_page_layout

def login_page():
    apply_page_layout()
    st.title("Login")
    st.page_link("pages/5_Reset_Password.py", label="Forgot your password?")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login")

        if submitted:
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                try:
                    response = supabase_client.auth.sign_in_with_password({
                        "email": email,
                        "password": password,
                    })
                    if response:
                        st.session_state["user"] = response.user
                        st.success("Login successful!")
                        st.switch_page("app.py")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    if supabase_client is None:
        st.error("Supabase client is not initialized. Please check your credentials.")
    else:
        login_page()
