# dashboard/app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from mock_api import get_mock_batch_jobs
from datetime import datetime
from io import BytesIO
from fpdf import FPDF

st.set_page_config(layout="wide", page_title="Batch Import Dashboard")

# ---------------------------------------
# Mock Authentication
# ---------------------------------------
users = {
    "bankcorp_admin": "BankCorp",
    "creditone_admin": "CreditOne",
    "fintrust_admin": "FinTrust",
}

with st.sidebar:
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

# Mock login logic
if not (username and password and username in users):
    st.warning("Please login to continue.")
    st.stop()

client_view = users[username]
st.sidebar.success(f"Logged in as: {client_view}")

# ---------------------------------------
# Load and Filter Data
# ---------------------------------------
df = get_mock_batch_jobs()
df['duration_minutes'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60
df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

# Filter to user's client
df = df[df['client_id'] == client_view]

# Sidebar Filters
with st.sidebar:
    st.header("📅 Filters")

    status_filter = st.selectbox("Job Status", ['All', 'SUCCESS', 'FAILED'])
    if status_filter != 'All':
        df = df[df['status'] == status_filter]

    # Time range filter
    min_date = df['start_time'].min().date()
    max_date = df['start_time'].max().date()
    date_range = st.date_input("Select Date Range", [min_date, max_date])
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['start_time'].dt.date >= start_date) & (df['start_time'].dt.date <= end_date)]

    # Duration filter
    duration_range = st.slider("Job Duration (minutes)", 0, int(df['duration_minutes'].max()), (0, 20))
    df = df[(df['duration_minutes'] >= duration_range[0]) & (df['duration_minutes'] <= duration_range[1])]

# ---------------------------------------
# Main Dashboard
# ---------------------------------------
st.title("📊 Batch Import Dashboard")
st.subheader(f"Welcome, {client_view}")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(df))
col2.metric("Success Rate", f"{(df['status'] == 'SUCCESS').mean() * 100:.1f}%")
col3.metric("Avg Duration (min)", f"{df['duration_minutes'].mean():.2f}")

st.divider()

# Charts
st.subheader("📈 Records Processed Over Time")
df['date'] = df['start_time'].dt.date
daily = df.groupby('date')['records_processed'].sum().reset_index()
fig = px.line(daily, x='date', y='records_processed', title="Records Processed per Day")
st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Recent Jobs")
st.dataframe(df.sort_values('start_time', ascending=False).head(10), use_container_width=True)

# ---------------------------------------
# Export Options
# ---------------------------------------
st.subheader("📤 Export")

col1, col2 = st.columns(2)

# Export to CSV
csv = df.to_csv(index=False).encode('utf-8')
col1.download_button("⬇️ Download CSV", data=csv, file_name=f"{client_view}_jobs.csv", mime='text/csv')

# Export to PDF
def convert_df_to_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Batch Job Report", ln=True, align='C')
    pdf.ln(10)

    # Headers
    headers = dataframe.columns.tolist()
    for header in headers:
        pdf.cell(30, 8, txt=str(header)[:12], border=1)
    pdf.ln()

    # Rows
    for i, row in dataframe.iterrows():
        for item in row:
            pdf.cell(30, 8, txt=str(item)[:12], border=1)
        pdf.ln()

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

pdf_bytes = convert_df_to_pdf(df.head(20))  # Limit to 20 rows for layout
col2.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=f"{client_view}_jobs.pdf", mime='application/pdf')

# ---------------------------------------
# File Upload & Retry Section
# ---------------------------------------
st.subheader("🛠️ Retry a Failed Job")

failed_jobs = df[df['status'] == 'FAILED']
if failed_jobs.empty:
    st.info("✅ No failed jobs to retry.")
else:
    selected_job = st.selectbox("Select a failed job", failed_jobs['job_id'].tolist())

    uploaded_file = st.file_uploader("Upload corrected file (CSV)", type=['csv'], key='file_retry')

    if uploaded_file and st.button("Reprocess Job"):
        try:
            retry_df = pd.read_csv(uploaded_file)

            from mock_api import reprocess_failed_job
            success = reprocess_failed_job(selected_job, retry_df)

            if success:
                st.success(f"✅ Job {selected_job} was successfully reprocessed!")
            else:
                st.error("❌ Reprocessing failed. File may be invalid or job not found.")
        except Exception as e:
            st.error(f"❌ Error reading CSV: {str(e)}")
