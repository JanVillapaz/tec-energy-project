import psycopg2
import requests
import logging
import pandas as pd
import os
from urllib.parse import quote
from datetime import datetime, timedelta
import numpy as np

DB_CONFIG = {
    'dbname': 'natural_gas_db',
    'user': "postgres",
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}
BASE_URL = "https://twtransfer.energytransfer.com/ipost/TW/capacity/operationally-available"
DATA_DIR = "data"

CYCLES = {
    0: "Timely",
    1: "Evening",
    3: "Intraday 1",
    4: "Intraday 2",
    7: "Intraday 3",
    5: "Final"
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("gas_data_pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def verify_data_directory():
    """
    Verifies that the data directory exists and creates it if it does not.
    """
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        logger.info("Data directory verified.")
    except Exception as e:
        logger.info(f"Data directory verification failed: {e}")


def verify_db_connection():
    """
    Verifies database connection and table existence.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        logger.info("Database connection successful.")

        # Verifies that table exists
        try:
            cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'gas_shipments');")
            table_exists = cur.fetchone()[0]
            if table_exists:
                logger.info("Table exists.")
            else:
                logger.warning("Table does not exist.")
        except psycopg2.Error as e:
            logger.error(f"Table check failed: {e}")
        
        # Close connections
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")


def fetch_csv_data(gas_day, cycle):
    """
    Fetches CSV data from the website 
    https://twtransfer.energytransfer.com/ipost/TW/capacity/operationally-available

    Args:
    gas_day (datetime): The date to fetch data for
    cycle (int): Cycle of the day to fetch data for

    Returns:
    path_file: The path of downloaded file
    """

    formatted_date = gas_day.strftime("%m/%d/%Y")
    cycle_name = CYCLES.get(cycle, str(cycle))


    # Log for debugging
    logger.info(f"Fetching data for {formatted_date} - {cycle_name}...")

    url = f"{BASE_URL}?f=csv&extension=csv&asset=TW&gasDay={quote(formatted_date)}&cycle={cycle}&searchType=NOM&searchString=&locType=ALL&locZone=ALL"
    file_name = f"{formatted_date.replace('/', '-')}_{cycle_name}.csv"
    file_path = os.path.join(DATA_DIR, file_name)
    
    response = requests.get(url, timeout=10)

    try:
        logger.info(f"Downloading {file_name}...")
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"Downloaded {file_name}.")
            return file_path
        else:
            logger.warning(f"Failed to download {file_name}.")
            return None
    except Exception as e:
        logger.error(f"Failed to download {file_name}: {e}")
        return None


def parse_csv(csv_path):
    """
    parse CSV To DataFrame
    
    Args:
    csv_path (str): The path of the CSV file to parse

    Returns:
    df: DataFrame of the CSV file
    """

    df = pd.read_csv(csv_path)

    # Clean and rename columns to match table schema
    df = df.rename(columns={
        "Loc": "loc",
        "Loc Zn": "loc_zn",
        "Loc Name": "loc_name",
        "Loc Purp Desc": "loc_purp_desc",
        "Loc/QTI": "loc_qti",
        "Flow Ind": "flow_ind",
        "DC": "dc",
        "OPC": "opc",
        "TSQ": "tsq",
        "OAC": "oac",
        "IT": "it",
        "Auth Overrun Ind": "auth_overrun_ind",
        "Nom Cap Exceed Ind": "nom_cap_exceed_ind",
        "All Qty Avail": "all_qty_avail",
        "Qty Reason": "qty_reason",
    })

    # Convert boolean columns to boolean type
    bool_columns = ["it", "auth_overrun_ind", "nom_cap_exceed_ind", "all_qty_avail"]
    for col in bool_columns:
        df[col] = df[col].map({"Y": True, "N": False})

    # Convert data types
    df["dc"] = pd.to_numeric(df["dc"], errors="coerce")
    df["opc"] = pd.to_numeric(df["opc"], errors="coerce")
    df["tsq"] = pd.to_numeric(df["tsq"], errors="coerce")
    df["oac"] = pd.to_numeric(df["oac"], errors="coerce")

    # Replace NaN values with None
    df = df.replace({np.nan: None})

    # Extract gas_day + cycle from filename
    df["gas_day"] = datetime.strptime(csv_path.split(os.sep)[-1].split("_")[0], "%m-%d-%Y").date()
    df["cycle"] = csv_path.split("_")[-1].replace(".csv", "")

    return df

    
def insert_into_db(df):
    """Inserts DataFrame into PostgreSQL"""

    # Log DataFrame for debugging
    logger.info(df)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    insert_query = """
    INSERT INTO gas_shipments (loc, loc_zn, loc_name, loc_purp_desc, loc_qti, flow_ind, dc, opc, tsq, oac, it, auth_overrun_ind, nom_cap_exceed_ind, all_qty_avail, qty_reason, gas_day, cycle)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
    """
    
    for _, row in df.iterrows():
        try:
            cur.execute(insert_query, tuple(row))
        except Exception as e:
            logger.error(f"Failed to insert row {tuple(row)}: {e}")

    conn.commit()
    cur.close()
    conn.close()

def main():
    logger.info("Starting data pipeline...")
    verify_data_directory()
    verify_db_connection()
    
    for i in range(3):  # Last 3 days
        date = datetime.today() - timedelta(days=i)
        for cycle in CYCLES.keys():
            csv_path = fetch_csv_data(date, cycle)
            if csv_path:
                df = parse_csv(csv_path)
                if df is not None:
                    insert_into_db(df)
    
    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()