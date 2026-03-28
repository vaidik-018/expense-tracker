import os
import sqlite3

BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path=os.path.join(BASE_DIR,"database.db")
def get_total_expense():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    total = cur.fetchone()[0] or 0

    return total

def check_budget(limit=5000):
    total = get_total_expense()

    if total > limit:
        return "⚠️ Budget exceeded!"
    return "✅ Within budget"