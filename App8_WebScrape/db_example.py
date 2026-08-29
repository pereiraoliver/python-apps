import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# 'INSERT INTO events VALUES ("Monkey", "Monkey City", "2088.10.15")'
# 'SELECT * FROM events WHERE date="2088.10.15"'
# 'DELETE FROM events WHERE band="Tigers"'


connection = sqlite3.connect(f"{BASE_DIR}/data.db")
cursor = connection.cursor()

# Query all data
cursor.execute("SELECT * FROM events")
rows = cursor.fetchall()
print(rows)

# Query certain columns
cursor.execute("SELECT band, date FROM events WHERE date='2088.10.15'")
rows = cursor.fetchall()
print(rows)

# # Insert new rows
# new_rows = [("Cat", "Cat City", "2088.10.17"), ("Hen", "Hen City", "2088.10.17")]
# cursor.executemany("INSERT INTO events VALUES (?,?,?)", new_rows)
# connection.commit()
