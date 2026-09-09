import csv
import random
import time
import requests
from bs4 import BeautifulSoup


def run_production_scraper():
    #1: STEALTH IDENTITY SETUP ────────────────────────
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
    )

    url = "https://quotes.toscrape.com/"

    try:
        # Add human jitter random delay
        time.sleep(random.uniform(1.5, 3.0))

        response = session.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as err:
        print(f"Network error encountered: {err}")
        return

    # ─── PILLAR 2: RELATIVE DOM isolation ───────────────────────
    soup = BeautifulSoup(response.text, "html.parser")

    # Isolate parent container blocks first
    quote_blocks = soup.find_all("div", class_="quote")

    extracted_records = []

    for block in quote_blocks:
        # Relative lookups inside THIS container scope
        text_el = block.find("span", class_="text")
        author_el = block.find("small", class_="author")

        # Defensive ternary extraction for avoiding crashes
        quote_text = text_el.get_text(strip=True) if text_el else None
        author_name = author_el.get_text(strip=True) if author_el else None

        extracted_records.append(
            {
                "quote": quote_text,
                "author": author_name,
            }
        )

    # ─── PILLAR 3: DEFENSIVE DATA NORMALIZATION &  COOL FILE I/O ──────
    fieldnames = ["quote", "author", "status"]

    with open(
        "quotes_master_clean.csv", mode="w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for record in extracted_records:
            # Enforce schema using .get() fallbacks
            clean_row = {
                "quote": record.get("quote") or "N/A",
                "author": record.get("author") or "Anonymous",
                "status": "Verified",
            }
            writer.writerow(clean_row)

    print(
        f"Success: Processed {len(extracted_records)} records into quotes_master_clean.csv"
    )


if __name__ == "__main__":
    run_production_scraper()
