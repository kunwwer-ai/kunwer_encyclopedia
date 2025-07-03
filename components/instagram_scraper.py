import os
import json
import instaloader
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def scrape_instagram(profile_name):
    print(f"[Instagram] Scraping public profile: {profile_name}")
    try:
        os.makedirs("output/instagram", exist_ok=True)
        os.chdir("output/instagram")

        # Set up Instaloader
        loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_comments=False,
            save_metadata=False
        )

        username = os.getenv("INSTA_USERNAME")
        password = os.getenv("INSTA_PASSWORD")

        if not username:
            print("[Instagram] ❌ Username is missing in .env file.")
            return

        # Try loading session from file
        session_loaded = False
        try:
            loader.load_session_from_file(username)
            print(f"[Instagram] ✅ Session loaded for {username}")
            session_loaded = True
        except FileNotFoundError:
            print(f"[Instagram] ⚠️ No session file found for {username}")
        except Exception as e:
            print(f"[Instagram] ⚠️ Session load failed: {e}")

        # If session not loaded, fallback to login
        if not session_loaded:
            if not password:
                print("[Instagram] ❌ Password missing and session not found.")
                return
            print(f"[Instagram] 🔐 Logging in as {username}...")
            loader.login(username, password)
            loader.save_session_to_file()
            print(f"[Instagram] ✅ Session saved for {username}")

        # Load target profile
        profile = instaloader.Profile.from_username(loader.context, profile_name)

        # Scrape posts
        posts_data = []
        for post in profile.get_posts():
            posts_data.append({
                "caption": post.caption or "No caption",
                "image_url": post.url,
                "url": f"https://www.instagram.com/p/{post.shortcode}/",
                "posted_on": post.date_utc.strftime("%Y-%m-%d %H:%M:%S")
            })

        # Save posts to JSON
        with open("instagram_posts.json", "w", encoding="utf-8") as f:
            json.dump(posts_data, f, indent=2, ensure_ascii=False)

        print(f"[Instagram] ✅ {len(posts_data)} posts saved to instagram_posts.json")

    except Exception as e:
        print(f"[Instagram] ❌ Error: {e}")
    finally:
        os.chdir("../../")

# Execute when run as script
if __name__ == "__main__":
    scrape_instagram("kunwersachdev")  # change handle if needed
