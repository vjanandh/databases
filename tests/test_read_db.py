import sqlite3 as sql

# Create a connection to the database on disk
con = sql.connect("tutorial.db")

# Create a cursor to execute SQL statements and fetch results
cur = con.cursor()

# Print all rows iteratively
for row in cur.execute("SELECT year, title, score FROM movies ORDER BY year"):
    print(row)