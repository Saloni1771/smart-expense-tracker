import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DB_Path="database/tracker.db"

def connect_db():
    # connect to the existing database
    return sqlite3.connect(DB_Path) 

def add_expense(user_id, amount, category, description):
    conn=connect_db()
    # create a controller to interact with database
    cursor=conn.cursor()
    date=datetime.now().strftime("%Y-%m-%d")
    #query to add expenses
    cursor.execute('''
        INSERT INTO expenses(user_id, amount, category, description, date)
        VALUES (?,?,?,?,?)
    ''', (amount, category, description, date))
    conn.commit()
    conn.close()
    print("\n  ✅ Expenses added successfully!")

def view_expenses(user_id):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC', conn,params=(user_id,))
    rows=cursor.fetchall()
    conn.close()

    if rows:
        print("\n---Expenses History ----")
        for row in rows:
            print(f"ID: {row[0]} | ₹{row[1]:.2f} | {row[2]} | {row[3]} | {row[4]} ") 

    else:
        print("\n⚠️ No expences recorded yet.")

def delete_expense(expense_id):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?' ,(expense_id,))
    conn.commit()
    conn.close()
    print(f"🗑️ Expenses ID {expense_id} deleted.")

def generate_summary():
    conn=connect_db()
    cursor=conn.cursor()
    df = pd.read_sql_query("SELECT * FROM expenses",conn)
    conn.close()

    if df.empty:
        print("\n No data expenses to summarize.")
        return
    # convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    print("\n ----Monthly Expense Summary ---")
    df['month'] = df['date'].dt.strftime('%Y-%m')
    summary= df.groupby(['month','category'])['amount'].sum().reset_index()

    print(summary)
    return df #we will use this late for visualization
def data_summary():
    conn=connect_db()
    cursor=conn.cursor()
    df = pd.read_sql_query("SELECT * FROM expenses",conn)
    conn.close()

    if df.empty:
        return None
    # convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    df['month'] = df['date'].dt.strftime('%Y-%m')
    summary= df.groupby(['month','category'])['amount'].sum().reset_index()
    return df

def visualize_expenses():
    df = data_summary()
    if df is None:
        return
    # convert date to column time
    df['date']=pd.to_datetime(df['date'])
    print("\nWhat would you like to visualize?")
    print("1. Pie Chart by Category")
    print("2. Bar Chart by Month")
    print("3. Both")
    choice = input("Enter your choice (1/2/3): ")
    
    #pie chart of spending by category
    if choice == "1" or choice == "3":
        category_summary = df.groupby('category')['amount'].sum()
        print("\n --- Visualizing Spending by Category---")
        category_summary.plot.pie(autopct='%1.1f%%', startangle=90, figsize=(6,6))
        plt.title("Spending Distribution by Category")  
        plt.ylabel("") # hide y-axis lable
        plt.tight_layout()
        plt.show()

    #bar chart for month;ly totals
    if choice == "2" or choice == "3":
        df['month']= df['date'].dt.strftime('%Y-%m')
        monthly_totals = df.groupby('month')['amount'].sum()
                              
        print("\n --- Visualizing Monthly Totals---")
        monthly_totals.plot(kind='bar', color='skyblue')
        plt.title("Monthly Expenses")
        plt.xlabel("Month")
        plt.ylabel("Total spent (₹)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
                              
def main():
    while True:
        print("\n========== Smart Expense Tracker ==========")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Generate Summary")
        print("5. Visualize Expenses")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                amount = float(input("Enter amount (₹): "))
                category = input("Enter category (e.g., Food, Rent, Travel): ")
                description = input("Enter description (optional): ")
                add_expense(amount, category, description)
            except ValueError:
                print("\n❌ Invalid input. Please enter a number for amount.")
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                delete_expense(expense_id)
            except ValueError:
                print("\n❌ Invalid ID. Please enter a number.")
        elif choice=="4":
            generate_summary()
        elif choice=="5":
            visualize_expenses()
        elif choice == "6":
            print("\n👋 Exiting... Have a great day!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    
