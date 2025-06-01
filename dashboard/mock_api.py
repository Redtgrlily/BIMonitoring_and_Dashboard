# dashboard/mock_api.py

import pandas as pd
from datetime import datetime, timedelta
import random

clients = ['BankCorp', 'CreditOne', 'FinTrust']
failed_job_records = {}

def get_mock_batch_jobs():
    jobs = []
    now = datetime.now()

    for i in range(100):
        client = random.choice(clients)
        start = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        duration = random.randint(1, 20)
        end = start + timedelta(minutes=duration)
        status = random.choices(['SUCCESS', 'FAILED'], weights=[0.9, 0.1])[0]
        job_id = f'job_{i}'
        
        jobs.append({
            'job_id': job_id,
            'client_id': client,
            'start_time': start,
            'end_time': end,
            'status': status,
            'records_processed': random.randint(1000, 50000)
        })

        if status == 'FAILED':
            failed_job_records[job_id] = None  # placeholder for uploaded fix

    return pd.DataFrame(jobs)

def reprocess_failed_job(job_id: str, df: pd.DataFrame) -> bool:
    """
    Simulates reprocessing a failed job. Returns True on success.
    """
    if job_id not in failed_job_records:
        return False
    
    if df.empty or 'account_id' not in df.columns:
        return False  # Simulate schema check failure
    
    failed_job_records[job_id] = df  # Save it as reprocessed
    return True