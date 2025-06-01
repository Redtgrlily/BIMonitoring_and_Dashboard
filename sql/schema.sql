-- 1. Batch Jobs Table to track each import job
CREATE TABLE batch_jobs (
    job_id SERIAL PRIMARY KEY,
    client_id VARCHAR(50) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status VARCHAR(20) NOT NULL,  -- e.g. 'RUNNING', 'SUCCESS', 'FAILED'
    records_processed INT DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Accounts Table
CREATE TABLE accounts (
    account_id VARCHAR(50) PRIMARY KEY,
    client_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    account_type VARCHAR(50),
    open_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Account Details Table (balance, currency, last update)
CREATE TABLE account_details (
    account_detail_id SERIAL PRIMARY KEY,
    account_id VARCHAR(50) REFERENCES accounts(account_id),
    balance NUMERIC(18, 2),
    currency VARCHAR(10),
    last_updated TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Account Statuses Table
CREATE TABLE account_statuses (
    account_status_id SERIAL PRIMARY KEY,
    account_id VARCHAR(50) REFERENCES accounts(account_id),
    status VARCHAR(20),  -- e.g. 'OPEN', 'CLOSED', 'DORMANT'
    status_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Host Relations Table (link primary account to secondary users)
CREATE TABLE host_relations (
    relation_id SERIAL PRIMARY KEY,
    primary_account_id VARCHAR(50) REFERENCES accounts(account_id),
    secondary_user_id VARCHAR(50),
    relation_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Posted Transactions Table
CREATE TABLE posted_transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) REFERENCES accounts(account_id),
    amount NUMERIC(18, 2),
    transaction_date TIMESTAMP,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
