from duckduckgo_search import ddg
from newspaper import Article
import os

query = "Kunwer Sachdev"
num_results = 20
os.makedirs("bing_articles/full_data", exist_ok=True)

print("🔍 Searching links...")
results = ddg(query, max_results=num_results) or []

if not results:
    print("⚠️ No results found.")
else:
    for i, result in enumerate(results):
        url = result.get("href") or result.get("url")
        if not url:
            continue

        try:
            print(f"📄 Fetching: {url}")
            article = Article(url)
            article.download()
            article.parse()

            with open(f"bing_articles/full_data/article_{i + 1}.txt", "w", encoding="utf-8") as f:
                f.write(f"Title: {article.title}\n")
                f.write(f"URL: {url}\n\n")
                f.write(article.text)
            print(f"✅ Saved article_{i + 1}.txt")
        except Exception as e:
            print(f"❌ Failed to fetch {url}: {e}")
