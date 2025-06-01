# etl/db_loader.py
from sqlalchemy.dialects.postgresql import insert
from etl.db import (
    Account, AccountDetail, AccountStatus, HostRelation, PostedTransaction, BatchJob
)

def upsert_accounts(session, df_accounts):
    """
    Upsert accounts DataFrame into accounts table.
    """
    for _, row in df_accounts.iterrows():
        stmt = insert(Account).values(
            account_id=row['account_id'],
            client_id=row.get('client_id', 'default_client'),
            customer_id=row['customer_id'],
            account_type=row.get('account_type'),
            open_date=row.get('open_date'),
            updated_at=datetime.utcnow()
        ).on_conflict_do_update(
            index_elements=['account_id'],
            set_={
                'customer_id': row['customer_id'],
                'account_type': row.get('account_type'),
                'open_date': row.get('open_date'),
                'updated_at': datetime.utcnow()
            }
        )
        session.execute(stmt)
    session.commit()

def upsert_account_details(session, df_details):
    for _, row in df_details.iterrows():
        stmt = insert(AccountDetail).values(
            account_id=row['account_id'],
            balance=row['balance'],
            currency=row.get('currency'),
            last_updated=row.get('last_updated'),
            updated_at=datetime.utcnow()
        ).on_conflict_do_update(
            index_elements=['account_id'],
            set_={
                'balance': row['balance'],
                'currency': row.get('currency'),
                'last_updated': row.get('last_updated'),
                'updated_at': datetime.utcnow()
            }
        )
        session.execute(stmt)
    session.commit()

def insert_account_statuses(session, df_statuses):
    # Status history usually append-only, so insert without upsert
    for _, row in df_statuses.iterrows():
        status = AccountStatus(
            account_id=row['account_id'],
            status=row['status'],
            status_date=row.get('status_date'),
        )
        session.add(status)
    session.commit()

def upsert_host_relations(session, df_relations):
    # Assuming no unique constraint, insert all
    for _, row in df_relations.iterrows():
        relation = HostRelation(
            primary_account_id=row['primary_account_id'],
            secondary_user_id=row['secondary_user_id'],
            relation_type=row.get('relation_type')
        )
        session.add(relation)
    session.commit()

def upsert_posted_transactions(session, df_transactions):
    for _, row in df_transactions.iterrows():
        stmt = insert(PostedTransaction).values(
            transaction_id=row['transaction_id'],
            account_id=row['account_id'],
            amount=row['amount'],
            transaction_date=row.get('transaction_date'),
            description=row.get('description')
        ).on_conflict_do_update(
            index_elements=['transaction_id'],
            set_={
                'account_id': row['account_id'],
                'amount': row['amount'],
                'transaction_date': row.get('transaction_date'),
                'description': row.get('description')
            }
        )
        session.execute(stmt)
    session.commit()
