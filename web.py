import requests, json, re, os
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # SERP_API_KEY in .env

# ────────────────────────────── helpers ──────────────────────────────
def sanitize_filename(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)

def extract_full_text(url: str) -> str:
    """Grab visible <p> text from a web article."""
    try:
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    except Exception as e:
        return f"❌ Error extracting article: {e}"

# ─────────────────────────── main scraper ────────────────────────────
def scrape_articles_only(query: str, api_key: str, max_pages: int = 2):
    print("🔍 Scraping article links (ignoring videos / social)…")
    all_articles = []

    for page in range(max_pages):
        print(f"📄 Page {page + 1}")
        params = {
            "engine": "google",
            "q": query,
            "hl": "en",
            "gl": "us",
            "api_key": api_key,
            "start": page * 10
        }

        try:
            res = requests.get("https://serpapi.com/search", params=params, timeout=15)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            print("❌ SerpAPI error:", e)
            continue

        for item in data.get("organic_results", []):
            url = item.get("link", "")
            # skip obvious non-article domains
            if any(x in url for x in ["youtube.com", "twitter.com", "facebook.com", "instagram.com", "linkedin.com"]):
                continue

            article = {
                "title":   item.get("title"),
                "link":    url,
                "date":    item.get("date", "N/A"),
                "source":  item.get("source", "Web"),
                "snippet": item.get("snippet", ""),
                "content": extract_full_text(url)
            }
            all_articles.append(article)

    if not all_articles:
        print("⚠️ No articles scraped.")
        return

    # save JSON with Streamlit-friendly prefix
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    fname = f"articles_data_about_{sanitize_filename(query)}_{ts}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=4, ensure_ascii=False)
    print(f"✅ Saved {len(all_articles)} articles to {fname}")

# ────────────────────────── command-line run ─────────────────────────
if __name__ == "__main__":
    key = os.getenv("SERP_API_KEY")
    if not key:
        print("⚠️ SERP_API_KEY missing in environment.")
        quit()

    query  = input("Enter search query: ").strip()
    pages  = input("How many Google pages (10 results each)? [1]: ").strip()
    pages  = int(pages) if pages.isdigit() else 1

    scrape_articles_only(query, key, max_pages=pages)
