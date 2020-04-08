import sqlite3

# ===== DB Connection =====
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# ==== Table Creation =====
# in sqlite for auto-incrementing, you must use INTEGER PRIMARY KEY
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# 'real' is a number with a decimal point in sqlite
create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)

# query for test
# cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

connection.commit()

connection.close()