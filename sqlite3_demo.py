import sqlite3 as sql
import sys
import os

# Add the root directory to sys.path
base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(base_dir)

# DB directory
db_dir = os.path.join(base_dir, 'db')

# Create a connection to the database on disk
file = os.path.join(db_dir, "tutorial.db")
con = sql.connect(file)

# Create a cursor to execute SQL statements and fetch results
cur = con.cursor()

# Check if the table already exists or else create one
res = cur.execute("SELECT name FROM sqlite_master")
if res.fetchone() is None:
    # Create a table and specify the columns
    cur.execute("CREATE TABLE movies(title, year, score)")
    
    # Check if the table has been created by fetching its name from the schema table of the database
    res = cur.execute("SELECT name FROM sqlite_master")
    print(res.fetchone())
    
    # Insert data into the table
    cur.execute("""
        INSERT INTO movies VALUES
                ('Monty Python and the Holy Grail', 1975, 8.2),
                ('And Now for Something Completely Different', 1971, 7.5)
    """)
    con.commit() # Commit changes to the database

    # Fetch the existing data from the table
    res = cur.execute("SELECT * from movies")
    print(res.fetchall())
    
    # Insert multiple rows - a different syntax using executemany() function
    data = [
        ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
        ("Monty Python's The Meaning of Life", 1983, 7.5),
        ("Monty Python's Life of Brian", 1979, 8.0),
    ]

    cur.executemany("INSERT INTO movies VALUES(?, ?, ?)", data)
    con.commit()

# Print all rows iteratively
for row in cur.execute("SELECT year, title, score FROM movies ORDER BY year"):
    print(row)

con.close()