import asyncio
import json
from playwright.async_api import async_playwright

async def api_sniffer():
    print("[+] Launching API Network Interceptor...")
    
    captured_json_data = []

    async def handle_response(response):
  
        resource_type = response.request.resource_type
        if resource_type in ["fetch", "xhr"]:
            try:
            
                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    data = await response.json()
                    print(f"\n[⚡ HIDDEN API DETECTED]")
                    print(f"➜ Endpoint: {response.url}")
                    print(f"➜ Status: {response.status}")
                    
                    captured_json_data.append({
                        "url": response.url,
                        "status": response.status,
                        "data": data
                    })
            except Exception:
                pass 

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        page.on("response", handle_response)

        
        target_url = "https://quotes.toscrape.com/scroll"
        print(f"[+] Navigating to: {target_url}")
        
        await page.goto(target_url, wait_until="networkidle")

    
        print("[+] Triggering user actions to fire API requests...")
        for _ in range(3):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1500)

        print(f"\n[✓] Intercepted {len(captured_json_data)} raw JSON payloads.")
        
        
        with open("raw_api_dump.json", "w") as f:
            json.dump(captured_json_data, f, indent=2)
            
        print("[✓] Saved all intercepted API calls to 'raw_api_dump.json'.")

        await context.close()
        await browser.close()

await api_sniffer()
