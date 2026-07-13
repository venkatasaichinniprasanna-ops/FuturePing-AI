import sqlite3

conn = sqlite3.connect("futureping.db")
cursor = conn.cursor()

# Create Students Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    email TEXT UNIQUE,
    password TEXT,
    branch TEXT,
    career TEXT
)
""")

# Create Opportunities Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS opportunities(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    type TEXT,
    link TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully.")