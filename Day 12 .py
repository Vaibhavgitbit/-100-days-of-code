import asyncio
import json
from playwright.async_api import async_playwright

async def save_authenticated_session():
    print("[+] Launching Browser for Login Automation...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # 1. Navigate to login page
        login_url = "https://quotes.toscrape.com/login"
        print(f"[+] Navigating to login page: {login_url}")
        await page.goto(login_url, wait_until="networkidle")

        # 2. Fill form inputs (selector, text)
        print("[+] Automating form field inputs...")
        await page.fill('input[name="username"]', 'my_secret_user')
        await page.fill('input[name="password"]', 'my_secret_pass')

        # 3. Click submit button and wait for redirect/navigation
        print("[+] Submitting login form...")
        await asyncio.gather(
            page.wait_for_selector("a[href='/logout']"), # Verify logged-in element appears
            page.click('input[type="submit"]')
        )
        
        print("[✓] Login successful! Capturing session state (Cookies & Storage)...")

        # 4. Save entire authenticated context (cookies, localStorage) to JSON
        session_file = "auth_state.json"
        await context.storage_state(path=session_file)
        print(f"[✓] Session state exported cleanly to '{session_file}'.")

        await context.close()
        await browser.close()

await save_authenticated_session()
