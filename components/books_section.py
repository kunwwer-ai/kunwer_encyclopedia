import streamlit as st
import json
import os
import glob

BOOKS_JSON_PREFIX = "books_data_about_"

def load_latest_json(prefix):
    files = sorted(glob.glob(f"{prefix}*.json"), reverse=True)
    if not files:
        return []
    with open(files[0], "r", encoding="utf-8") as f:
        return json.load(f)

def show_books_section():
    st.header("📚 Books Authored / Featured In")
    books_data = load_latest_json(BOOKS_JSON_PREFIX)

    if books_data:
        for book in books_data:
            with st.expander(book.get("title", "Untitled Book")):
                col1, col2 = st.columns([1, 5])

                # Thumbnail
                with col1:
                    if book.get("thumbnail"):
                        st.image(book["thumbnail"], width=100)
                    else:
                        st.write("📕 No cover")

                # Details
                with col2:
                    st.markdown(f"**✍️ Author:** {book.get('author', 'Unknown')}")
                    st.markdown(f"**📅 Published:** {book.get('published_date', 'N/A')}")

                    # Summary
                    if book.get("summary"):
                        st.write(book["summary"])
                    else:
                        st.info("No summary available.")

                    # External link
                    if book.get("link"):
                        st.markdown(f"[🔗 View Book]({book['link']})", unsafe_allow_html=True)

                    # Local .docx download only
                    if book.get("docx_path"):
                        docx_path = book["docx_path"]
                        if os.path.isfile(docx_path):
                            with open(docx_path, "rb") as f:
                                st.download_button(
                                    label="📄 Download Word File",
                                    data=f,
                                    file_name=os.path.basename(docx_path),
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                        else:
                            st.warning(f"⚠️ File not found at path: `{docx_path}`")
    else:
        st.info("No books found.")
