import streamlit as st
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict
import pandas as pd
import os

DATA_FILE = "transactions.json"


def seed_sample_data():
    """Create some sample transactions when there's no existing file."""
    if os.path.exists(DATA_FILE):
        return
    sample = [
        Income(datetime.today().isoformat(), 5000.0, "Salary", "Monthly salary"),
        Expense(datetime.today().replace(day=5).isoformat(), 1200.0, "Rent", "Monthly rent"),
        Expense(datetime.today().replace(day=10).isoformat(), 150.0, "Groceries", "Weekly groceries"),
        Expense(datetime.today().replace(day=15).isoformat(), 60.0, "Transport", "Gas & transit"),
        Investment(datetime.today().replace(day=20).isoformat(), 300.0, "Stocks", "Monthly investment"),
    ]
    save_transactions([s.to_dict() for s in sample])

# --------------------
# Object-oriented model
# --------------------
@dataclass
class Transaction:
    date: str
    amount: float
    category: str
    note: str = ""
    type: str = "transaction"

    def to_dict(self):
        return asdict(self)


class Income(Transaction):
    def __init__(self, date: str, amount: float, category: str, note: str = ""):
        super().__init__(date, amount, category, note, type="income")


class Expense(Transaction):
    def __init__(self, date: str, amount: float, category: str, note: str = ""):
        super().__init__(date, amount, category, note, type="expense")


class Investment(Transaction):
    def __init__(self, date: str, amount: float, category: str, note: str = ""):
        super().__init__(date, amount, category, note, type="investment")


# --------------------
# Data storage helpers
# --------------------

def load_transactions() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_transactions(transactions: List[Dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)


# --------------------
# Business logic
# --------------------

def add_transaction(tx: Transaction):
    transactions = load_transactions()
    transactions.append(tx.to_dict())
    save_transactions(transactions)


def transactions_to_df(transactions: List[Dict]) -> pd.DataFrame:
    if not transactions:
        return pd.DataFrame(columns=["date", "amount", "category", "note", "type"])

    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def calculate_statistics(df: pd.DataFrame) -> Dict:
    stats = {
        "total_income": 0.0,
        "total_expense": 0.0,
        "total_investment": 0.0,
        "net_balance": 0.0,
        "savings_percentage": 0.0,
    }
    if df.empty:
        return stats

    stats["total_income"] = df[df["type"] == "income"]["amount"].sum()
    stats["total_expense"] = df[df["type"] == "expense"]["amount"].sum()
    stats["total_investment"] = df[df["type"] == "investment"]["amount"].sum()

    stats["net_balance"] = stats["total_income"] - stats["total_expense"] - stats["total_investment"]

    if stats["total_income"] > 0:
        savings = stats["total_income"] - stats["total_expense"]
        stats["savings_percentage"] = (savings / stats["total_income"]) * 100

    return stats


def analyze_categories(df: pd.DataFrame) -> Dict:
    result = {
        "highest_spending_category": None,
        "most_frequent_category": None,
        "unique_categories": set(),
        "category_totals": {},
    }

    if df.empty:
        return result

    # Highest spending category (expenses only)
    expense_df = df[df["type"] == "expense"]
    if not expense_df.empty:
        cat_totals = expense_df.groupby("category")["amount"].sum().to_dict()
        result["category_totals"] = cat_totals
        result["highest_spending_category"] = max(cat_totals.items(), key=lambda x: x[1])[0]

    # Most frequent category overall
    freq = df["category"].value_counts()
    if not freq.empty:
        result["most_frequent_category"] = freq.idxmax()

    result["unique_categories"] = set(df["category"].unique().tolist())

    return result


# --------------------
# Streamlit UI
# --------------------

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")
st.title("📊 Personal Finance Tracker")

seed_sample_data()
# Load data
transactions = load_transactions()
df = transactions_to_df(transactions)

# Sidebar: Add transaction
st.sidebar.header("Add a transaction")
with st.sidebar.form("tx_form"):
    tx_type = st.selectbox("Type", ["income", "expense", "investment"])
    tx_date = st.date_input("Date", value=datetime.today())
    tx_amount = st.number_input("Amount", min_value=0.01, step=0.01, value=0.00, format="%.2f")
    tx_category = st.text_input("Category", value="General")
    tx_note = st.text_area("Note (optional)")

    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        try:
            amount_val = float(tx_amount)
            if amount_val <= 0:
                st.warning("Amount must be a positive number")
            else:
                date_str = tx_date.isoformat()

                if tx_type == "income":
                    tx = Income(date_str, amount_val, tx_category.strip(), tx_note.strip())
                elif tx_type == "expense":
                    tx = Expense(date_str, amount_val, tx_category.strip(), tx_note.strip())
                else:
                    tx = Investment(date_str, amount_val, tx_category.strip(), tx_note.strip())

                add_transaction(tx)
                st.success(f"{tx_type.title()} added: {amount_val} — {tx_category}")
                st.experimental_rerun()

        except ValueError:
            st.error("Please enter a valid numeric amount")

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Transactions")
    # Provide a main-area transaction form for better visibility
    with st.expander("Quick Add Transaction", expanded=True):
        with st.form("tx_form_main"):
            main_tx_type = st.selectbox("Type", ["income", "expense", "investment"], key="main_type")
            main_tx_date = st.date_input("Date", value=datetime.today(), key="main_date")
            main_tx_amount = st.number_input("Amount", min_value=0.01, step=0.01, value=0.00, format="%.2f", key="main_amount")
            main_tx_category = st.text_input("Category", value="General", key="main_category")
            main_tx_note = st.text_area("Note (optional)", key="main_note")
            main_submitted = st.form_submit_button("Add Transaction")
            if main_submitted:
                try:
                    amt = float(main_tx_amount)
                    if amt <= 0:
                        st.warning("Amount must be a positive number")
                    else:
                        date_str = main_tx_date.isoformat()
                        if main_tx_type == "income":
                            tx = Income(date_str, amt, main_tx_category.strip(), main_tx_note.strip())
                        elif main_tx_type == "expense":
                            tx = Expense(date_str, amt, main_tx_category.strip(), main_tx_note.strip())
                        else:
                            tx = Investment(date_str, amt, main_tx_category.strip(), main_tx_note.strip())
                        add_transaction(tx)
                        st.success(f"{main_tx_type.title()} added: {amt} — {main_tx_category}")
                        st.experimental_rerun()
                except ValueError:
                    st.error("Please enter a valid numeric amount")
    if df.empty:
        st.info("No transactions yet — add your first transaction from the sidebar.")
    else:
        display_df = df.copy()
        display_df["date"] = display_df["date"].dt.date
        st.dataframe(display_df.sort_values(by="date", ascending=False).reset_index(drop=True))

with col2:
    st.subheader("Quick Actions")
    if st.button("Reload Data"):
        st.experimental_rerun()

    # Always show CSV export if data exists
    if not df.empty:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv_bytes, file_name="transactions_export.csv", mime="text/csv")
    else:
        st.warning("No data to export")
    # Sample / admin actions
    st.markdown("---")
    if st.button("Add sample transaction"):
        # add a small sample expense for quick testing
        tx = Expense(datetime.today().isoformat(), 99.99, "Test", "Quick sample")
        add_transaction(tx)
        st.success("Sample transaction added")
        st.experimental_rerun()

    st.write("\n")
    if st.checkbox("I confirm clearing all data"):
        if st.button("Clear all transactions"):
            save_transactions([])
            st.success("All transactions cleared")
            st.experimental_rerun()

# Statistics and Insights
st.markdown("---")
stats = calculate_statistics(df)
insights = analyze_categories(df)

left, right = st.columns(2)
with left:
    st.subheader("Summary Statistics")
    st.metric("Total Income", f"{stats['total_income']:.2f}")
    st.metric("Total Expense", f"{stats['total_expense']:.2f}")
    st.metric("Total Investment", f"{stats['total_investment']:.2f}")
    st.metric("Net Balance", f"{stats['net_balance']:.2f}")
    st.metric("Savings %", f"{stats['savings_percentage']:.1f}%")

with right:
    st.subheader("Category Insights")
    st.write("Highest spending category:", insights["highest_spending_category"] or "—")
    st.write("Most frequent category:", insights["most_frequent_category"] or "—")
    st.write("Unique categories:")
    st.write(sorted(list(insights["unique_categories"] if insights["unique_categories"] else [])))

# Category totals chart
st.subheader("Category-wise Expense Totals")
if insights["category_totals"]:
    cat_df = pd.DataFrame(list(insights["category_totals"].items()), columns=["category", "amount"])
    cat_df = cat_df.sort_values(by="amount", ascending=False)
    st.bar_chart(cat_df.set_index("category"))
else:
    st.info("No expense category totals to display")

# Monthly totals and time series
st.markdown("---")
st.subheader("Monthly totals (income / expense / investment)")
if not df.empty:
    # monthly grouping - avoid modifying the main df; drop rows without valid date
    df_month = df.dropna(subset=["date"]).copy()
    df_month['month'] = df_month['date'].dt.to_period('M').dt.to_timestamp()
    monthly = df_month.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
    st.line_chart(monthly)
else:
    st.info("No data for monthly totals")

st.markdown("---")
st.subheader("Category breakdown (expenses)")
if insights["category_totals"]:
    pie_df = pd.DataFrame(list(insights['category_totals'].items()), columns=['category','amount'])
    pie_df = pie_df.sort_values(by='amount', ascending=False)
    # use st.bar_chart and st.pyplot (simple inline) — keep it simple
    st.bar_chart(pie_df.set_index('category'))
else:
    st.info("No expenses yet to show a category breakdown")

st.markdown("---")
st.subheader("Savings Goal")
goal_percent = st.slider("Monthly savings goal (% of income)", 0, 100, 20)

if stats["total_income"] <= 0:
    st.warning("No income recorded yet — cannot evaluate goal")
else:
    actual = round(stats["savings_percentage"], 2)
    st.write(f"Actual savings: {actual}% of income")

    if actual >= goal_percent:
        if actual >= goal_percent + 10:
            st.success(f"Amazing! You're well above your goal by {actual - goal_percent:.2f}%")
        else:
            st.success(f"Great job — you've met your goal by {actual - goal_percent:.2f}%")
    else:
        shortfall = goal_percent - actual
        if shortfall > 20:
            st.error(f"Significant shortfall: Increase savings by {shortfall:.2f}%")
        else:
            st.warning(f"You're under the goal by {shortfall:.2f}%. Try reducing expenses.")

# Category string analysis
st.markdown("---")
st.subheader("Category Name String Analysis")
cat_set = insights["unique_categories"] or set()
joined = ", ".join(sorted(cat_set))
joined_upper = joined.upper()
count_A = joined_upper.count("A")

st.write("Joined categories:", joined)
st.write("Uppercase:", joined_upper)
st.write("Number of letter 'A' in joined string:", count_A)

# Footer
st.markdown("---")
st.write("Tip: Data is stored locally in `transactions.json`. Keep a backup if needed.")

# Raw JSON viewer
with st.expander("Raw stored JSON"):
    st.write(transactions)
