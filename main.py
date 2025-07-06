# Project: CoffeeChain Inventory Sync Tool
# Description: Pulls daily inventory data from the CoffeeChain warehouse API
# and updates a central PostgreSQL database used by Intel Ventures' Retail Analytics Division.

from config import get_env_vars
from db import insert_inventory
import requests

def fetch_inventory(api_url, api_key):
    """
    Fetches inventory data from the fictional CoffeeChain API.
    Example URL: https://api.coffeechain.io/v1/inventory
    """
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"[ERROR] API request failed with status {response.status_code}")
    
    print("[INFO] Inventory data fetched successfully.")
    return response.json()['data']

def main():
    env = get_env_vars()
    print("[INFO] Starting CoffeeChain sync job.")
    inventory_data = fetch_inventory(env['API_URL'], env['API_KEY'])
    insert_inventory(inventory_data, env)
    print("[INFO] Sync complete. Inventory successfully loaded into PostgreSQL.")

if __name__ == "__main__":
    main()
