import sqlite3
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
conn = sqlite3.connect("SalesDB/sales.db")

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS sales
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            price REAL NOT NULL)''')

cursor.execute('''INSERT INTO sales (customer_name, product_name, quantity, total_price, price)              VALUES
              ('John Doe', 'Product A', 2, 50.0, 25.0),
              ('Jane Smith', 'Product B', 1, 30.0, 30.0),
              ('Alice Johnson', 'Product C', 3, 90.0, 30.0),
              ('Bob Brown', 'Product A', 1, 25.0, 25.0),
              ('Charlie Davis', 'Product B', 2, 60.0, 30.0)''')

conn.commit()
conn.close()