# etl/db.py

from sqlalchemy import (
    create_engine, Column, Integer, String, Date, DateTime, Numeric, Text, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class BatchJob(Base):
    __tablename__ = 'batch_jobs'

    job_id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(String(20), nullable=False)
    records_processed = Column(Integer, default=0)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(String(50), primary_key=True)
    client_id = Column(String(50), nullable=False)
    customer_id = Column(String(50), nullable=False)
    account_type = Column(String(50))
    open_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class AccountDetail(Base):
    __tablename__ = 'account_details'

    account_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String(50), ForeignKey('accounts.account_id'))
    balance = Column(Numeric(18, 2))
    currency = Column(String(10))
    last_updated = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class AccountStatus(Base):
    __tablename__ = 'account_statuses'

    account_status_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String(50), ForeignKey('accounts.account_id'))
    status = Column(String(20))
    status_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

class HostRelation(Base):
    __tablename__ = 'host_relations'

    relation_id = Column(Integer, primary_key=True, autoincrement=True)
    primary_account_id = Column(String(50), ForeignKey('accounts.account_id'))
    secondary_user_id = Column(String(50))
    relation_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class PostedTransaction(Base):
    __tablename__ = 'posted_transactions'

    transaction_id = Column(String(50), primary_key=True)
    account_id = Column(String(50), ForeignKey('accounts.account_id'))
    amount = Column(Numeric(18, 2))
    transaction_date = Column(DateTime)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# Database session factory
def get_engine(user, password, host, port, dbname):
    return create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}')

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
