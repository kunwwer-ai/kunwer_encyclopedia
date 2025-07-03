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
                    # Handle full URL images
                    if image_path.startswith("http"):
                        st.image(image_path, use_container_width=True)
                    else:
                        # Try both direct path and fallback to ./images/
                        possible_paths = [
                            image_path,
                            os.path.join("images", os.path.basename(image_path))
                        ]

                        loaded = False
                        for path in possible_paths:
                            if os.path.exists(path):
                                st.image(path, use_container_width=True)
                                loaded = True
                                break
                        if not loaded:
                            st.caption(f"🖼️ Image not found: `{image_path}`")
