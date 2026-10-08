import requests
from bs4 import BeautifulSoup

r = requests.get("https://books.toscrape.com/")
clean = BeautifulSoup(r.text, "html.parser")

for heading in clean.html.find_all("h3"):
    link = heading.a
    print(link["title"])
