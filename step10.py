import sqlite3
import pandas as pd

conn = sqlite3.connect("books.db")
news = pd.read_sql("SELECT * FROM news", conn)
print(len(news), "headlines loaded")
conn.close()

news["companies"] = news["title"].apply(match_companies)

tagged = news.explode("companies").dropna(subset=["companies"])
print(len(tagged), "company mentions")
print(tagged[["companies", "title", "sentiment"]])

summary = (
    tagged.groupby("companies")["sentiment"]
    .agg(["count", "mean"])
    .sort_values("count", ascending=False)
)

print(summary)
