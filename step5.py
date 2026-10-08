import sqlite3

conn = sqlite3.connect("fruit.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS fruit (
        name TEXT,
        price REAL,
        ripe INTEGER
    )
""")

rows = [("apple", 0.5, 1), ("pear", 0.7, 0)]
# ? placeholders get filled in from the tuples
cur.executemany("INSERT INTO fruit VALUES (?, ?, ?)", rows)
# nothing is saved until you commit
conn.commit()

cur.execute("SELECT * FROM fruit")
print(cur.fetchall())
conn.close()

# [('apple', 0.5, 1), ('pear', 0.7, 0)]
