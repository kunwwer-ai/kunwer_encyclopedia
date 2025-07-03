import streamlit as st
import glob
import os
import json

def show_youtube_section(load_latest_json=None):
    st.header("🎥 Video Interviews & Mentions")

    # 🔽 Load available YouTube datasets
    all_json_files = sorted(glob.glob("youtube_data_about_*.json"), reverse=True)
    if not all_json_files:
        st.warning("⚠️ No YouTube datasets found.")
        return

    selected_file = st.selectbox(
        "Choose a YouTube video dataset:",
        all_json_files,
        format_func=lambda x: os.path.basename(x)
    )

    # 📥 Load selected file
    if selected_file and os.path.exists(selected_file):
        with open(selected_file, "r", encoding="utf-8") as f:
            youtube_data = json.load(f)
        st.success(f"Loaded data from: `{selected_file}`")
    else:
        st.error("❌ Selected YouTube JSON file not found.")
        return

    if not youtube_data:
        st.info("ℹ️ No videos found in this dataset.")
        return

    # 📂 Download option
    with open(selected_file, "rb") as f:
        st.download_button("⬇️ Download this dataset", f, file_name=os.path.basename(selected_file))

    # 🔍 Filters
    st.subheader("🔎 Filter & Sort Videos")
    search_query = st.text_input("Search by title or description:", "")
    
    sort_option = st.selectbox("Sort by:", ["Newest", "Oldest", "Most Viewed", "Least Viewed"])
    num_videos = st.selectbox("Number of videos to show:", [10, 20, 50, 100, "All"], index=2)

    # 🔍 Apply filtering
    filtered = [
        v for v in youtube_data
        if (search_query.lower() in v["title"].lower() or search_query.lower() in v["description"].lower())
        
    ]

    # 🔃 Sorting
    def safe_int(x):
        try: return int(x)
        except: return 0

    if sort_option == "Newest":
        filtered = sorted(filtered, key=lambda v: v.get("published_at", ""), reverse=True)
    elif sort_option == "Oldest":
        filtered = sorted(filtered, key=lambda v: v.get("published_at", ""))
    elif sort_option == "Most Viewed":
        filtered = sorted(filtered, key=lambda v: safe_int(v.get("view_count")), reverse=True)
    elif sort_option == "Least Viewed":
        filtered = sorted(filtered, key=lambda v: safe_int(v.get("view_count")))

    st.markdown(f"🔢 **{len(filtered)} video(s) found** after applying filters.")

    # 🎞 Display results
    show_all = num_videos == "All"
    display_count = len(filtered) if show_all else num_videos

    for vid in filtered[:display_count]:
        with st.expander(vid.get("title", "Untitled Video")):
            st.write(f"**📅 Published on:** {vid.get('published_at', 'N/A')}")
            st.write(f"**📺 Channel:** {vid.get('channel_title', 'Unknown')}")
            st.write(f"**👁️ Views:** {vid.get('view_count', '0')} | 👍 {vid.get('like_count', '0')} | 💬 {vid.get('comment_count', '0')}")
            st.write(vid.get("description", ""))
            st.video(vid["video_url"])
