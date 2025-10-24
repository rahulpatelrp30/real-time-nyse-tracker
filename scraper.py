# scraper.py
import time
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

URL = "https://finance.yahoo.com/most-active"
SLEEP_SECONDS = 20  # use 20s while testing; change to 180 (3 min) later

client = MongoClient("mongodb://localhost:27017")
db = client["nyse_tracker"]
col = db["most_active"]

def fetch_html(url: str, retries: int = 2, timeout: int = 12) -> str:
    for attempt in range(retries + 1):
        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=timeout
        )
        if 200 <= r.status_code < 300:
            return r.text
        if attempt < retries:
            time.sleep(3)
    raise RuntimeError(f"Failed to fetch {url} after {retries+1} attempts")

def parse_rows(html: str):
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    if not table:
        return []
    rows = []
    for tr in table.select("tbody tr"):
        tds = tr.find_all("td")
        if len(tds) < 6:
            continue
        rows.append({
            "Symbol": tds[0].get_text(strip=True),
            "Name":   tds[1].get_text(strip=True),
            "Price":  tds[2].get_text(strip=True),
            "Change": tds[4].get_text(strip=True),  # adjust index if Yahoo layout changes
            "Volume": tds[5].get_text(strip=True),
            "timestamp": datetime.now(timezone.utc),
        })
    return rows

def main():
    print("📈 Starting NYSE Most Active scraper… (Ctrl+C to stop)")
    while True:
        try:
            html = fetch_html(URL)
            docs = parse_rows(html)
            if docs:
                col.insert_many(docs)
                print(f"✅ {len(docs)} rows inserted at {datetime.now().strftime('%H:%M:%S')}")
            else:
                print("⚠️ No rows parsed this cycle.")
        except Exception as e:
            print(f"❌ Error: {e}")
            # Per assignment: terminate if retries failed
            break
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
