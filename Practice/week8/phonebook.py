from connect import get_connection


def search_by_pattern():
    pattern = input("Enter name or phone (or part): ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
            rows = cur.fetchall()
        if not rows:
            print("No results.")
        else:
            print(f"\n  {'ID':<5} {'Name':<25} {'Phone'}")
            print("  " + "-" * 45)
            for row in rows:
                print(f"  {row[0]:<5} {row[1]:<25} {row[2]}")
    finally:
        conn.close()


def upsert_contact():
    name  = input("Name: ").strip()
    phone = input("Phone: ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def bulk_insert():
    print("Enter contacts one by one. Type 'done' when finished.")
    names, phones = [], []
    while True:
        name = input("Name (or 'done'): ").strip()
        if name.lower() == "done":
            break
        phone = input("Phone: ").strip()
        names.append(name)
        phones.append(phone)

    if not names:
        print("Nothing to insert.")
        return

    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL insert_many_contacts(%s, %s);",
                    (names, phones)
                )
        print("Done. Invalid phones were printed as notices above.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def paginated_query():
    try:
        page      = int(input("Page number: ").strip())
        page_size = int(input("Contacts per page: ").strip())
    except ValueError:
        print("Enter a valid number.")
        return

    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (page, page_size))
            rows = cur.fetchall()
        if not rows:
            print("No results.")
        else:
            print(f"\n  {'ID':<5} {'Name':<25} {'Phone'}")
            print("  " + "-" * 45)
            for row in rows:
                print(f"  {row[0]:<5} {row[1]:<25} {row[2]}")
    finally:
        conn.close()


def delete_contact():
    value = input("Enter name or phone to delete: ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s);", (value,))
        print("Deleted.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


MENU = """
--- PhoneBook (Practice 8) ---
1. Search by pattern
2. Add / update contact (upsert)
3. Bulk insert
4. Show contacts (paginated)
5. Delete contact
0. Exit
"""

ACTIONS = {
    "1": search_by_pattern,
    "2": upsert_contact,
    "3": bulk_insert,
    "4": paginated_query,
    "5": delete_contact,
}


def main():
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