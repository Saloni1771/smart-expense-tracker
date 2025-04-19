import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import auth_db

auth_db.create_users_table()

# Ensure reports folder exists
os.makedirs("reports", exist_ok=True)

# Set page title and icon
st.set_page_config(page_title="Smart Expense Tracker", page_icon="💸", layout="centered")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = ""
if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = True

DB_PATH = "database/tracker.db"

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

# Login/Signup Logic
def login_section():
    st.subheader("Login / Sign Up")

    option = st.radio("Choose an action:", ["Login", "Sign Up"], key="auth_option",on_change=reset_fields)

    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")

    if option == "Sign Up":
        if st.button("Create Account"):
            success = auth_db.register_user(username, password)
            if success:
                st.success("Account created successfully!")
                st.rerun()  # Refresh to clear fields
            else:
                st.error("Username already exists.")

    elif option == "Login":
        if st.button("Login"):
            user_id = auth_db.login_user(username, password)
            if user_id:
                st.success(f"Welcome, {username}!")
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.rerun()  # Refresh to hide login section
            else:
                st.error("Invalid username or password.")
                
# Function to reset username and password fields when switching options
def reset_fields():
    st.session_state.username_input = ""
    st.session_state.password_input = ""
                
# ----------------- Streamlit UI -----------------

# Show expense tracking only after login
if not st.session_state.logged_in:
    login_section()
else:
    st.sidebar.title(f"Welcome, {st.session_state['username']}")

    menu = ["Add Expense", "View Expenses", "Download Report", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Expense":
        # your add expense code (use user_id from session)
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
        # your view code
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
    elif choice=="Logout":
        st.session_state.logged_in = False
        st.session_state.sidebar_visible = False
        st.rerun()  # Refresh the page to hide the sidebar
        login_session()






