# smart-expense-tracker
# Smart Expense Tracker

A full-featured personal expense tracking app built with Python, Streamlit, SQLite, and Pandas. This project helps users log their expenses, view visual summaries, and securely manage their own data using a login system.

---

## 🔧 Features

- **Secure Login/Sign Up** using username and password
- **User-specific expense tracking** (no shared data)
- **Add/View/Delete Expenses**
- **Pie & Bar Charts** for monthly summaries
- **Download Excel report** of your expenses
- **CLI version** for quick use on local machines
- Built-in **SQLite database** (`tracker.db`)

---

## 📁 Project Structure


smart-expense-tracker/
│
├── app.py              ← Streamlit app with dashboard (main app)
├── app1.py             ← Alternate Streamlit UI with authentication
├── tracker.py          ← CLI version for local/terminal use
├── auth_db.py          ← Authentication logic (login/signup)
├── requirements.txt    ← List of required Python libraries
│
├── database/
│   ├── setup_db.py     ← DB schema setup (users + expenses)
│   └── tracker.db      ← SQLite database (auto-generated)
│
├── reports/            ← Folder to store downloadable Excel reports
│
└── README.md           ← You are here!


---

## 🛠️ Installation & Run Locally

### 1. Clone the Repo
bash
git clone https://github.com/yourusername/smart-expense-tracker.git
cd smart-expense-tracker


### 2. Install Dependencies
bash
pip install -r requirements.txt


### 3. Run the Streamlit App
bash
streamlit run app.py


The app will open in your browser at `http://localhost:8501`.

---

## 🧪 CLI Usage (Optional)

Want to use this from terminal?

bash
python tracker.py


This will launch a text-based menu in your terminal/IDLE for adding, viewing, deleting, and visualizing expenses.

---

## 🧾 Requirements

See `requirements.txt`, but key libraries used include:

- `streamlit`
- `pandas`
- `matplotlib`
- `sqlite3` (standard Python library)
- `hashlib` (for password encryption)

---

## 🌐 Deployment

You can easily deploy this to [Streamlit Cloud](https://streamlit.io/cloud) in 3 steps:
1. Push your project to a public GitHub repo
2. Go to Streamlit Cloud and link your repo
3. Set `app.py/ app1.py as the main app file depending on with or without authentication requirement.

*Note: SQLite works well for small apps, but for multiple users in production, consider switching to PostgreSQL.*

---

## ✨ Future Ideas

- Add expense categories with icons or emojis
- Track income vs expenses
- Monthly budget notifications
- Export filtered reports

---

## 🙌 Author

Built by Saloni — IIT grad, aspiring developer + creative storyteller.

-----