import os, re, json, asyncio
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import requests
import sys
from urllib.parse import urljoin

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

# ────────────── Helpers ──────────────
def sanitize_filename(name): return re.sub(r"[^a-zA-Z0-9_-]", "_", name)

def extract_text_from_url(url, retries=2):
    for _ in range(retries):
        try:
            res = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            return "\n\n".join(p.get_text(strip=True) for p in soup.find_all("p"))
        except Exception:
            continue
    return "❌ Error extracting content"

# ────────────── Google (SerpAPI) ──────────────
def scrape_google_serpapi(query, max_pages):
    print(f"🔍 Google (SerpAPI): {query}")
    articles = []
    for page in range(max_pages):
        params = {
            "engine": "google", "q": query,
            "hl": "en", "gl": "us",
            "api_key": SERP_API_KEY,
            "start": page * 10
        }
        try:
            res = requests.get("https://serpapi.com/search", params=params)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            print(f"❌ Google SerpAPI error:", e)
            continue

        for item in data.get("organic_results", []):
            link = item.get("link", "")
            if not link or any(x in link for x in ["youtube", "facebook", "linkedin", "twitter"]): continue
            articles.append({
                "query": query,
                "title": item.get("title"),
                "link": link,
                "source": "Google",
                "snippet": item.get("snippet", ""),
                "date": item.get("date", "N/A"),
                "content": extract_text_from_url(link)
            })
    return articles

# ────────────── Playwright Engines ──────────────
async def scrape_engine(playwright, query, engine_name, base_url, search_path, result_selector, pages=1):
    print(f"🔍 {engine_name}: {query}")
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    articles = []

    try:
        for page_num in range(pages):
            full_url = base_url + search_path.format(query=query, start=page_num * 10)
            await page.goto(full_url, timeout=20000)
            await page.wait_for_timeout(3000)

            links = await page.query_selector_all(result_selector)
            for link in links:
                href = await link.get_attribute("href")
                title = await link.inner_text()
                if not href or not title:
                    continue
                full_url = href if href.startswith("http") else urljoin(base_url, href)
                if any(x in full_url for x in ["youtube", "facebook", "linkedin", "twitter"]): continue

                articles.append({
                    "query": query,
                    "title": title.strip(),
                    "link": full_url,
                    "source": engine_name,
                    "snippet": "",
                    "date": "N/A",
                    "content": extract_text_from_url(full_url)
                })
    except Exception as e:
        print(f"❌ {engine_name} error:", e)

    await browser.close()
    return articles

# ────────────── Scraper Core ──────────────
async def scrape_all_engines(query, pages):
    results = []
    if SERP_API_KEY:
        results += scrape_google_serpapi(query, pages)

    async with async_playwright() as pw:
        tasks = [
            scrape_engine(pw, query, "DuckDuckGo", "https://html.duckduckgo.com", "/html/?q={query}&s={start}", ".result__url", pages),
            scrape_engine(pw, query, "Mojeek", "https://www.mojeek.com", "/search?q={query}&s={start}", ".result > h2 > a", pages),
            scrape_engine(pw, query, "Brave", "https://search.brave.com", "/search?q={query}&offset={start}", "a.result-title", pages)
        ]
        engine_results = await asyncio.gather(*tasks)
        for res in engine_results:
            results.extend(res)

    return results

# ────────────── Main ──────────────
async def main():
    print("📰 Multi-Search Engine Article Scraper (Combined Output)")

    # Accept comma-separated input or CLI
    input_names = " ".join(sys.argv[1:]).strip()
    if not input_names:
        input_names = input("👥 Enter comma-separated names to search: ")

    query_list = [q.strip() for q in input_names.split(",") if q.strip()]
    if not query_list:
        print("❌ No valid queries provided.")
        return

    pages = input("📄 Pages per engine per user (default 10): ").strip()
    pages = int(pages) if pages.isdigit() else 10

    os.makedirs("outputs", exist_ok=True)
    all_results = []

    for query in query_list:
        print(f"\n🔎 Scraping for: {query}")
        query_results = await scrape_all_engines(query, pages)
        all_results.extend(query_results)

    # Deduplicate
    seen_links = set()
    unique_results = []
    for item in all_results:
        if item["link"] not in seen_links:
            seen_links.add(item["link"])
            unique_results.append(item)

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"outputs/web_data_combined_{ts}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(unique_results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Scraping complete.")
    print(f"📁 Combined file saved: {filename}")
    print(f"🔗 Total unique results: {len(unique_results)}")

if __name__ == "__main__":
    asyncio.run(main())
