import subprocess
import os

def scrape_twitter(query):
    print(f"[Twitter] Scraping tweets for: {query}")
    safe_name = query.replace(" ", "_").lower()
    output_file = f"output/twitter_data_{safe_name}.json"
    os.makedirs("output", exist_ok=True)

    try:
        result = subprocess.run(
            f"snscrape --jsonl twitter-search \"{query}\"",
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result.stdout)
            print(f"[Twitter] ✅ Data saved to {output_file}")
        else:
            print("[Twitter] ⚠️ No data returned.")
    except Exception as e:
        print(f"[Twitter] ❌ Error: {e}")
