import streamlit as st
from utils.supabase import supabase_client
from components.page_layout import apply_page_layout

def profile_page():
    apply_page_layout()
    st.title("User Profile")

    if "user" in st.session_state:
        user = st.session_state["user"]
        st.write(f"**Email:** {user.email}")

        # Avatar display and upload
        avatar_url = user.user_metadata.get("avatar_url")
        if avatar_url:
            st.image(avatar_url, width=100)

        new_avatar = st.file_uploader("Upload a new avatar", type=["png", "jpg", "jpeg"])
        if new_avatar:
            try:
                # Upload to Supabase Storage
                file_contents = new_avatar.read()
                file_name = f"{user.id}/avatar/{new_avatar.name}"
                supabase_client.storage.from_("avatars").upload(
                    file=file_contents,
                    path=file_name,
                    file_options={"content-type": new_avatar.type, "upsert": "true"}
                )

                # Get public URL
                public_url = supabase_client.storage.from_("avatars").get_public_url(file_name)

                # Update user metadata
                supabase_client.auth.update_user({"data": {"avatar_url": public_url}})
                st.success("Avatar updated successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Error updating avatar: {e}")

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
