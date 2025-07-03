import requests
from bs4 import BeautifulSoup
import json
import time
import os

# Input and output file paths
input_path = "scraped_data/social_data_about_kunwer_linkedin.json"
output_path = "scraped_data/social_data_about_kunwer_linkedin_with_images.json"

# Create folder if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Extract LinkedIn image using Open Graph
def extract_linkedin_image(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        og_image = soup.find("meta", property="og:image")
        return og_image["content"] if og_image else None
    except Exception as e:
        return f"Error: {e}"

# Load LinkedIn JSON
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Process and enrich each post
for idx, post in enumerate(data.get("posts", []), start=1):
    url = post.get("url", "")
    if url:
        print(f"[{idx}] Fetching image for: {url}")
        post["image_url"] = extract_linkedin_image(url)
        time.sleep(1)  # Polite delay to avoid rate limits

# Save enriched data
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Done! File saved at: {output_path}")
