import sqlite3

conn = sqlite3.connect("futureping.db")
cursor = conn.cursor()

cursor.execute("""
DELETE FROM opportunities
WHERE id = (
    SELECT MAX(id)
    FROM opportunities
    WHERE title='OpenAI Internship'
)
""")

conn.commit()
conn.close()

print("Duplicate removed successfully.")