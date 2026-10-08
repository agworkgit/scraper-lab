import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from datetime import datetime


def scrape_page(url):
    books = []
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Page {url} returned {r.status_code}")
        return []
    r.encoding = "utf-8"
    clean = BeautifulSoup(r.text, "html.parser")
    # Build dictionary
    for article in clean.html.find_all("article"):
        title = article.img["alt"]
        price = article.select_one("p.price_color").text
        clean_price = float(price.replace("£", ""))
        availability = article.select_one("p.availability").text.strip()
        in_stock = "In stock" in availability
        books.append(
            {
                "title": title,
                "price": clean_price,
                "in_stock": in_stock,
            }
        )
    return books


# Go through all pages and collect data
all_books = []
scraped_at = datetime.now().isoformat()

for n in range(1, 4):
    url = f"https://books.toscrape.com/catalogue/page-{n}.html"
    time.sleep(2)
    all_books.extend(scrape_page(url))

print(len(all_books))

# Connect a database
conn = sqlite3.connect("books.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        title TEXT,
        price REAL,
        in_stock INTEGER,
        scraped_at TEXT
    )
""")

rows = []

for book in all_books:
    rows.append((book["title"], book["price"], book["in_stock"], scraped_at))
# ? placeholders get filled in from the tuples
cur.executemany("INSERT INTO books VALUES (?, ?, ?, ?)", rows)
# nothing is saved until you commit
conn.commit()

cur.execute("SELECT COUNT(*) FROM books")
print(cur.fetchone()[0])
cur.execute("SELECT * FROM books LIMIT 3")
print(cur.fetchall())
conn.close()
