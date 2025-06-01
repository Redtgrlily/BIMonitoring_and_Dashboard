# 🏦 Enterprise Batch Import Monitoring & Retry Dashboard

A data engineering demo project for ETL pipeline monitoring, with a modern dashboard that supports job retries, client-specific views, and interactive analytics. Built for fintech platforms that ingest and transform daily batch files from enterprise clients like banks and credit unions.

---

## 📌 Project Overview

This project simulates a production-grade batch ETL platform with:

- Python-based ETL pipeline that ingests CSV batch files
- SQL database schema for tracking imports
- Streamlit dashboard for clients to:
  - Monitor job performance
  - Filter by time, status, duration
  - Retry failed jobs by uploading corrected files
  - Export reports to CSV/PDF

---

## 🧱 Architecture

+-----------------------+ +------------------+ +---------------------+
| Client Uploads | —> S3 | ETL Job | —> DB | Job History Table |
+-----------------------+ +------------------+ +---------------------+
|
v
+-------------------+
| Streamlit Dashboard|
+-------------------+


- **Backend**: Python ETL w/ helper modules for parsing and database loading
- **Database**: PostgreSQL (simulated with SQLAlchemy schema)
- **Frontend**: Streamlit dashboard for monitoring & retry logic
- **Demo**: Mock data simulates real job runs, including failures

---

## 🚀 Features

| Feature                             | Status |
|-------------------------------------|--------|
| Batch file ETL logic                | ✅ Done |
| SQL schema for job and account data | ✅ Done |
| Streamlit dashboard                 | ✅ Done |
| Login & client-specific filtering   | ✅ Done |
| Time range and job duration filters | ✅ Done |
| Export reports to CSV and PDF       | ✅ Done |
| Retry failed jobs via file upload   | ✅ Done |
| Mock API simulating backend data    | ✅ Done |

---

## 🧪 Project Structure

project-root/
├── etl/
│ ├── batch_job.py # ETL orchestrator
│ ├── db.py # DB models and session
│ ├── parsers.py # Parsing logic
│ ├── helpers.py # Shared functions
│
├── dashboard/
│ ├── app.py # Streamlit dashboard app
│ ├── mock_api.py # Simulated job data + retry logic
│ └── requirements.txt # Dashboard dependencies
│
├── sql/
│ └── schema.sql # Raw SQL for table creation
├── data/ # Sample batch files
├── requirements.txt
└── README.md


---

## 🧰 Tech Stack

- **Python 3.9+**
- **Streamlit** – interactive client dashboard
- **Pandas** – data manipulation
- **Plotly** – visualizations
- **FPDF** – export reports to PDF
- **SQLAlchemy** – DB schema and connection
- **PostgreSQL** – target database

---

## 🧪 Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/your-username/batch-import-dashboard.git
cd batch-import-dashboard

2. ** Install Requirements **
```bash
pip install -r requirements.txt

3. ** Running the Dashboard **
```bash
streamlit run dashboard/app.py

Then visit http://localhost:8501 in your browser.
Login credentials
Username	Client View
bankcorp_admin	BankCorp
creditone_admin	CreditOne
fintrust_admin	FinTrust

Note: This is mock authentication for demo purposes only.

4. ** Reprocessing Failed Jobs **
Navigate to the "🛠️ Retry a Failed Job" section.

Select a failed job from the dropdown.

Upload a corrected CSV file.

Click "Reprocess Job" to simulate re-ingestion.

✅ A success message appears if the mock reprocess function accepts the file.

5. ** Exporting Data **
Export filtered job history to CSV or PDF using the export buttons.

## Example Use Cases ##

Internal dashboard for support teams to track ETL job health

Client-facing portal to allow reprocessing and transparency

MVP for building a multi-tenant data observability tool

##  Future Improvements
✅ Replace mock API with FastAPI or Flask backend

✅ Connect to real PostgreSQL data source

🔒 Real authentication + RBAC

📨 Email/SMS alerts on job failures

🔁 Automated job retry logic (via Lambda or Celery)

📦 Dockerize for deployment

## Author
Built by an aspiring Data Engineer focused on scalable data ingestion, monitoring, and self-serve tolling for enterprise clients.

## License
MIT License. Free to use and adapt.