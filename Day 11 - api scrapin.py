import asyncio 
import json
from playwright.async_api import async_playwright
async def api_sniffer():
  captured_json_data=[]
  async def handle_response(response):
    resource_type=response.requests.resource_type
    if resource_type in ["fetch","xhr"]:
      try:
        content_type = response.headers.get("content-type","")
        if "application/json" in content_type:
          data = await response.json()
          captured_json_data.append({"url":response.url,"status":response.status,"data":data})
      except Exception:
        pass
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    context=await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    page=await context.new_page()
    page.on("response",handle_response)
    target_url="quotes.toscrape.com"
    await page.goto(target_url,wait_unti="networkidle")
    for _ in range:
      await page.evaluate("window.scrollTo(0,document.body.scrollHeight)")
      await page.wait_for_timeout(1500)
    with open("raw_api_dump.json","w")as f:
      json.dump(captured_json_data,f,indent=2)
    await context.close()
    await browser.close()
await api_sniffer()
