import streamlit as st
import pandas as pd

# ==========================
# Load Data from Google Sheets
# ==========================
@st.cache_data
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/16uAUKfLbCOG7QtvBAAyVVaCfHL52NOZg/export?format=csv"
    df = pd.read_csv(sheet_url)
    return df

df = load_data()

st.set_page_config(page_title="Branchwise Loan Dashboard", layout="wide")
st.title("🏦 Branchwise Loan Dashboard")
st.markdown("This dashboard updates automatically whenever the Google Sheet is updated.")

# --------------------------
# Show raw data
# --------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(df)

# --------------------------
# Filters
# --------------------------
branches = df["Branch"].unique().tolist()
selected_branch = st.selectbox("Select Branch", ["All"] + branches)

status_list = df["Status"].unique().tolist()
selected_status = st.multiselect("Select Loan Status", status_list, default=status_list)

filtered_df = df.copy()
if selected_branch != "All":
    filtered_df = filtered_df[filtered_df["Branch"] == selected_branch]

if selected_status:
    filtered_df = filtered_df[filtered_df["Status"].isin(selected_status)]

# --------------------------
# 📊 Branchwise Loan Summary
# --------------------------
st.subheader("📊 Branch × Status Loan Summary")

summary_table = (
    filtered_df
    .groupby(["Branch", "Status"], as_index=False)
    .agg(Total_Loans=("Loan_ID", "count"),
         Total_Amount=("Loan_Amount", "sum"))
)

st.dataframe(summary_table)

# --------------------------
# 📈 Chart
# --------------------------
st.subheader("📈 Loan Amount by Branch")
chart_data = (
    filtered_df.groupby("Branch", as_index=False)["Loan_Amount"].sum()
)
st.bar_chart(chart_data.set_index("Branch"))
