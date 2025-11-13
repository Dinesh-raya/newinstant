import streamlit as st
from utils.supabase import supabase_client
from components.page_layout import apply_page_layout

def editor_page():
    apply_page_layout()
    st.title("Note Editor")

    if "user" not in st.session_state:
        st.error("You need to be logged in to create or edit notes.")
        return

    note_id = None
    title = ""
    content = ""

    if "current_note" in st.session_state:
        note = st.session_state["current_note"]
        note_id = note["id"]
        title = note["title"]
        content = note["content"]

    with st.form("editor_form"):
        title_input = st.text_input("Title", value=title)
        content_input = st.text_area("Content", value=content, height=300)
        submitted = st.form_submit_button("Save Note")

        if submitted:
            user_id = st.session_state["user"].id
            data = {"title": title_input, "content": content_input, "user_id": user_id}
            try:
                if note_id:
                    supabase_client.table("notes").update(data).eq("id", note_id).execute()
                    st.success("Note updated successfully!")
                else:
                    supabase_client.table("notes").insert(data).execute()
                    st.success("Note created successfully!")

                if "current_note" in st.session_state:
                    del st.session_state["current_note"]
                st.switch_page("app.py")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    editor_page()
