import json
import os
from datetime import datetime
from duckduckgo_search import DDGS
from GoogleNews import GoogleNews
from newspaper import Article           # NEW – for full-text extraction
import requests

# ▸ Optional: SERPAPI key for Bing / Google universal search
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────
def sanitize(text: str) -> str:
    """Make a safe filename segment."""
    return "".join(c if c.isalnum() else "_" for c in text.lower())


def extract_article_content(url: str) -> str:
    """Download & parse the main article text."""
    try:
        art = Article(url)
        art.download()
        art.parse()
        return art.text.strip()
    except Exception as e:
        print(f"⚠️  Content-grab failed for {url[:80]}… – {e}")
        return ""


# ──────────────────────────────────────────────────────────────
# DuckDuckGo News
# ──────────────────────────────────────────────────────────────
def fetch_duckduckgo_news(query: str, max_results: int = 10):
    articles = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.news(query, region="in-en", max_results=max_results):
                link = r.get("url")
                articles.append({
                    "engine":  "DuckDuckGo",
                    "title":   r.get("title", "No Title"),
                    "link":    link,
                    "source":  r.get("source", "Unknown"),
                    "date":    r.get("date", str(datetime.now().date())),
                    "snippet": r.get("body", ""),
                    "content": extract_article_content(link)          # ← NEW
                })
    except Exception as e:
        print(f"❌ DuckDuckGo error: {e}")
    return articles


# ──────────────────────────────────────────────────────────────
# Google News (GoogleNews library)
# ──────────────────────────────────────────────────────────────
def fetch_google_news(query: str, max_results: int = 10):
    gn = GoogleNews(lang="en", region="IN", period="7d")
    gn.search(query)
    results = gn.results(sort=True)
    articles = []
    for r in results[:max_results]:
        link = r.get("link")
        articles.append({
            "engine":  "Google News",
            "title":   r.get("title", "No Title"),
            "link":    link,
            "source":  r.get("media", "Unknown"),
            "date":    r.get("date", str(datetime.now().date())),
            "snippet": r.get("desc", ""),
            "content": extract_article_content(link)                # ← NEW
        })
    return articles


# ──────────────────────────────────────────────────────────────
# Bing News via SerpAPI
# ──────────────────────────────────────────────────────────────
def fetch_bing_news_serpapi(query: str, max_results: int = 10):
    if not SERPAPI_KEY:
        print("⚠️  Skipping Bing – set SERPAPI_KEY env-var to enable")
        return []

    try:
        url = (
            f"https://serpapi.com/search.json?q={query}"
            f"&tbm=nws&api_key={SERPAPI_KEY}&num={max_results}"
        )
        res = requests.get(url, timeout=20).json()
        articles = []
        for r in res.get("news_results", [])[:max_results]:
            link = r.get("link")
            articles.append({
                "engine":  "Bing News (SerpAPI)",
                "title":   r.get("title"),
                "link":    link,
                "source":  r.get("source", "Unknown"),
                "date":    r.get("date", str(datetime.now().date())),
                "snippet": r.get("snippet", ""),
                "content": extract_article_content(link)            # ← NEW
            })
        return articles
    except Exception as e:
        print(f"❌ Bing News error: {e}")
        return []


# ──────────────────────────────────────────────────────────────
# Save results
# ──────────────────────────────────────────────────────────────
def save_results(query: str, articles):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename  = f"news_about_{sanitize(query)}_{timestamp}.json"
    os.makedirs("news_output", exist_ok=True)
    path = os.path.join("news_output", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(articles)} articles → {path}")


# ──────────────────────────────────────────────────────────────
# CLI entry-point
# ──────────────────────────────────────────────────────────────
def run():
    query = input("🔎  Search topic: ").strip()
    if not query:
        print("❗ Enter a search term.")
        return

    count = input("📄  Articles per engine (default 10): ").strip()
    count = int(count) if count.isdigit() else 10

    articles  = []
    articles += fetch_duckduckgo_news(query, count)
    articles += fetch_google_news(query, count)
    articles += fetch_bing_news_serpapi(query, count)

    if articles:
        save_results(query, articles)
    else:
        print("⚠️  No articles found.")


if __name__ == "__main__":
    run()
