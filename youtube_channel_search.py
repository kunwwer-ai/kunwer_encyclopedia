import os
import json
import re
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube_videos(query, max_results=50):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    videos = []

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 50,
        "relevanceLanguage": "hi",       # Optional: focus on Hindi content
        "safeSearch": "strict",          # Optional: filter inappropriate content
        "key": YOUTUBE_API_KEY
    }

    while len(videos) < max_results:
        resp = requests.get(search_url, params=params)
        data = resp.json()

        if "error" in data:
            print(f"❌ API Error: {data['error'].get('message')}")
            break

        for item in data.get("items", []):
            video_id = item["id"].get("videoId")
            if video_id:
                videos.append(video_id)

        if "nextPageToken" in data and len(videos) < max_results:
            params["pageToken"] = data["nextPageToken"]
        else:
            break

    return videos[:max_results]

def fetch_video_details(video_ids, match_title: str = None):
    results = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics",
            "id": ",".join(chunk),
            "key": YOUTUBE_API_KEY
        }
        resp = requests.get(url, params=params)
        data = resp.json()

        for item in data.get("items", []):
            snippet = item["snippet"]
            stats = item.get("statistics", {})
            title = snippet.get("title", "").lower()
            if match_title and match_title.lower() not in title:
                continue  # Skip irrelevant videos

            results.append({
                "video_id": item["id"],
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "published_at": snippet.get("publishedAt"),
                "channel_title": snippet.get("channelTitle"),
                "view_count": stats.get("viewCount"),
                "like_count": stats.get("likeCount"),
                "comment_count": stats.get("commentCount"),
                "video_url": f"https://www.youtube.com/watch?v={item['id']}"
            })
    return results

def main():
    query = input("🔍 Enter search keyword (e.g., Manohar Lal Khattar): ").strip()
    max_videos = input("🎯 Max number of videos to fetch (default 50): ").strip()

    try:
        max_videos = int(max_videos)
    except ValueError:
        print("⚠️ Invalid input. Using default: 50")
        max_videos = 50

    print(f"\n🔎 Searching YouTube for: '{query}'...")
    video_ids = search_youtube_videos(query, max_results=max_videos)
    print(f"✅ Found {len(video_ids)} videos. Now filtering titles...")

    results = fetch_video_details(video_ids, match_title=query)
    print(f"🎯 {len(results)} videos match the title filter: '{query}'")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    safe_query = re.sub(r'[^\w\-_.]', '_', query)
    out_file = f"youtube_data_about_{safe_query}_{timestamp}.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved filtered data to: {out_file}")

if __name__ == "__main__":
    main()
