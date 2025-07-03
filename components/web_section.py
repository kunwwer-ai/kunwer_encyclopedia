# components/web_section.py
import streamlit as st
import json
import os
import glob

def show_web_section():
    st.title("🌐 Web Mentions & Articles")

    folder = "outputs"
    prefix = "web_data_about_"
    files = sorted(glob.glob(os.path.join(folder, f"{prefix}*.json")), reverse=True)

    if not files:
        st.warning("⚠️ No scraped web data found in outputs/.")
        return

    try:
        with open(files[0], "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        st.error(f"❌ Failed to read data: {e}")
        return

    if not isinstance(data, list):
        st.error("❌ Invalid data format. Expected a list of articles.")
        return

    for item in data:
        title = item.get("title") or item.get("link", "Untitled")
        with st.expander(f"🔗 {title}"):
            st.markdown(f"**🔗 Link:** [{item.get('link')}]({item.get('link')})", unsafe_allow_html=True)
            st.markdown(f"**📅 Scraped At:** `{item.get('scraped_at', 'Unknown')}`")
            st.markdown(f"**📰 Source:** `{item.get('source', 'Unknown')}`")
            st.write(item.get("content", "No content found."))
