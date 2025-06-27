import json
import os
from facebook_scraper import get_posts

def scrape_facebook(page_name):
    print(f"[Facebook] Scraping public posts from: {page_name}")
    fb_posts = []
    try:
        for post in get_posts(page_name, pages=3):
            fb_posts.append(post)

        os.makedirs("output", exist_ok=True)
        output_file = f"output/facebook_data_{page_name}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(fb_posts, f, ensure_ascii=False, indent=2)

        print(f"[Facebook] ✅ Data saved to {output_file}\n")
    except Exception as e:
        print(f"[Facebook] ❌ Error: {e}")
