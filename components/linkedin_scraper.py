import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin(profile_url):
    print(f"[LinkedIn] Scraping: {profile_url}")
    apify_token = os.getenv("APIFY_TOKEN")

    if not apify_token:
        print("[LinkedIn] Apify token missing in .env file.")
        return

    payload = {
        "profileUrls": [profile_url],
        "locale": "en_US"
    }

    try:
        response = requests.post(
            f"https://api.apify.com/v2/actor-tasks/dunglee~linkedin-profile-scraper/run-sync-get-dataset-items?token={apify_token}",
            json=payload,
        )

        if response.status_code == 200:
            linkedin_data = response.json()
            os.makedirs("output", exist_ok=True)
            with open("output/linkedin.json", "w", encoding="utf-8") as f:
                json.dump(linkedin_data, f, indent=2)
            print("[LinkedIn] Done. Data saved to linkedin.json\n")
        else:
            print(f"[LinkedIn] Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[LinkedIn] Error: {e}")
