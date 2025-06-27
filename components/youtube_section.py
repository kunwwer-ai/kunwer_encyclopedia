import streamlit as st
import glob
import os
import json

def show_youtube_section(load_latest_json):
    st.header("🎥 Video Interviews & Mentions")

    # 🔽 Dropdown to choose specific JSON file
    all_json_files = sorted(glob.glob("youtube_data_about_*.json"), reverse=True)
    selected_file = st.selectbox(
        "Choose a YouTube video dataset:",
        all_json_files,
        format_func=lambda x: os.path.basename(x)
    )

    # 🔄 Load selected file
    if selected_file and os.path.exists(selected_file):
        with open(selected_file, "r", encoding="utf-8") as f:
            youtube_data = json.load(f)
        st.success(f"Loaded data from: `{selected_file}`")
    else:
        st.error("Selected YouTube JSON file not found.")
        return

    if not youtube_data:
        st.info("No YouTube videos available.")
        return

    # 🔍 Filters
    st.subheader("🔎 Filter & Sort Videos")
    search_query = st.text_input("Search by title:", "")
    year_filter = st.selectbox("Filter by year:", ["All"] + sorted(list({v["published_at"][:4] for v in youtube_data})))
    sort_option = st.selectbox("Sort by:", ["Newest", "Oldest", "Most Viewed", "Least Viewed"])
    num_videos = st.selectbox("Number of videos to show:", [10, 20, 50, 100], index=2)

    # 🔍 Apply filters
    filtered = [
        v for v in youtube_data
        if (search_query.lower() in v["title"].lower())
        and (year_filter == "All" or v["published_at"].startswith(year_filter))
    ]

    # 🔃 Sorting
    if sort_option == "Newest":
        filtered = sorted(filtered, key=lambda v: v["published_at"], reverse=True)
    elif sort_option == "Oldest":
        filtered = sorted(filtered, key=lambda v: v["published_at"])
    elif sort_option == "Most Viewed":
        filtered = sorted(filtered, key=lambda v: int(v.get("view_count", 0)), reverse=True)
    elif sort_option == "Least Viewed":
        filtered = sorted(filtered, key=lambda v: int(v.get("view_count", 0)))

    # 🎞 Display videos
    for vid in filtered[:num_videos]:
        with st.expander(vid["title"]):
            st.write(f"**📅 Published on:** {vid['published_at']}")
            st.write(f"**📺 Channel:** {vid['channel_title']}")
            st.write(f"**👁️ Views:** {vid['view_count']} | 👍 {vid['like_count']} | 💬 {vid['comment_count']}")
            st.write(vid["description"])
            st.video(vid["video_url"])
