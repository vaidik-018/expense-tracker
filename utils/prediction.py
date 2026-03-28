import os
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import sqlite3

BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path=os.path.join(BASE_DIR,"database.db")

def predict_next_month():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)

    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby('date')['amount'].sum().reset_index()

    df['day'] = (df['date'] - df['date'].min()).dt.days

    X = df[['day']]
    y = df['amount']

    model = LinearRegression()
    model.fit(X, y)

    future_day = np.array([[df['day'].max() + 30]])
    prediction = model.predict(future_day)

    return prediction[0]