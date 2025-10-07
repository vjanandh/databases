import random as rnd
import hashlib as hash
import sqlite3 as sql
import datetime as dt
import sys
import os

# A function to generate random IP address
def rand_ip():
    return f"{rnd.randint(0,255)}.{rnd.randint(0,255)}.{rnd.randint(0,255)}.{rnd.randint(0,255)}"

# A function to simulate encrypted packet hash
def gen_hash_pkt():
    payload = "".join(rnd.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=50))
    hash_obj = hash.sha256(payload.encode())
    return hash_obj.hexdigest()

if __name__ == '__main__':
    # Add the root directory to sys.path
    base_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(base_dir)

    # DB directory
    db_dir = os.path.join(base_dir, 'db')

    # Connect to network logs database (create one if it does not exist)
    file = os.path.join(db_dir, "nw_logs.db")
    con = sql.connect(file)
    cur = con.cursor()

    # Create a network logs table if it does not exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nw_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            timestamp TEXT,
            status TEXT,
            hashed_pkt TEXT
        )
    """)

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