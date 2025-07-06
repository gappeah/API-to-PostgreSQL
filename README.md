# API-to-PostgreSQL


📦 Project: CoffeeChain – Retail Inventory Sync

📖 Overview

This project demonstrates how to retrieve inventory data from a fictional RESTful API (https://api.coffeechain.io/v1/inventory) and insert the results into a PostgreSQL database. The scenario simulates an internal tool used by a mid-sized coffee chain to synchronise warehouse inventory with the central database every 24 hours.

While the project is fictional, the structure, tooling, and logic reflect common real-world business applications—such as internal ETL jobs, API integrations, or scheduled database sync tasks.

⸻

🔧 Tech Stack
	•	Python 3.11
	•	PostgreSQL 15
	•	requests for API calls
	•	psycopg2 for PostgreSQL interaction
	•	.env file for managing secrets

⸻

📂 Project Structure

coffeechain_inventory_sync/
│
├── main.py
├── db.py
├── config.py
├── requirements.txt
├── .env
└── README.md


⸻

📑 Sample .env

API_KEY=your_api_key_here
API_URL=https://api.coffeechain.io/v1/inventory
PG_HOST=localhost
PG_PORT=5432
PG_DB=coffeechain
PG_USER=postgres
PG_PASSWORD=yourpassword


⸻

🐍 main.py

from config import get_env_vars
from db import insert_inventory
import requests

def fetch_inventory(api_url, api_key):
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()['data']

def main():
    env = get_env_vars()
    inventory_data = fetch_inventory(env['API_URL'], env['API_KEY'])
    insert_inventory(inventory_data, env)

if __name__ == "__main__":
    main()


⸻

🐘 db.py

import psycopg2
from psycopg2.extras import execute_values

def insert_inventory(data, env):
    conn = psycopg2.connect(
        host=env['PG_HOST'],
        port=env['PG_PORT'],
        dbname=env['PG_DB'],
        user=env['PG_USER'],
        password=env['PG_PASSWORD']
    )

    with conn:
        with conn.cursor() as cur:
            query = """
            INSERT INTO inventory (sku, item_name, quantity, warehouse)
            VALUES %s
            ON CONFLICT (sku) DO UPDATE
            SET quantity = EXCLUDED.quantity;
            """
            values = [(item['sku'], item['item_name'], item['quantity'], item['warehouse']) for item in data]
            execute_values(cur, query, values)
    conn.close()


⸻

⚙️ config.py

from dotenv import load_dotenv
import os

def get_env_vars():
    load_dotenv()
    return {
        'API_URL': os.getenv('API_URL'),
        'API_KEY': os.getenv('API_KEY'),
        'PG_HOST': os.getenv('PG_HOST'),
        'PG_PORT': os.getenv('PG_PORT'),
        'PG_DB': os.getenv('PG_DB'),
        'PG_USER': os.getenv('PG_USER'),
        'PG_PASSWORD': os.getenv('PG_PASSWORD'),
    }


⸻

📦 requirements.txt

requests
psycopg2-binary
python-dotenv


⸻

🧪 Example Use Case

Intel’s fictional internal CoffeeChain brand uses this script as part of a nightly ETL workflow run on an Airflow DAG. The goal is to provide their analytics team with near-real-time stock data from 120+ franchise locations.

⸻

🚀 Running the Script

# 1. Set your .env variables
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the script
python main.py


⸻

🧼 Notes
	•	PostgreSQL must already have an inventory table with the following schema:

CREATE TABLE inventory (
    sku TEXT PRIMARY KEY,
    item_name TEXT,
    quantity INTEGER,
    warehouse TEXT
);

	•	Assumes API data format is:

{
  "data": [
    {"sku": "C1001", "item_name": "Dark Roast Beans", "quantity": 110, "warehouse": "Bristol"},
    ...
  ]
}


⸻
