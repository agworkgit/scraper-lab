import requests
from bs4 import BeautifulSoup

r = requests.get("https://books.toscrape.com/")
r.encoding = "utf-8"
clean = BeautifulSoup(r.text, "html.parser")

# Build dictionary
books = []

for article in clean.html.find_all("article"):
    title = article.img["alt"]
    price = article.select_one("p.price_color").text
    clean_price = float(price.replace("£", ""))
    availability = article.select_one("p.availability").text.strip()
    in_stock = "In stock" in availability
    books.append({"title": title, "price": clean_price, "in_stock": in_stock})

print(books)

# <article class="product_pod">
# <div class="image_container">
# <a href="catalogue/its-only-the-himalayas_981/index.html"><img alt="It's Only the Himalayas" class="thumbnail" src="media/cache/27/a5/27a53d0bb95bdd88288eaf66c9230d7e.j
# pg"/></a>
# </div>
# <p class="star-rating Two">
# <i class="icon-star"></i>
# <i class="icon-star"></i>
# <i class="icon-star"></i>
# <i class="icon-star"></i>
# <i class="icon-star"></i>
# </p>
# <h3><a href="catalogue/its-only-the-himalayas_981/index.html" title="It's Only the Himalayas">It's Only the Himalayas</a></h3>
# <div class="product_price">
# <p class="price_color">Â£45.17</p>
# <p class="instock availability">
# <i class="icon-ok"></i>
#
#         In stock
#
# </p>
# <form>
# <button class="btn btn-primary btn-block" data-loading-text="Adding..." type="submit">Add to basket</button>
# </form>
# </div>
# </article>
