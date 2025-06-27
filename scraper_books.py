import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

def find_latest_json_file(folder="."):
    """Find the latest .json file in the folder."""
    json_files = [f for f in os.listdir(folder) if f.endswith(".json")]
    if not json_files:
        return None
    json_files.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
    return json_files[0]

def sanitize_filename(url):
    """Generate a filesystem-safe filename from URL."""
    parsed = urlparse(url)
    base = parsed.netloc.replace('.', '_') + parsed.path.replace('/', '_')
    return base[:100].strip('_')

def extract_article_text(url):
    """Extract readable text from a webpage."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)) or "⚠️ No readable content."
    except Exception as e:
        return f"❌ Error fetching content: {e}"

def scrape_links_from_latest_json():
    """Parse links and download content from the latest JSON file."""
    latest_file = find_latest_json_file()
    if not latest_file:
        print("❌ No .json files found.")
        return

    print(f"📂 Using JSON file: {latest_file}")

    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    links = []

    if isinstance(data, list):  # flat list of dicts
        for item in data:
            if isinstance(item, dict) and "link" in item:
                links.append(item["link"])
    elif isinstance(data, dict):  # fallback for older structure
        if "organic_results" in data:
            links += [res["link"] for res in data["organic_results"] if "link" in res]

    if not links:
        print("⚠️ No links found in JSON.")
        return

    os.makedirs("articles", exist_ok=True)

    for i, url in enumerate(links, 1):
        print(f"🔎 Scraping: {url}")
        content = extract_article_text(url)
        filename = f"articles/article_{i}_{sanitize_filename(url)}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"🔗 URL: {url}\n\n{content}")
        print(f"✅ Saved: {filename}\n{'-'*60}")

if __name__ == "__main__":
    scrape_links_from_latest_json()
