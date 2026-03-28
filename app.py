from flask import Flask, request, jsonify, render_template
import sqlite3
import pandas as pd

from utils.analytics import monthly_summary
from utils.prediction import predict_next_month
from utils.budget import check_budget

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    # cur.execute("DROP TABLE IF EXISTS transactions")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        category TEXT,
        amount REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()

def connect_db():
    return sqlite3.connect("database.db")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add', methods=['POST'])
def add_transactions():
    data = request.json
    print("DATA RECIEVED",data)
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)",
        (data['type'], data['category'], data['amount'], data['date'])
    )

    conn.commit()
    conn.close()
    print(data)
    return jsonify({"message": "Transactions added successfully"})
    

# ✅ NEW ROUTES
@app.route('/summary')
def summary():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month

    # GROUPING
    df = df.groupby(["month", "category"], as_index=False)["amount"].sum()

    return jsonify(df.to_dict(orient="records"))

@app.route("/chart")
def chart():
    data=monthly_summary().reset_index()
    return jsonify(data.to_dict(orient="records"))

@app.route('/predict')
def predict():
    return jsonify(monthly_summary().to_dict())


@app.route('/budget')
def budget():
    return jsonify({"status": check_budget()})

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn=connect_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM transactions WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "deleted successfully"})

@app.route("/transactions")
def transactions():
    conn=connect_db()
    df=pd.read_sql_query("SELECT* FROM transactions", conn)
    conn.close()
    return jsonify(df.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)