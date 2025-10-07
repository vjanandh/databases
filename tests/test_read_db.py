import sqlite3 as sql

# Create a connection to the database on disk
con = sql.connect("tutorial.db")

# Create a cursor to execute SQL statements and fetch results
cur = con.cursor()

# Check if the table already exists or else create one
res = cur.execute("SELECT name FROM sqlite_master")
if res.fetchone() is not None:
    # Print all rows iteratively
    for row in cur.execute("SELECT year, title, score FROM movies ORDER BY year"):
        print(row)
else:
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
con.close()
