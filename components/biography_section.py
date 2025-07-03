import streamlit as st
import os

def show_biography_section(bio_data):
    st.header("📖 Biography")

    if not bio_data or "sections" not in bio_data:
        st.warning("⚠️ No biography content found.")
        return

    for section in bio_data["sections"]:
        heading = section.get("heading", section["text"][:80] + "...")

        with st.expander(f"🔹 {heading}"):
            st.markdown(
                f"<h3 style='margin-top:0; color:#2e86de;'>{heading}</h3>",
                unsafe_allow_html=True
            )
            
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(section["text"])

            with col2:
                images = section.get("images", [])
                if not images and "image" in section:
                    images = [section["image"]]

                for image_path in images:
                    if image_path.startswith("http"):
                        st.image(image_path, use_container_width=True)
                    elif os.path.exists(image_path):
                        st.image(image_path, use_container_width=True)
                    else:
                        st.caption(f"🖼️ Image not found: `{image_path}`")
