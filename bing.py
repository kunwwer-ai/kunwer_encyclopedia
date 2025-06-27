import requests
from bs4 import BeautifulSoup
from newspaper import Article
import os
import time

# 1. Set search query
query = "Kunwer Sachdev"
search_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 2. Get search result URLs
response = requests.get(search_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Bing search results
results = soup.select("li.b_algo h2 a")
urls = [a['href'] for a in results if a.has_attr('href')]

# 3. Folder to save articles
os.makedirs("bing_articles", exist_ok=True)

print(f"🔍 Found {len(urls)} articles. Extracting...")

# 4. Extract content using newspaper3k
for i, url in enumerate(urls):
    try:
        print(f"📄 ({i+1}/{len(urls)}) Fetching: {url}")
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        
        filename = f"bing_articles/article_{i+1}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Title: {article.title}\n")
            f.write(f"URL: {url}\n\n")
            f.write(article.text)
        print(f"✅ Saved: {filename}")
        
        time.sleep(1)  # avoid rate-limiting
    except Exception as e:
        print(f"❌ Error processing {url}: {e}")
