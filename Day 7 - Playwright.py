"""
Playwright Dynamic Scraping Engine (v1.0)

"""

import sys
from playwright.sync_api import sync_playwright


TARGET_URL = "https://quotes.toscrape.com/js/"

def run_dynamic_scraper(url: str):
    print(f"[+] Launching headless Chromium engine...")
    
    with sync_playwright() as p:
    
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        
  
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        
        page = context.new_page()
        
        try:
            print(f"[+] Navigating to: {url}")
            page.goto(url, wait_until="networkidle", timeout=30000)
            
          
            page.wait_for_selector("div.quote", timeout=10000)
            
            elements = page.query_selector_all("div.quote")
            print(f"[✓] Successfully extracted {len(elements)} JS-rendered nodes.\n")
            
            for idx, el in enumerate(elements[:3], start=1):
                quote_text = el.query_selector("span.text").inner_text()
                author_name = el.query_selector("small.author").inner_text()
                print(f"[{idx}] {author_name}: {quote_text}")
                
        except Exception as e:
            print(f"[!] Scraper execution exception: {e}", file=sys.stderr)
            
        finally:
            context.close()
            browser.close()
            print("\n[+] Browser session terminated cleanly.")

if __name__ == "__main__":
    run_dynamic_scraper(TARGET_URL)
