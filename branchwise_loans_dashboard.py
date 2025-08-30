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

# ==========================
# Streamlit App
# ==========================
st.set_page_config(page_title="Branchwise Loan Dashboard", layout="wide")

st.title("🏦 Branchwise Loan Dashboard")
st.markdown("This dashboard updates automatically whenever the Google Sheet is updated.")

# Show raw data
with st.expander("📄 View Raw Data"):
    st.dataframe(df)

# ==========================
# Filters
# ==========================
branches = df["Branch"].unique().tolist()
selected_branch = st.selectbox("Select Branch", ["All"] + branches)

status_list = df["Status"].unique().tolist()
selected_status = st.multiselect("Select Loan Status", status_list, default=status_list)

# Apply filters
filtered_df = df.copy()

if selected_branch != "All":
    filtered_df = filtered_df[filtered_df["Branch"] == selected_branch]

if selected_status:
    filtered_df = filtered_df[filtered_df["Status"].isin(selected_status)]

# ==========================
# Summary KPIs
# ==========================
st.subheader("📊 Summary")
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Loans", len(filtered_df))
with col2:
    st.metric("Total Loan Amount", f"{filtered_df['LoanAmount'].sum():,.2f}")

# ==========================
# Branchwise Aggregation
# ==========================
st.subheader("🏢 Branchwise Loan Amount")
branch_summary = (
    filtered_df.groupby("Branch", as_index=False)["LoanAmount"].sum()
)

st.dataframe(branch_summary)

# ==========================
# Chart
# ==========================
st.subheader("📈 Loan Amount by Branch")
st.bar_chart(branch_summary.set_index("Branch"))

