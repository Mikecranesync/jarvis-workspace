import sqlite3
import os

db_path = "/opt/plc-copilot/kb_harvester/kb_industrial.db"
print(f"DB size: {os.path.getsize(db_path) / 1024:.1f} KB")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print(f"Tables: {tables}")

for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    print(f"  {t}: {cur.fetchone()[0]} rows")

# Sample data from each table
for t in tables:
    cur.execute(f"SELECT * FROM {t} LIMIT 2")
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    print(f"\n--- {t} ({', '.join(cols)}) ---")
    for r in rows:
        print(f"  {r[:3]}...")

conn.close()
