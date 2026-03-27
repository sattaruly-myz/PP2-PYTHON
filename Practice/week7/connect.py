import psycopg2
from config import DB_CONFIG


def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.OperationalError as e:
        print(f"Connection error: {e}")
        return None


def create_table():
    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS phonebook (
                        id    SERIAL PRIMARY KEY,
                        name  VARCHAR(100) NOT NULL,
                        phone VARCHAR(20)  NOT NULL UNIQUE
                    );
                """)
        print("Table ready.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
