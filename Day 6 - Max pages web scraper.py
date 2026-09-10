import csv
import random
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"
current_path = "/page/1/"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36"
})

all_records = []

print("Starting multi-page crawl...")

while current_path:
    target_url = urljoin(BASE_URL, current_path)
    print(f"Crawling: {target_url}")

    time.sleep(random.uniform(1.0, 2.0))

    try:
        response = session.get(target_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as err:
        print(f"Failed to load {target_url}: {err}")
        break  

    soup = BeautifulSoup(response.text, "html.parser")

    
    quote_blocks = soup.find_all("div", class_="quote")

    for block in quote_blocks:
        text_el = block.find("span", class_="text")
        author_el = block.find("small", class_="author")

        all_records.append({
            "quote": text_el.get_text(strip=True) if text_el else "N/A",
            "author": author_el.get_text(strip=True) if author_el else "Anonymous"
        })

  
    next_btn = soup.find("li", class_="next")

    if next_btn and next_btn.find("a"):
        current_path = next_btn.find("a")["href"]
    else:
        print("Reached final page. Stopping crawl.")
        current_path = None


with open("multipage_quotes.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["quote", "author"])
    writer.writeheader()
    writer.writerows(all_records)

print(f"\nDone! Successfully extracted {len(all_records)} items across all pages.")
