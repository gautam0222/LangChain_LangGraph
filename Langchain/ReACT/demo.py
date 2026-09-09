import sqlite3

conn = sqlite3.connect("SalesDB/sales.db")

cursor = conn.cursor()


cursor.execute("SELECT * FROM sales")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()    