import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from newspaper import Article
import yt_dlp
from datetime import datetime, timedelta
from dotenv import load_dotenv
import textwrap

# ─────────────────────────────────────────────
# Load environment variables from .env
# ─────────────────────────────────────────────
load_dotenv()
SERPAPI_KEY = os.getenv("SERP_API_KEY")

# ─────────────────────────────────────────────
# Helper: Generate date ranges for filters
# ─────────────────────────────────────────────
def generate_date_range(option):
    today = datetime.today()
    if option == "1 Day":
        return [today.strftime("%m/%d/%Y")]
    elif option == "7 Days":
        return [(today - timedelta(days=i)).strftime("%m/%d/%Y") for i in range(7)]
    elif option == "1 Month":
        return [(today - timedelta(days=i)).strftime("%m/%d/%Y") for i in range(30)]
    elif option == "3 Months":
        return [(today - timedelta(days=i)).strftime("%m/%d/%Y") for i in range(90)]
    elif option == "6 Months":
        return [(today - timedelta(days=i)).strftime("%m/%d/%Y") for i in range(180)]
    return []

# ─────────────────────────────────────────────
# Google Search via SerpAPI
# ─────────────────────────────────────────────
def search_google_serpapi(query, mode="web", limit=10, date_filter=None):
    if not SERPAPI_KEY:
        st.warning("🔐 SERPAPI_KEY not found.")
        return []

    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": limit
    }

    if mode == "news":
        params["tbm"] = "n"

    if date_filter:
        params["tbs"] = f"cdr:1,cd_min:{date_filter},cd_max:{date_filter}"

    try:
        res = requests.get("https://serpapi.com/search", params=params)
        data = res.json()
        key = "news_results" if mode == "news" else "organic_results"
        return [r.get("link") for r in data.get(key, []) if r.get("link")]
    except Exception as e:
        st.error(f"SerpAPI search failed: {e}")
        return []

# ─────────────────────────────────────────────
# Scraping Functions
# ─────────────────────────────────────────────
def extract_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            "kind": "article",
            "title": article.title,
            "authors": ", ".join(article.authors),
            "date": article.publish_date,
            "text": textwrap.shorten(article.text, 1000),
            "fulltext": article.text
        }
    except:
        return {"kind": "link", "title": url, "text": "Failed to parse."}

def extract_video(url):
    try:
        with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
            info = ydl.extract_info(url, download=False)
        return {
            "kind": "video",
            "title": info.get("title"),
            "channel": info.get("uploader"),
            "duration": info.get("duration"),
            "embed": url
        }
    except:
        return {"kind": "link", "title": url, "text": "Failed to parse video."}

# ─────────────────────────────────────────────
# Streamlit UI
# ─────────────────────────────────────────────
def show_realtime_scraper():
    st.markdown("# ⚡ Real-Time Content Scraper")
    query = st.text_input("🔍 Enter a person, topic, or brand name", "Kunwer Sachdev")

    st.markdown("### 🎯 What content would you like to fetch?")
    col1, col2 = st.columns(2)
    with col1:
        opt_news = st.checkbox("📰 News Articles")
        opt_web = st.checkbox("🌐 Web Results")
    with col2:
        opt_youtube = st.checkbox("📺 YouTube Videos")
        st.checkbox("🖼️ Images (coming soon)", disabled=True)

    date_range_option = st.selectbox("📅 Select Date Range", ["1 Day", "7 Days", "1 Month", "3 Months", "6 Months"])

    if st.button("🚀 Fetch"):
        if not query.strip():
            st.warning("Please enter a topic or name.")
            return

        st.info("⏳ Fetching content. Please wait...")
        dates = generate_date_range(date_range_option)
        urls = set()

        for date_str in dates:
            if opt_news:
                urls.update(search_google_serpapi(query, mode="news", date_filter=date_str, limit=10))
            if opt_web:
                urls.update(search_google_serpapi(query, mode="web", date_filter=date_str, limit=10))

        urls = list(urls)
        results = []

        for url in urls:
            if "youtube.com" in url or "youtu.be" in url:
                if opt_youtube:
                    results.append(extract_video(url))
            elif opt_news or opt_web:
                results.append(extract_article(url))

        if not results:
            st.warning("⚠️ No content found.")
            return

        for result in results:
            with st.expander(result.get("title", "Untitled")):
                if result["kind"] == "video":
                    st.video(result["embed"])
                    st.markdown(f"**Channel:** {result['channel']}")
                    st.markdown(f"**Duration:** {result['duration']} seconds")
                else:
                    if result.get("authors"):
                        st.caption(f"✍️ {result['authors']}")
                    if result.get("date"):
                        st.caption(f"🗓️ {result['date']}")
                    st.write(result.get("text", ""))

# ─────────────────────────────────────────────
# Run in Streamlit
# ─────────────────────────────────────────────
if __name__ == "__main__":
    show_realtime_scraper()
