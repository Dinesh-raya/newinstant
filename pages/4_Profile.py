import streamlit as st
from utils.supabase import supabase_client
from components.page_layout import apply_page_layout
import os

def profile_page():
    apply_page_layout()
    st.title("User Profile")

    if "user" in st.session_state:
        user = st.session_state["user"]

        # Determine avatar path based on the current theme
        theme = st.session_state.get("theme", "dark")
        avatar_path = f"assets/{theme.capitalize()}/profile.png"

        if os.path.exists(avatar_path):
            st.image(avatar_path, width=150)

        st.write(f"**Email:** {user.email}")

        st.subheader("Change Password")
        with st.form("change_password_form"):
            new_password = st.text_input("New Password", type="password")
            confirm_new_password = st.text_input("Confirm New Password", type="password")
            submitted = st.form_submit_button("Change Password")

            if submitted:
                if not new_password or not confirm_new_password:
                    st.error("Please fill in both password fields.")
                elif new_password != confirm_new_password:
                    st.error("Passwords do not match.")
                elif len(new_password) < 7:
                    st.error("Password must be at least 7 characters long.")
                else:
                    try:
                        supabase_client.auth.update_user({"password": new_password})
                        st.success("Password updated successfully.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
    else:
        st.error("You need to be logged in to view your profile.")

if __name__ == "__main__":
    profile_page()
