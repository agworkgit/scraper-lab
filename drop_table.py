import sqlite3

conn = sqlite3.connect("books.db")
conn.execute("DROP TABLE news")
conn.commit()
conn.close()
