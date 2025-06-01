# etl/batch_job.py
from etl.parsers import parse_file
from etl.db import get_engine, get_session, Base
from etl.db_loader import (
    upsert_accounts, upsert_account_details, insert_account_statuses,
    upsert_host_relations, upsert_posted_transactions
)
from datetime import datetime

def process_batch_and_load(files_dict, db_session, client_id='default_client'):
    job_start = datetime.utcnow()
    job_status = 'RUNNING'
    records_processed = 0

    try:
        batch_data = {}
        for file_type, filepath in files_dict.items():
            print(f"Parsing {file_type} from {filepath}")
            df = parse_file(filepath, file_type)
            # Inject client_id where relevant
            if 'client_id' not in df.columns:
                df['client_id'] = client_id
            batch_data[file_type] = df
            records_processed += len(df)
            print(f"Loaded {len(df)} records for {file_type}")

        # Load into DB
        upsert_accounts(db_session, batch_data['accounts'])
        upsert_account_details(db_session, batch_data['account_details'])
        insert_account_statuses(db_session, batch_data['account_statuses'])
        upsert_host_relations(db_session, batch_data['host_relations'])
        upsert_posted_transactions(db_session, batch_data['posted_transactions'])

        job_status = 'SUCCESS'

    except Exception as e:
        job_status = 'FAILED'
        error_message = str(e)
        print(f"Batch job failed: {error_message}")

    job_end = datetime.utcnow()

    # Record batch job metadata
    from etl.db import BatchJob
    batch_job_record = BatchJob(
        client_id=client_id,
        start_time=job_start,
        end_time=job_end,
        status=job_status,
        records_processed=records_processed,
        error_message=error_message if job_status == 'FAILED' else None
    )
    db_session.add(batch_job_record)
    db_session.commit()
    print(f"Batch job ended with status {job_status}, processed {records_processed} records")

if __name__ == "__main__":
    # Example usage
    engine = get_engine('your_user', 'your_password', 'localhost', 5432, 'your_db')
    Base.metadata.create_all(engine)
    session = get_session(engine)

    files = {
        'accounts': 'data/accounts.csv',
        'account_details': 'data/account_details.csv',
        'account_statuses': 'data/account_statuses.csv',
        'host_relations': 'data/host_relations.csv',
        'posted_transactions': 'data/posted_transactions.csv',
    }

    process_batch_and_load(files, session, client_id='bank_123')