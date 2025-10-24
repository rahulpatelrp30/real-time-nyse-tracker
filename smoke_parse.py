import requests
from bs4 import BeautifulSoup

URL = "https://finance.yahoo.com/most-active"
html = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}).text
soup = BeautifulSoup(html, "lxml")
table = soup.find("table")

rows = []
for tr in table.select("tbody tr"):
    tds = tr.find_all("td")
    if len(tds) < 6:
        continue
    rows.append((
        tds[0].get_text(strip=True),  # Symbol
        tds[1].get_text(strip=True),  # Name
        tds[2].get_text(strip=True),  # Price
        tds[4].get_text(strip=True),  # Change
        tds[5].get_text(strip=True),  # Volume
    ))

print(f"Parsed {len(rows)} rows")
print(rows[:5])

SLEEP_SECONDS = 180  # temp for testing; later set back to 180
