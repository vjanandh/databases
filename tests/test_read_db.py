import sqlite3 as sql
import random as rnd
import datetime as dt
import sys
import os

# Add the root directory to sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

# DB directory
db_dir = os.path.join(base_dir, 'tests', 'test_db')

from nw_logs_db_demo import rand_ip, gen_hash_pkt

def test_read():
    # Create a connection to the database on disk
    file = os.path.join(db_dir, "tutorial.db")
    con = sql.connect(file)

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
    assert True

def test_analyse_logs():
    file = os.path.join(db_dir, "nw_logs.db")
    con = sql.connect(file)
    cur = con.cursor()

    print("ERROR logs")
    res = cur.execute("SELECT * FROM nw_logs WHERE status = 'ERROR'")
    for row in res.fetchall():
        print(row)
    
    print("Frequent IPs")
    res = cur.execute('''
            SELECT ip_address, COUNT(*) as count FROM nw_logs
            GROUP BY ip_address
            HAVING count > 2
            ''')
    for row in res.fetchall():
        print(row)
    
    print("Logs after midnight")
    res = cur.execute('''
            SELECT * FROM nw_logs
            WHERE strftime('%H', timestamp) >= '00' AND strftime('%H', timestamp) <= '06'
            ''')
    for row in res.fetchall():
        print(row)
    
    print("Duplicate hash packets")
    res = cur.execute('''
            SELECT ip_address, hashed_pkt, COUNT(*) as count FROM nw_logs
            GROUP BY hashed_pkt
            HAVING count > 1
            ''')
    for row in res.fetchall():
        print(row)
    
    con.close()
    assert True

def test_nw_logs():
    # Create a connection to the database on disk
    file = os.path.join(db_dir, "nw_logs.db")
    con = sql.connect(file)
    # Create a cursor to execute SQL statements and fetch results
    cur = con.cursor()

    # Check if the table already exists or else create one
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() is not None:
        return test_analyse_logs()
    else:
        # Generate and add some logs into the table
        for _ in range(50):
            ip = rand_ip()
            ts = dt.datetime.now() - dt.timedelta(minutes=rnd.randint(0, 60))
            status = rnd.choice(['OK', 'ERROR'])
            pkt = gen_hash_pkt()

            cur.execute("""
                INSERT INTO nw_logs (ip_address, timestamp, status, hashed_pkt)
                VALUES (?, ?, ?, ?)
                """, (ip, ts.isoformat(), status, pkt))
        con.commit()
        con.close()
        return test_analyse_logs()
test_nw_logs()