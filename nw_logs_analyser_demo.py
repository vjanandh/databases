import sqlite3 as sql
import sys
import os

# Add the root directory to sys.path
base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(base_dir)

# DB directory
db_dir = os.path.join(base_dir, 'db')

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