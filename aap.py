import streamlit as st
import json
import os
from datetime import date
import pandas as pd
import altair as alt
from sklearn.linear_model import LinearRegression
import numpy as np

# --------------------- CSS ---------------------
st.markdown("""
<style>
body {background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 100%);}
h1 {text-align:center; font-family: 'Segoe UI', sans-serif; color:#2a2a2a; font-weight:900;}
.metric-card {padding:25px; border-radius:18px; color:white; font-weight:bold; text-align:center; margin-bottom:15px; font-size:20px; box-shadow:1px 4px 18px rgba(0,0,0,0.2); transition: transform 0.2s;}
.metric-card:hover {transform: scale(1.05);}
.income-card { background: linear-gradient(135deg, #00c853, #b9f6ca);}
.expense-card { background: linear-gradient(135deg, #d50000, #ff8a80);}
.invest-card { background: linear-gradient(135deg, #1a237e, #7986cb);}
.balance-card { background: linear-gradient(135deg, #ff6d00, #ffd180);}
.forecast-card { background: linear-gradient(135deg, #ff4081, #f8bbd0);}
.sidebar .sidebar-header {color:#333333; font-weight:bold; font-size:18px; margin-bottom:5px;}
</style>
""", unsafe_allow_html=True)

# --------------------- OOP ---------------------
class Transaction:
    def __init__(self, date, amount, category, note):
        self.date = date
        self.amount = amount
        self.category = category
        self.note = note

class Income(Transaction): type="income"
class Expense(Transaction): type="expense"
class Investment(Transaction): type="investment"

# --------------------- Data ---------------------
FILE = "finance_data.json"
def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []
def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()

# --------------------- Page ---------------------
st.set_page_config(page_title="PFTS Dashboard", layout="wide")
st.title("💸 PFTS – Personal Finance Tracking System")

# --------------------- Sidebar: Add Transaction ---------------------
st.sidebar.markdown("### ➕ Add Transaction")
with st.sidebar.form("entry_form"):
    t_type = st.selectbox("Transaction Type", ["Income","Expense","Investment"])
    t_date = st.date_input("Date", date.today())
    t_amount = st.number_input("Amount", min_value=1.0, format="%.2f")
    t_category = st.text_input("Category")
    t_note = st.text_area("Note (optional)")
    submitted = st.form_submit_button("Add Transaction")
    if submitted:
        if t_type=="Income": obj=Income(str(t_date), t_amount, t_category, t_note)
        elif t_type=="Expense": obj=Expense(str(t_date), t_amount, t_category, t_note)
        else: obj=Investment(str(t_date), t_amount, t_category, t_note)
        entry={"type":obj.type,"date":obj.date,"amount":obj.amount,"category":obj.category,"note":obj.note}
        data.append(entry)
        save_data(data)
        st.success("✅ Transaction Added!")

# --------------------- Sidebar: CSV Upload/Download ---------------------
st.sidebar.markdown("### 📤 Upload / Download CSV")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    new_df = pd.read_csv(uploaded_file)
    data.extend(new_df.to_dict(orient="records"))
    save_data(data)
    st.sidebar.success("✅ CSV Imported!")

# --------------------- Sidebar: Filters ---------------------
st.sidebar.markdown("### 🔍 Filters")
df = pd.DataFrame(data)
if df.empty: df=pd.DataFrame(columns=["type","date","amount","category","note"])
df["date"]=pd.to_datetime(df["date"])
type_filter=st.sidebar.multiselect("Transaction Type", options=df["type"].unique(), default=df["type"].unique())
category_filter=st.sidebar.multiselect("Category", options=df["category"].unique(), default=df["category"].unique())
min_date=df["date"].min() if not df.empty else pd.to_datetime("2020-01-01")
max_date=df["date"].max() if not df.empty else pd.to_datetime(date.today())
date_filter=st.sidebar.date_input("Date Range",[min_date,max_date])

filtered_df=df[
    (df["type"].isin(type_filter)) &
    (df["category"].isin(category_filter)) &
    (df["date"]>=pd.to_datetime(date_filter[0])) &
    (df["date"]<=pd.to_datetime(date_filter[1]))
]

# CSV Download
csv_export=filtered_df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button("📥 Download Transactions CSV", data=csv_export, file_name="transactions.csv", mime="text/csv")

# --------------------- Metrics ---------------------
total_income=filtered_df[filtered_df["type"]=="income"]["amount"].sum()
total_expense=filtered_df[filtered_df["type"]=="expense"]["amount"].sum()
total_invest=filtered_df[filtered_df["type"]=="investment"]["amount"].sum()
balance=total_income-total_expense

col1,col2,col3,col4=st.columns(4)
col1.markdown(f"<div class='metric-card income-card'>💰 Income<br>₹ {total_income:.2f}</div>",unsafe_allow_html=True)
col2.markdown(f"<div class='metric-card expense-card'>🛒 Expenses<br>₹ {total_expense:.2f}</div>",unsafe_allow_html=True)
col3.markdown(f"<div class='metric-card invest-card'>📈 Investment<br>₹ {total_invest:.2f}</div>",unsafe_allow_html=True)
col4.markdown(f"<div class='metric-card balance-card'>💵 Balance<br>₹ {balance:.2f}</div>",unsafe_allow_html=True)

# --------------------- Pie Chart ---------------------
st.subheader("📊 Income vs Expenses Pie Chart")
if total_income+total_expense>0:
    pie_df=pd.DataFrame({"Type":["Income","Expenses"],"Amount":[total_income,total_expense]})
    pie_chart=alt.Chart(pie_df).mark_arc(innerRadius=50).encode(
        theta="Amount", color="Type", tooltip=["Type","Amount"]
    )
    st.altair_chart(pie_chart,use_container_width=True)
else: st.info("No data yet to show pie chart.")

# --------------------- Category Bar Chart ---------------------
st.subheader("📊 Category Wise Spending")
if not filtered_df.empty and filtered_df["amount"].sum()>0:
    category_totals=filtered_df.groupby("category")["amount"].sum().reset_index()
    bar_chart=alt.Chart(category_totals).mark_bar().encode(
        x="category", y="amount", color="category", tooltip=["category","amount"]
    )
    st.altair_chart(bar_chart,use_container_width=True)
else: st.info("No data for category chart yet.")

# --------------------- Monthly Trend ---------------------
st.subheader("📈 Monthly Trend")
if not filtered_df.empty:
    filtered_df["month"]=filtered_df["date"].dt.to_period("M").astype(str)
    monthly_summary=filtered_df.groupby(["month","type"])["amount"].sum().reset_index()
    line_chart=alt.Chart(monthly_summary).mark_line(point=True).encode(
        x="month", y="amount", color="type", tooltip=["month","type","amount"]
    )
    st.altair_chart(line_chart,use_container_width=True)
else:
    st.info("No data for monthly trends yet.")

# --------------------- Forecast Next Month ---------------------
st.subheader("🔮 Forecast Next Month")
forecast_data=[]
for t in ["income","expense"]:
    temp=monthly_summary[monthly_summary["type"]==t].copy() if not filtered_df.empty else pd.DataFrame()
    if len(temp)>1:
        temp["month_num"]=range(len(temp))
        X=temp[["month_num"]]
        y=temp["amount"]
        model=LinearRegression().fit(X,y)
        next_month_num=np.array([[len(temp)]])
        pred=int(model.predict(next_month_num)[0])
        forecast_data.append((t,pred))
    else:
        forecast_data.append((t,temp["amount"].sum() if not temp.empty else 0))

forecast_income=[x[1] for x in forecast_data if x[0]=="income"][0]
forecast_expense=[x[1] for x in forecast_data if x[0]=="expense"][0]
forecast_balance=forecast_income-forecast_expense

col1,col2,col3=st.columns(3)
col1.markdown(f"<div class='metric-card forecast-card'>📈 Forecast Income<br>₹ {forecast_income:.2f}</div>",unsafe_allow_html=True)
col2.markdown(f"<div class='metric-card forecast-card'>📉 Forecast Expense<br>₹ {forecast_expense:.2f}</div>",unsafe_allow_html=True)
col3.markdown(f"<div class='metric-card forecast-card'>💵 Forecast Balance<br>₹ {forecast_balance:.2f}</div>",unsafe_allow_html=True)

# --------------------- Savings Goal ---------------------
st.subheader("🎯 Savings Goal")
goal=st.slider("Set Monthly Savings Goal (%)",1,80,20)
if total_income>0:
    savings_pct=(balance/total_income)*100
    if savings_pct>=goal:
        st.success(f"Great! You saved {savings_pct:.2f}% – above your goal 🎉")
    else:
        st.warning(f"You saved {savings_pct:.2f}% – below your goal 😟")
else: st.info("Add income to calculate savings goal.")

# --------------------- String Analysis ---------------------
categories_set=set(filtered_df["category"].unique())
joined=", ".join(categories_set).upper()
count_a=joined.count("A")
st.subheader("🔤 Category Name Analysis")
st.write(f"**All categories (uppercase):** {joined}")
st.write(f"**Number of 'A' letters:** {count_a}")

# --------------------- Raw Table ---------------------
st.subheader("📄 Filtered Transactions")
st.dataframe(filtered_df)
