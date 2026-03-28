import os
import pandas as pd
import sqlite3
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path=os.path.join(BASE_DIR,"database.db")
def get_data():
    conn=sqlite3.connect("database.db")
    df=pd.read_sql_query("SELECT * FROM transactions", conn)
    return df

def monthly_summary():
    df = get_data()

    if df.empty:
        return "No data found"

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month

    # 🔥 IMPORTANT FILTER
    df = df[df["type"] == "expense"]

    print(df)

    return df.groupby(["month", "category"],as_index=False)["amount"].sum()


import matplotlib.pyplot as plt
def plot_category_expense(df):
    df.groupby("category")["amount"].sum().plot(kind="bar")
    plt.title("category-wise expense")
    plt.show()
