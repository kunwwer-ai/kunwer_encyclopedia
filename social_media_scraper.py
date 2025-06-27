import os
import json
from datetime import datetime

from components.twitter_scraper import scrape_twitter
from components.facebook_scraper import scrape_facebook
from components.instagram_scraper import scrape_instagram
from components.linkedin_scraper import scrape_linkedin
from components.validate_output import validate_file, validate_instagram

OUTPUT_DIR = "output"

def load_json_if_exists(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ Failed to read {path}")
    return []

def extract_instagram_json(folder_path):
    if not os.path.exists(folder_path):
        return []
    results = []
    for file in os.listdir(folder_path):
        if file.endswith(".json.xz"):
            try:
                import lzma
                with lzma.open(os.path.join(folder_path, file), "rt", encoding="utf-8") as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            results.append(data)
                        except:
                            continue
            except Exception as e:
                print(f"⚠️ Failed to extract {file}: {e}")
    return results

def save_combined_social_data(name_slug, data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{OUTPUT_DIR}/social_data_about_{name_slug}_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Combined social media data saved to {filename}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Inputs
    target_name = input("🔎 Enter person's full name: ").strip()
    instagram_username = input("📸 Instagram username: ").strip()
    facebook_page_name = input("📘 Facebook page name: ").strip()
    linkedin_profile_url = input("💼 LinkedIn profile URL: ").strip()
    safe_name = target_name.lower().replace(" ", "_")

    # Scraping
    scrape_twitter(target_name)
    scrape_facebook(facebook_page_name)
    scrape_instagram(instagram_username)
    scrape_linkedin(linkedin_profile_url)

    # Validation
    print("\n✅ Validating scraped data...\n")
    twitter_path = f"{OUTPUT_DIR}/twitter_data_{safe_name}.json"
    facebook_path = f"{OUTPUT_DIR}/facebook_data_{facebook_page_name}.json"
    linkedin_path = f"{OUTPUT_DIR}/linkedin_data.json"
    instagram_folder = f"{OUTPUT_DIR}/instagram/{instagram_username}"

    validate_file(twitter_path, "Twitter")
    validate_file(facebook_path, "Facebook")
    validate_file(linkedin_path, "LinkedIn")
    validate_instagram(instagram_username)

    # Merge all valid data
    combined_data = []

    twitter_data = load_json_if_exists(twitter_path)
    facebook_data = load_json_if_exists(facebook_path)
    linkedin_data = load_json_if_exists(linkedin_path)
    instagram_data = extract_instagram_json(instagram_folder)

    if twitter_data:
        combined_data.extend([{"platform": "Twitter", **x} for x in twitter_data])
    if facebook_data:
        combined_data.extend([{"platform": "Facebook", **x} for x in facebook_data])
    if linkedin_data:
        combined_data.extend([{"platform": "LinkedIn", **x} for x in linkedin_data])
    if instagram_data:
        combined_data.extend([{"platform": "Instagram", **x} for x in instagram_data])

    # Save
    save_combined_social_data(safe_name, combined_data)

if __name__ == "__main__":
    main()
