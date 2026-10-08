import sqlite3
import pandas as pd

conn = sqlite3.connect("books.db")
df = pd.read_sql("SELECT * FROM books", conn)
conn.close()

latest = df["scraped_at"].max()  # the most recent timestamp
newest = df[df["scraped_at"] == latest]  # keep only those rows
# several summaries at one, per group
print(df.groupby("scraped_at")["price"].agg(["mean", "count"]))
print(newest.sort_values("price", ascending=False).head(5))
