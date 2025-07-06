# db.py
# Handles insertion of CoffeeChain warehouse stock into the PostgreSQL DB.
# Assumes all SKUs are globally unique across all CoffeeChain branches.

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
            # Simulated payload: [{'sku': 'C1001', 'item_name': 'Dark Roast', ...}]
            values = [
                (item['sku'], item['item_name'], item['quantity'], item['warehouse'])
                for item in data
            ]
            execute_values(cur, query, values)
            print(f"[INFO] Inserted/Updated {len(values)} inventory items.")

    conn.close()
