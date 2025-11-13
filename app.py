import streamlit as st
from components.page_layout import apply_page_layout
from utils.supabase import supabase_client
from datetime import datetime

def main():
    apply_page_layout()

    if supabase_client is None:
        st.error("Supabase client is not initialized. Please check your credentials.")
        return

    if "user" not in st.session_state:
        st.title("Welcome to InstantNote")
        st.write("Please log in or register to continue.")
    else:
        st.title("Your Notes")

        search_term = st.text_input("Search Notes", "")
        user_id = st.session_state["user"].id
        notes = []

        try:
            query = supabase_client.table("notes").select("*").eq("user_id", user_id).order("created_at", desc=True)
            if search_term:
                query = query.or_(f"title.ilike.%{search_term}%,content.ilike.%{search_term}%")
            notes = query.execute().data
        except Exception as e:
            st.error(f"An error occurred while fetching notes: {e}")

        if not notes:
            st.write("You don't have any notes yet. Create one!")
        else:
            for note in notes:
                # Format the date
                date_str = datetime.fromisoformat(note["created_at"]).strftime("%B %d, %Y")

                # Use st.markdown with custom HTML to apply the CSS classes
                note_html = f"""
                <div class="note">
                    <div class="note-title">{note['title']}</div>
                    <div class="note-content">{note['content'][:150] + '...' if len(note['content']) > 150 else note['content']}</div>
                    <div class="note-date">{date_str}</div>
                </div>
                """
                st.markdown(note_html, unsafe_allow_html=True)

                # --- Action Buttons ---
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Edit", key=f"edit_{note['id']}"):
                        st.session_state['current_note'] = note
                        st.switch_page("pages/3_Editor.py")
                with col2:
                    if st.button("Delete", key=f"delete_{note['id']}"):
                        supabase_client.table("notes").delete().eq("id", note["id"]).execute()
                        st.rerun()

if __name__ == "__main__":
    main()
