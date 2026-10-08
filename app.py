# used: requests, beautifulsoup, pandas, sqlite, streamlit
# run it with a cron job for realtime updates

import sqlite3
import pandas as pd
import streamlit as st

# for dashboard -> run with streamlit run <file>
# fetch company data
from companies import match_companies

conn = sqlite3.connect("books.db")
df = pd.read_sql("SELECT * FROM books", conn)
news = pd.read_sql("SELECT * FROM news", conn)
conn.close()

latest = df["scraped_at"].max()  # the most recent timestamp
newest = df[df["scraped_at"] == latest]  # keep only those rows
ranked = newest.sort_values("price", ascending=False)  # all rows, most expensive first
top = ranked.head(10)  # top 10, only used for the chart


news["companies"] = news["title"].apply(match_companies)
tagged = news.explode("companies").dropna(subset=["companies"])
summary = (
    tagged.groupby("companies")["sentiment"]
    .agg(["count", "mean"])
    .sort_values("count", ascending=False)
)

st.title("Trends Dashboard")

tab_books, tab_news = st.tabs(["Books", "Company news"])

with tab_books:
    st.metric("Books", len(newest))
    st.metric("Average Price", f'£{newest["price"].mean():.2f}')
    st.metric("In Stock", int(newest["in_stock"].sum()))
    st.dataframe(ranked)
    st.subheader("Runs So Far")
    st.dataframe(df.groupby("scraped_at")["price"].agg(["mean", "count"]))
    st.subheader("10 Most Expensive")
    st.bar_chart(top.set_index("title")["price"])

with tab_news:
    st.metric("Headlines Tracked", len(news))
    st.dataframe(summary)
    st.bar_chart(summary["count"])
    st.dataframe(tagged[["companies", "source", "title", "sentiment"]])
