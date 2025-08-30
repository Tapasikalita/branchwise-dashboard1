import streamlit as st
import pandas as pd

# -----------------------------
# Load data from Google Sheets
# -----------------------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/16uAUKfLbCOG7QtvBAAyVVaCfHL52NOZg/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

# Add button to refresh data
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()

# Load the data
df = load_data()

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("🏦 Branchwise Loan Dashboard")
st.caption("This dashboard updates automatically from Google Sheets. Use the Refresh button if you added new rows.")

# -----------------------------
# Raw Data Viewer
# -----------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(df)

# -----------------------------
# Filters
# -----------------------------
branches = ["All"] + sorted(df["Branch"].dropna().unique().tolist())
statuses = ["All"] + sorted(df["Status"].dropna().unique().tolist())

branch_choice = st.selectbox("Select Branch", branches)
status_choice = st.selectbox("Select Loan Status", statuses)

filtered_df = df.copy()
if branch_choice != "All":
    filtered_df = filtered_df[filtered_df["Branch"] == branch_choice]
if status_choice != "All":
    filtered_df = filtered_df[filtered_df["Status"] == status_choice]

# -----------------------------
# Summary Metrics
# -----------------------------
st.subheader("📊 Summary")

total_loans = filtered_df.shape[0]
total_amount = filtered_df["Loan_Amount"].sum()

col1, col2 = st.columns(2)
col1.metric("Total Loans", total_loans)
col2.metric("Total Loan Amount", f"{total_amount:,.2f}")

# -----------------------------
# Branchwise Table
# -----------------------------
st.subheader("🏢 Branchwise Loan Summary")

branch_summary = (
    filtered_df.groupby(["Branch", "Status"], as_index=False)
    .agg({"Loan_Amount": "sum", "Loan_ID": "count"})
    .rename(columns={"Loan_ID": "No_of_Loans"})
)

st.dataframe(branch_summary)
