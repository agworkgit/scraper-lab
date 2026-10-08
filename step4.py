import requests
from bs4 import BeautifulSoup
import time


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
        books.append({"title": title, "price": clean_price, "in_stock": in_stock})
    return books


# Go through all pages and collect data
all_books = []

for n in range(49, 53):
    url = f"https://books.toscrape.com/catalogue/page-{n}.html"
    time.sleep(2)
    all_books.extend(scrape_page(url))

print(len(all_books))
