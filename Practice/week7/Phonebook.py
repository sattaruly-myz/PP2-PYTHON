import csv
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "phonebook_db",
    "user": "postgres",
    "password": 230508
}


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
    finally:
        conn.close()


def _print_rows(rows):
    if not rows:
        print("No results.")
        return
    print(f"\n  {'ID':<5} {'Name':<25} {'Phone'}")
    print("  " + "-" * 45)
    for row in rows:
        print(f"  {row[0]:<5} {row[1]:<25} {row[2]}")


def insert_from_console():
    name  = input("Name: ").strip()
    phone = input("Phone: ").strip()
    if not name or not phone:
        print("Name and phone cannot be empty.")
        return
    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO phonebook (name, phone) VALUES (%s, %s);",
                    (name, phone)
                )
        print(f"Added '{name}'.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def insert_from_csv(filepath="contacts.csv"):
    try:
        with open(filepath, encoding="utf-8") as f:
            rows = [(r["name"].strip(), r["phone"].strip()) for r in csv.DictReader(f)]
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
        return
    conn = get_connection()
    if not conn:
        return
    added, skipped = 0, 0
    try:
        with conn:
            with conn.cursor() as cur:
                for name, phone in rows:
                    try:
                        cur.execute(
                            "INSERT INTO phonebook (name, phone) VALUES (%s, %s);",
                            (name, phone)
                        )
                        added += 1
                    except Exception:
                        conn.rollback()
                        skipped += 1
        print(f"Added: {added}, skipped (duplicates): {skipped}.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def show_all():
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, phone FROM phonebook ORDER BY name;")
            rows = cur.fetchall()
        print(f"\nTotal: {len(rows)}")
        _print_rows(rows)
    finally:
        conn.close()


def search_by_name():
    name = input("Name (or part): ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, phone FROM phonebook WHERE name ILIKE %s ORDER BY name;",
                (f"%{name}%",)
            )
            _print_rows(cur.fetchall())
    finally:
        conn.close()


def search_by_phone_prefix():
    prefix = input("Phone prefix (e.g. +7701): ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, phone FROM phonebook WHERE phone LIKE %s ORDER BY phone;",
                (f"{prefix}%",)
            )
            _print_rows(cur.fetchall())
    finally:
        conn.close()


def update_contact():
    name = input("Search name to update: ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, phone FROM phonebook WHERE name ILIKE %s;",
                (f"%{name}%",)
            )
            rows = cur.fetchall()
        if not rows:
            print("Not found.")
            return
        _print_rows(rows)
        contact_id = input("Enter ID to update: ").strip()
        print("1 - Name  2 - Phone")
        choice = input("Choice: ").strip()
        with conn:
            with conn.cursor() as cur:
                if choice == "1":
                    new_val = input("New name: ").strip()
                    cur.execute("UPDATE phonebook SET name = %s WHERE id = %s;", (new_val, contact_id))
                elif choice == "2":
                    new_val = input("New phone: ").strip()
                    cur.execute("UPDATE phonebook SET phone = %s WHERE id = %s;", (new_val, contact_id))
                else:
                    print("Invalid choice.")
                    return
        print("Updated.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def delete_by_name():
    name = input("Name to delete: ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebook WHERE name ILIKE %s;", (f"%{name}%",))
                print(f"Deleted {cur.rowcount} contact(s).")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def delete_by_phone():
    phone = input("Phone to delete: ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebook WHERE phone = %s;", (phone,))
                print(f"Deleted {cur.rowcount} contact(s).")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


MENU = """
--- PhoneBook ---
1. Show all
2. Add contact
3. Load from CSV
4. Search by name
5. Search by phone prefix
6. Update contact
7. Delete by name
8. Delete by phone
0. Exit
"""

ACTIONS = {
    "1": show_all,
    "2": insert_from_console,
    "3": lambda: insert_from_csv("contacts.csv"),
    "4": search_by_name,
    "5": search_by_phone_prefix,
    "6": update_contact,
    "7": delete_by_name,
    "8": delete_by_phone,
}


def main():
    create_table()
    while True:
        print(MENU)
        choice = input("Select: ").strip()
        if choice == "0":
            break
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()