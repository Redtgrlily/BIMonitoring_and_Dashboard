import pandas as pd

def load_csv(filepath, expected_columns, dtypes):
    """
    Load CSV file, ensure columns, and apply dtypes.
    """
    df = pd.read_csv(filepath, usecols=expected_columns)
    for col, dtype in dtypes.items():
        if dtype == 'datetime64[ns]':
            df[col] = pd.to_datetime(df[col], errors='coerce')
        else:
            df[col] = df[col].astype(dtype, errors='ignore')
    return df

def validate_required_columns(df, required_columns):
    """
    Validate that required columns have no missing values.
    """
    missing = [col for col in required_columns if df[col].isnull().any()]
    if missing:
        raise ValueError(f"Missing required data in columns: {missing}")
    
def clean_string_columns(df):
    """
    Strip whitespace from string columns.
    """
    str_cols = df.select_dtypes(include='object').columns
    for col in str_cols:
        df[col] = df[col].str.strip()
    return df