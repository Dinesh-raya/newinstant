import streamlit as st
from components.page_layout import apply_page_layout
from utils.supabase import supabase_client

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
        notes = []  # Default to empty list

        # --- Data Fetching ---
        try:
            query = supabase_client.table("notes").select("*").eq("user_id", user_id)
            if search_term:
                query = query.or_(f"title.ilike.%{search_term}%,content.ilike.%{search_term}%")
            notes = query.execute().data
        except Exception as e:
            st.error(f"An error occurred while fetching notes: {e}")

        # --- Display Logic ---
        if not notes:
            st.write("You don't have any notes yet. Create one!")
        else:
            for note in notes:
                with st.expander(note["title"]):
                    st.write(note["content"])

                    col1, col2 = st.columns(2)
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
