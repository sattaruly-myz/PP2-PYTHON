import psycopg2
from config import DB_CONFIG


def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.OperationalError as e:
        print(f"Connection error: {e}")
        return None