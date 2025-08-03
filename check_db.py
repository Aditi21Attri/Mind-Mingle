import sqlite3
import os

db_path = os.path.join('instance', 'moodmingle.db')
print(f'Checking database at: {db_path}')
print(f'Database exists: {os.path.exists(db_path)}')

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f'Tables in database: {tables}')
    conn.close()
else:
    print("Database not found!")
