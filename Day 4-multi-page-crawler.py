# run in python 
import csv
import requests
from bs4 import BeautifulSoup

# 1. System Parameters & File Configuration to store our precious data 😂
OUTPUT_FILE = "infinite_leveraged_quotes.csv"
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

print("🚀 Launching Multi-Page Crawler Pipelin...")

# 2. Context Storage Safe-Bubble (Prevents data corruption)
with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Author", "Quote Text"])  # Core Data Columns
    
    # 3. Dynamic Crawler Loop (Iterating up to 15 pages to test boundaries can be chnaged for how much we want)
    for page in range(1, 16):
        # path routing to avoid NameResolution errors
        target_url = f"https://quotes.toscrape.com/page/{page}/"
        print(f"📡 Sending Handshake Request to Page {page}...")
        
        response = requests.get(target_url, headers=BROWSER_HEADERS)
        
        # Verify Network Integrity
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            quote_containers = soup.find_all("div", class_="quote")
            
            # The Kill Switch Guard Clause: Exit if page yields zero data tags (cool code 😎)
            if not quote_containers:
                print(f"🛑 No data found on Page {page}. Graceful exit triggered.")
                break
                
            # Relative Loop Traversal to preserve row data alignment
            for container in quote_containers:
                quote_text = container.find("span", class_="text").text.strip()
                author_name = container.find("small", class_="author").text.strip()
                
                # Commit the verified data row into the CSV matrix file
                writer.writerow([author_name, quote_text])
                
            print(f"   ✅ Page {page} records extracted and committed successfully.")
        else:
            print(f"🚨 Network Blocked on Page {page}: Status Code {response.status_code}")
            break

print(f"📦 Pipeline Complete: Complete data asset locked inside {OUTPUT_FILE
}") #to acess data go to saved file location and open csvfile to see magic ✨🪄
