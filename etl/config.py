PARSING_CONFIGS = {
    'accounts': {
        'columns': ['account_id', 'customer_id', 'account_type', 'open_date'],
        'dtypes': {
            'account_id': str,
            'customer_id': str,
            'account_type': str,
            'open_date': 'datetime64[ns]'
        },
        'required': ['account_id','customer_id']
    },
    'account_details': {
        'columns': ['account_id', 'balance', 'currency', 'last_updated'],
        'dtypes': {
            'account_id': str,
            'balance': float,
            'currency': str,
            'last_updated': 'datetime64[ns]'
        },
        'required': ['account_id', 'balance']
    },
    'account_statuses': {
        'columns': ['account_id', 'status', 'status_date'],
        'dtypes': {
            'account_id': str,
            'status': str,
            'status_date': 'datetime64[ns]'
        },
        'required': ['account_id', 'status']
    },
    'host_relations': {
        'columns': ['primary_account_id', 'secondary_user_id', 'relation_type'],
        'dtypes': {
            'primary_account_id': str,
            'secondary_user_id': str,
            'relation_type': str
        },
        'required': ['primary_account_id', 'secondary_user_id']
    },
    'posted_transactions': {
        'columns': ['transaction_id', 'account_id', 'amount', 'transaction_date', 'description'],
        'dtypes': {
            'transaction_id': str,
            'account_id': str,
            'amount': float,
            'transaction_date': 'datetime64[ns]',
            'description': str
        },
        'required': ['transaction_id', 'account_id', 'amount']
    }
}