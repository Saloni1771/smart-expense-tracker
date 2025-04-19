import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import auth_db

auth_db.create_users_table()

# Ensure reports folder exists
os.makedirs("reports", exist_ok=True)

DB_PATH = "database/tracker.db"
# Set page title and icon
st.set_page_config(page_title="Smart Expense Tracker", page_icon="💸", layout="centered")

def connect_db():
    return sqlite3.connect(DB_PATH)

def add_expense(amount, category, description):
    conn = connect_db()
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, description, date))
    conn.commit()
    conn.close()

def get_expenses():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC", conn)
    conn.close()
    return df

def export_to_excel(df):
    path = "reports/expense_report.xlsx"
    df.to_excel(path, index=False)
    return path

# ----------------- Streamlit UI -----------------
st.title("Smart Expense Tracker")

menu = ["Add Expense", "View Expenses", "Download Report"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Expense":
    st.subheader("Add a New Expense")

    amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
    category = st.selectbox("Category", ["Food", "Rent", "Travel", "Shopping", "Bills", "Other"])
    description = st.text_input("Description")

    if st.button("Add"):
        if amount > 0:
            add_expense(amount, category, description)
            st.success("✅ Expense added successfully!")
        else:
            st.error("Amount must be greater than 0.")

elif choice == "View Expenses":
    st.subheader("Your Expense History")
    df = get_expenses()
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No expenses recorded yet.")

elif choice == "Download Report":
    st.subheader("Download All Expenses as Excel")
    df = get_expenses()
    if df.empty:
        st.warning("No data to export.")
    else:
        path = export_to_excel(df)
        with open(path, "rb") as f:
            st.download_button("📥 Download Excel", f, file_name="expense_report.xlsx")
