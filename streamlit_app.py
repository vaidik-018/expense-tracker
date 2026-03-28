import streamlit as st
from utils.analytics import monthly_summary
from utils.prediction import predict_next_month

st.title("Smart Expense Tracker")

if st.button("Show Summary"):
    st.write(monthly_summary())

if st.button("Predict Next Month Expense"):
    st.write(predict_next_month())