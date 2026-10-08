import requests

r = requests.get("https://books.toscrape.com/")
print(r.status_code)
print(r.text)
# print(r.headers["content-type"])
# print(r.encoding)
# print(r.text)
# print(r.json())
