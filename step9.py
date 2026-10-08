import feedparser
import pandas as pd
import sqlite3
from datetime import datetime
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()


def scrape_feed(source, URL):
    feed = feedparser.parse(URL)  # also accepts a URL

    rows = []
    for entry in feed.entries:
        rows.append(
            {
                "title": entry.title,
                "source": source,
                "published": entry.published,
                "link": entry.link,
                "sentiment": analyser.polarity_scores(entry.title)["compound"],
            }
        )

    return pd.DataFrame(rows)


feeds = {
    "BBC Business": "https://feeds.bbci.co.uk/news/business/rss.xml",
    "Guardian Business": "https://www.theguardian.com/uk/business/rss",
    "CNBC": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",
}

frames = []
for source, URL in feeds.items():
    frames.append(scrape_feed(source, URL))
    time.sleep(1)

news = pd.concat(frames, ignore_index=True)
print(news.shape)

news = news.drop_duplicates(subset="link")
news["scraped_at"] = datetime.now().isoformat()
print(news.shape)
print(news["source"].value_counts())

conn = sqlite3.connect("books.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS news (
        title TEXT,
        source TEXT,
        published TEXT,
        link TEXT UNIQUE,
        sentiment REAL,
        scraped_at TEXT
    )
""")

conn.commit()

before = conn.execute("SELECT COUNT(*) FROM news").fetchone()[0]
rows = list(
    news[
        ["title", "source", "published", "link", "sentiment", "scraped_at"]
    ].itertuples(index=False, name=None)
)

conn.executemany(
    """
    INSERT OR IGNORE INTO news
        (title, source, published, link, sentiment, scraped_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    rows,
)

conn.commit()

after = conn.execute("SELECT COUNT(*) FROM news").fetchone()[0]
print(after - before, "new stories added;", after, "in total")

conn.close()
