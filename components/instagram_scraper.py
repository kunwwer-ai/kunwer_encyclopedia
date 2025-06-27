import os
import instaloader
from dotenv import load_dotenv

load_dotenv()

def scrape_instagram(profile_name):
    print(f"[Instagram] Scraping public profile: {profile_name}")
    try:
        os.makedirs("output/instagram", exist_ok=True)
        os.chdir("output/instagram")

        loader = instaloader.Instaloader(
            download_pictures=True,
            download_videos=False,
            download_comments=False,
            save_metadata=True
        )

        username = os.getenv("INSTA_USERNAME")
        password = os.getenv("INSTA_PASSWORD")

        if not username or not password:
            print("[Instagram] Missing login credentials in .env file.")
        else:
            loader.login(username, password)

        loader.download_profile(profile_name, profile_pic_only=False)
        print("[Instagram] Done. Data saved to output/instagram/\n")
        os.chdir("../../")
    except Exception as e:
        print(f"[Instagram] Error: {e}")
        os.chdir("../../")
