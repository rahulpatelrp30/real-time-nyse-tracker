import requests
import time
from pymongo import MongoClient
from bs4 import BeautifulSoup

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Change this URL to your MongoDB server
db = client['stock_database']  # Change 'stock_database' to your database name
collection = db['most_active_stocks']  # Change 'most_active_stocks' to your collection name

def fetch_stock_data():
    url = 'https://finance.yahoo.com/most-active'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for any request errors

        soup = BeautifulSoup(response.text, 'html.parser')

        stock_data = []

        indexes = soup.find_all('td', class_='Py(10px) Ta(start)')[:6]
        symbols = soup.find_all('td', class_='Va(m) Ta(start) Pstart(10px) Fz(s)')[:6]
        prices = soup.find_all('td', class_='Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)')[:6]
        changes = soup.find_all('td', class_='Py(10px) Pstart(10px)')[:6]
        volumes = soup.find_all('td', class_='Py(10px) Pstart(20px)')[:6]
        names = soup.find_all('td', class_='Va(m) Ta(start) Px(10px)')[:6]

        for index, symbol, price, change, volume, name in zip(indexes, symbols, prices, changes, volumes, names):
            stock = {
                'Symbol': symbol.text,
                'Name': name.text,
                'Price (Intraday)': price.text,
                'Change': change.text,
                'Volume': volume.text
            }
            stock_data.append(stock)

        # Save the data to MongoDB
        collection.insert_many(stock_data)
        print("Data saved successfully to MongoDB")

    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        # Retry logic can be added here if needed

if __name__ == "__main__":
    # Run the data fetching loop indefinitely every 3 minutes (change as needed)
    try:
        while True:
            fetch_stock_data()
            time.sleep(180)  # Sleep for 3 minutes
    except KeyboardInterrupt:
        print("Stopping the program.")
