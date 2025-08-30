import streamlit as st
import pandas as pd

st.set_page_config(page_title="Branchwise Loan Dashboard", layout="wide")

# Path to your Excel file
excel_file = r"branchwise_loans.xlsx"

# Load data function with cache + refresh
@st.cache_data(ttl=30)  # refresh every 30 seconds
def load_data():
    return pd.read_excel(excel_file)

df = load_data()

# Dashboard Title
st.title("🏦 Branchwise Loan Dashboard")

# ========== KPI Metrics ==========
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Loan Amount", f"₹{df['Loan_Amount'].sum():,.0f}")
with col2:
    st.metric("Number of Loans", df["Loan_ID"].nunique())

# ========== Branchwise Summary Table ==========
st.subheader("📋 Branchwise Loan Summary")

summary_table = df.groupby(["Branch", "Status"], as_index=False).agg(
    Total_Loan_Amount=("Loan_Amount", "sum"),
    Number_of_Loans=("Loan_ID", "nunique")
)

st.dataframe(summary_table, use_container_width=True)

st.caption("🔄 This table refreshes every 30 seconds. Add new data in Excel to see updates.")


