import requests
import pandas as pd
import json
from pathlib import Path
import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine


def load_env_variables() -> dict[str, str]:
    required_env_variables = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
    config = {}
    for var in required_env_variables:
        config[var] = os.getenv(var)
        if not config[var]:
            raise EnvironmentError(f'Missing reuqired environment variable {var}')
    
    return config


def load_data(url: str) -> list[dict]:
   try:
        response = requests.get(url)
        logging.info('Extracted data from an API')
        return response.json()
   except requests.RequestException as e:
       logging.error(f'Failed to fetch data: {e}')
       raise 


def read_raw_data_from_json_file(filepath: Path) -> list[dict]:
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        logging.info(f'Loaded data from local file: {filepath}')
        return data
    except Exception as e:
        logging.error(f'Error reading from JSON file: {e}')
        raise

def extract_essential_data(data: list[dict]) -> list[dict]:
    return [{'country_name': entry['name']['common'], 
             'country_official_name': entry['name']['official'],
             'flag_png': entry['flags']['png'],
             'flag_desc': entry['flags']['alt'], 
             'population': entry['population'],
             'region': entry['region'],
             'area': entry['area']
            } for entry in data]


def convert_to_dataframe(data: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(data)


def write_raw_data_to_json_file(data: list[dict], filepath: Path):
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f)
        logging.info(f'Successfully written data to {filepath}')
    except Exception as e:
        logging.error(f'Error writing to a JSON file: {e}')
        raise 


def write_dataframe_to_db(df: pd.DataFrame, conn_string: str, table_name: str, if_exists='replace'):
    engine = create_engine(conn_string)
    try:
        with engine.connect() as connection:
            df.to_sql(table_name, con=connection, if_exists=if_exists, index=False, schema='public')
        logging.info(f'{len(df)} rows written to DB')
    except Exception as e:
        logging.error(f'Error writing to a database: {e}')
        raise
        

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    config = load_env_variables()

    DATA_DIR = Path.cwd() / 'data'
    RAW_FILE = DATA_DIR / 'raw' / 'countries_raw.json'
    fields_of_interest = ['name', 'flags', 'population', 'region', 'area']
    URL = f'https://restcountries.com/v3.1/all?fields={",".join(fields_of_interest)}'
    DB_TABLE_NAME = 'countries'

    if RAW_FILE.exists():
        data = read_raw_data_from_json_file(RAW_FILE)
    else:
        data = load_data(URL)
        RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
        write_raw_data_to_json_file(data, RAW_FILE)

    transformed_data = extract_essential_data(data)
    countries_df = convert_to_dataframe(transformed_data)

    conn_string = f'postgresql://{config["DB_USER"]}:{config["DB_PASSWORD"]}@{config["DB_HOST"]}:{config["DB_PORT"]}/{config["DB_NAME"]}'
    write_dataframe_to_db(countries_df, conn_string, DB_TABLE_NAME)