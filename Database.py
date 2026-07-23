import sqlite3
import os

# Create database folder if it doesn't exist
os.makedirs("database", exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect("database/fake_news.db")

cursor = conn.cursor()

# Create History Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    news_title TEXT,

    news_text TEXT NOT NULL,

    prediction TEXT,

    confidence REAL,

    summary TEXT,

    source_url TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()

conn.close()

print("Database Created Successfully")