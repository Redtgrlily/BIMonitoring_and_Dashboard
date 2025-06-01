from etl.helpers import load_csv, validate_required_columns, clean_string_columns
from etl.config import PARSING_CONFIGS

def parse_file(filepath, file_type):
    config = PARSING_CONFIGS[file_type]
    df = load_csv(filepath, config['columns'], config['dtypes'])
    df = clean_string_columns(df)
    validate_required_columns(df, config['required'])
    # Additional file-type specific parsing logic can go here
    return df