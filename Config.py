# config.py
# Loads API and database secrets for the CoffeeChain sync tool.

from dotenv import load_dotenv
import os

def get_env_vars():
    load_dotenv()
    return {
        'API_URL': os.getenv('API_URL'),  # e.g. https://api.coffeechain.io/v1/inventory
        'API_KEY': os.getenv('API_KEY'),
        'PG_HOST': os.getenv('PG_HOST'),
        'PG_PORT': os.getenv('PG_PORT'),
        'PG_DB': os.getenv('PG_DB'),
        'PG_USER': os.getenv('PG_USER'),
        'PG_PASSWORD': os.getenv('PG_PASSWORD'),
    }
