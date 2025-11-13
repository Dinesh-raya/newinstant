import streamlit as st
from utils.supabase import supabase_client
import time
from components.page_layout import apply_page_layout
from datetime import datetime

def editor_page():
    apply_page_layout()
    st.title("Create or Edit a Note")

    current_note = st.session_state.get("current_note", None)
    existing_attachment = None

    if current_note:
        # Fetch existing attachment if any
        try:
            attachment_response = supabase_client.table("attachments").select("*").eq("note_id", current_note["id"]).limit(1).execute()
            if attachment_response.data:
                existing_attachment = attachment_response.data[0]
        except Exception as e:
            st.warning(f"Could not fetch attachment: {e}")

    with st.form("note_editor_form"):
        title = st.text_input("Title", value=current_note["title"] if current_note else "")
        content = st.text_area("Content (Markdown supported)", value=current_note["content"] if current_note else "", height=300)

        show_preview = st.checkbox("Show Markdown Preview")
        if show_preview:
            st.markdown("---")
            st.markdown(content)
            st.markdown("---")

        tags = st.text_input("Tags (comma-separated)", value=", ".join(current_note["tags"]) if current_note and current_note.get("tags") else "")

        if existing_attachment:
            st.write("Existing Attachment:")
            st.image(existing_attachment["file_url"], width=200)
            if st.form_submit_button("Delete Attachment"):
                try:
                    # Delete from storage and db
                    file_path = existing_attachment["file_url"].split("attachments/")[-1]
                    supabase_client.storage.from_("attachments").remove([file_path])
                    supabase_client.table("attachments").delete().eq("id", existing_attachment["id"]).execute()
                    st.success("Attachment deleted!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting attachment: {e}")

        attachment = st.file_uploader("Upload or Replace Attachment (max 2MB)", type=["png", "jpg", "jpeg"])

        submitted = st.form_submit_button("Save Note")

        if submitted:
            if not title:
                st.error("Please add a title.")
            else:
                user_id = st.session_state["user"].id
                tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]

                db_record = {
                    "user_id": user_id,
                    "title": title,
                    "content": content,
                    "tags": tags_list,
                }

                try:
                    if current_note:
                        db_record["updated_at"] = datetime.now().isoformat()
                        response = supabase_client.table("notes").update(db_record).eq("id", current_note["id"]).execute()
                        note_id = current_note["id"]
                        st.session_state.pop("current_note", None)
                    else:
                        response = supabase_client.table("notes").insert(db_record).execute()
                        note_id = response.data[0]['id']

                    if attachment is not None:
                        if attachment.size > 2 * 1024 * 1024:
                            st.error("File size exceeds 2MB limit.")
                            return

                        # If replacing, delete old attachment first
                        if existing_attachment:
                            file_path = existing_attachment["file_url"].split("attachments/")[-1]
                            supabase_client.storage.from_("attachments").remove([file_path])
                            supabase_client.table("attachments").delete().eq("id", existing_attachment["id"]).execute()

                        file_contents = attachment.read()
                        file_name = f"{user_id}/{note_id}/{attachment.name}"

                        supabase_client.storage.from_("attachments").upload(
                            file=file_contents, path=file_name, file_options={"content-type": attachment.type}
                        )

                        public_url = supabase_client.storage.from_("attachments").get_public_url(file_name)
                        supabase_client.table("attachments").insert({
                            "note_id": note_id, "file_url": public_url
                        }).execute()

                    st.success("Note saved successfully!")
                    time.sleep(1)
                    st.switch_page("app.py")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    if "user" in st.session_state:
        editor_page()
    else:
        st.error("You need to be logged in to access this page.")
        st.stop()
