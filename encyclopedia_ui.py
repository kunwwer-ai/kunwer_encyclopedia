import streamlit as st
import json, os, glob
import pyarrow  # Required for Streamlit custom components

from dashboard_layout import apply_dashboard_layout

# Section Modules
from components.youtube_section import show_youtube_section
from components.books_section import show_books_section
from components.biography_section import show_biography_section
from components.articles_section import show_articles_section
from components.news_section import show_news_section
from components.web_section import show_web_section  # ✅ New section added

# ── Layout and Navigation ───────────────────────────────────────
selected = apply_dashboard_layout()

# ── Load latest JSON from correct folder ────────────────────────
def load_latest_json(prefix: str):
    folder_map = {
        "news_about_": "news_output",
        "articles_data_about_": "",
        "biography_data_about_": "",
        "social_data_about_": "scraped_data",
        "web_data_about_": "outputs"
    }
    folder = folder_map.get(prefix, ".")
    files = sorted(glob.glob(os.path.join(folder, f"{prefix}*.json")), reverse=True)

    # Prefer LinkedIn JSON if exists, else look for "kuwar"/"kunwer", else fallback to latest
    special = next((f for f in files if "linkedin" in f.lower()), None)
    special = special or next((f for f in files if "kuwar" in f.lower() or "kunwer" in f.lower()), None)
    path = special or (files[0] if files else None)

    if path and os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"❌ Failed to load {path}: {e}")
    else:
        st.warning(f"⚠️ No data found for prefix {prefix} in {folder}/.")
    return []

# ── Route by tab ────────────────────────────────────────────────
if selected == "Overview":
    st.markdown("""
        <div style="background-color:#2f80ed;border-radius:10px;padding:20px;color:white;">
            <div style="display:flex;align-items:center;">
                <div style="font-size:36px;font-weight:bold;">Kunwer Sachdev</div>
                <div style="margin-left:20px;">
                    <span style="background:#27ae60;padding:5px 10px;border-radius:6px;">✅ Verified</span>
                    <span style="background:#f2994a;padding:5px 10px;border-radius:6px;margin-left:10px;">Threat: ORANGE</span>
                </div>
            </div>
            <h2 style="margin-top:10px;">Reputation Score: <span style="color:#fff;">82 / 100</span></h2>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-box"><h4>📈 Positive Mentions</h4><h2>25</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><h4>📉 Negative Mentions</h4><h2>2</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h4>📊 Trends</h4><h2>Monthly View</h2></div>', unsafe_allow_html=True)

elif selected == "Biography":
    show_biography_section(load_latest_json("biography_data_about_"))

elif selected == "YouTube":
    show_youtube_section(load_latest_json("social_data_about_"))

elif selected == "Articles":
    show_articles_section(load_latest_json("articles_data_about_"))

elif selected == "Books":
    show_books_section()

elif selected == "News":
    show_news_section(load_latest_json("news_about_"))

elif selected == "Social Media":
    st.markdown("### 🌐 <span style='color:#2e86de;'>Social Media Activity</span>", unsafe_allow_html=True)
    social_data = load_latest_json("social_data_about_")

    if social_data:
        for post in social_data.get("posts", []):
            platform = str(post.get("platform") or "Unknown")
            title = str(post.get("title") or "Untitled")
            content = str(post.get("content") or "No content available.")
            posted_on = post.get("posted_on", "Unknown")
            url = post.get("url")
            image_url = post.get("image_url")

            with st.expander(f"{platform}: {title}"):
                if image_url and image_url.startswith("http"):
                    st.image(image_url, use_container_width=True)
                else:
                    st.info("No image available.")
                st.markdown(f"**📆 Posted on:** {posted_on}")
                st.markdown(content)
                if url:
                    st.markdown(f"[🔗 View Post]({url})")
    else:
        st.info("No social media posts available.")

elif selected == "Web":
    show_web_section()
