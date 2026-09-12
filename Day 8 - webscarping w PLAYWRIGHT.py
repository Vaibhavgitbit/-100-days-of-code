import asyncio
import json
from playwright.async_api import async_playwright

async def run_pagination_scraper():
    print("[+] Launching Multi-Page Pagination Engine...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        target_url = "https://quotes.toscrape.com/js/"
        await page.goto(target_url, wait_until="networkidle")
        
        scraped_data = []
        page_num = 1
        
        while True:
            print(f"[+] Scraping Page {page_num}...")
            await page.wait_for_selector("div.quote", timeout=10000)
            
            quotes = await page.query_selector_all("div.quote")
            for q in quotes:
                text_el = await q.query_selector("span.text")
                author_el = await q.query_selector("small.author")
                
                scraped_data.append({
                    "page": page_num,
                    "author": await author_el.inner_text() if author_el else "Unknown",
                    "quote": await text_el.inner_text() if text_el else "N/A"
                })
            
            # Check for the presence of the 'Next' button
            next_button = await page.query_selector("li.next > a")
            
            if not next_button:
                print("[!] No further pages detected. Ending navigation loop.")
                break
            
            # Click next and wait for network/DOM to update
            print("[+] Clicking 'Next' page button...")
            await asyncio.gather(
                page.wait_for_selector("div.quote"),
                next_button.click()
            )
            page_num += 1
            await page.wait_for_timeout(1000)  # Gentle delay between page clicks

        print(f"\n[✓] Successfully scraped {len(scraped_data)} total items across {page_num} pages.\n")
        print(json.dumps(scraped_data[:3], indent=2))
        
        await context.close()
        await browser.close()

await run_pagination_scraper()
