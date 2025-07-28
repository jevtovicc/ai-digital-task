import requests
import pandas as pd
import json
import psycopg2
from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


def extract_essential_data(data: list[dict]) -> list[dict]:
    return [{'country_name': entry['name']['common'], 
             'country_official_name': entry['name']['official'],
             'flag_png': entry['flags']['png'],
             'flag_desc': entry['flags']['alt'], 
             'population': entry['population']
            } for entry in data]


def convert_to_dataframe(data: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(data)


def write_raw_data_to_json_file(data: list[dict], filepath: Path):
    with open(filepath, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    DATA_DIR = Path.cwd() / 'data'
    RAW_DIR = DATA_DIR / 'raw'
    URL = 'https://restcountries.com/v3.1/all?fields=name,flags,population'

    response = requests.get(URL)
    data = response.json()

    write_raw_data_to_json_file(data, RAW_DIR / 'countries_raw.json')

    res = extract_essential_data(data)
    countries_df = convert_to_dataframe(res)

    load_dotenv()

    DB_USER = os.getenv('DB_USER')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT= os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    conn_string = f'postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(conn_string)
    countries_df.to_sql("countries", engine, if_exists="replace", index=False)