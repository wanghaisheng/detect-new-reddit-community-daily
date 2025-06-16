import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import json
import os
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

QUERY = 'site:reddit.com/r/ -site:reddit.com/r/all -site:reddit.com/r/popular -site:reddit.com/r/random -site:reddit.com/r/place'
GOOGLE_SEARCH_URL = "https://www.google.com/search"
RESULTS_DIR = "results"

def fetch_google_results(query, pages=2, delay=2):
    subreddits = []
    for page in range(pages):
        params = {
            "q": query,
            "hl": "en",
            "tbs": "qdr:d",  # results from past 24 hours
            "start": page * 10
        }
        print(f"Fetching page {page + 1}...")
        response = requests.get(GOOGLE_SEARCH_URL, headers=HEADERS, params=params)
        soup = BeautifulSoup(response.text, "html.parser")

        for g in soup.select("div.g"):
            link_tag = g.select_one("a")
            if link_tag:
                url = link_tag["href"]
                parsed = urlparse(url)
                if parsed.path.startswith("/r/") and "reddit.com/r/" in url:
                    subreddits.append({
                        "title": g.select_one("h3").text if g.select_one("h3") else "",
                        "url": url
                    })
        time.sleep(delay)  # respectful delay

    return subreddits

def save_results(results):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    file_path = os.path.join(RESULTS_DIR, f"{date_str}-google.json")
    with open(file_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {len(results)} results to {file_path}")

if __name__ == "__main__":
    results = fetch_google_results(QUERY)
    save_results(results)
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import json
import os
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

QUERY = 'site:reddit.com/r/ -site:reddit.com/r/all -site:reddit.com/r/popular -site:reddit.com/r/random -site:reddit.com/r/place'
GOOGLE_SEARCH_URL = "https://www.google.com/search"
RESULTS_DIR = "results"

def fetch_google_results(query, pages=2, delay=2):
    subreddits = []
    for page in range(pages):
        params = {
            "q": query,
            "hl": "en",
            "tbs": "qdr:d",  # results from past 24 hours
            "start": page * 10
        }
        print(f"Fetching page {page + 1}...")
        response = requests.get(GOOGLE_SEARCH_URL, headers=HEADERS, params=params)
        soup = BeautifulSoup(response.text, "html.parser")

        for g in soup.select("div.g"):
            link_tag = g.select_one("a")
            if link_tag:
                url = link_tag["href"]
                parsed = urlparse(url)
                if parsed.path.startswith("/r/") and "reddit.com/r/" in url:
                    subreddits.append({
                        "title": g.select_one("h3").text if g.select_one("h3") else "",
                        "url": url
                    })
        time.sleep(delay)  # respectful delay

    return subreddits

def save_results(results):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    file_path = os.path.join(RESULTS_DIR, f"{date_str}-google.json")
    with open(file_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {len(results)} results to {file_path}")

if __name__ == "__main__":
    results = fetch_google_results(QUERY)
    save_results(results)
