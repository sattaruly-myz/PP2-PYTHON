from connect import get_connection
import csv
import json
from pathlib import Path


VALID_PHONE_TYPES = {"home", "work", "mobile"}
SORT_MAP = {
    "1": "c.name",
    "2": "c.birthday",
    "3": "c.id",   # date added = insertion order, since there is no created_at column
}


def _get_group_id(cur, group_name):
    if not group_name:
        return None

    cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id;", (group_name,))
    return cur.fetchone()[0]


def _fetch_contacts(cur, where_sql="", params=(), order_sql="c.name"):
    query = f"""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            COALESCE(g.name, 'No group') AS group_name,
            COALESCE(
                STRING_AGG(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id),
                'No phones'
            ) AS phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON p.contact_id = c.id
        {where_sql}
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY {order_sql};
    """
    cur.execute(query, params)
    return cur.fetchall()


def _print_contacts(rows):
    if not rows:
        print("No results.")
        return

    print(f"\n  {'ID':<5} {'Name':<22} {'Email':<28} {'Birthday':<12} {'Group':<12} Phones")
    print("  " + "-" * 110)
    for row in rows:
        cid, name, email, birthday, group_name, phones = row
        birthday_text = birthday.isoformat() if birthday else "-"
        email_text = email or "-"
        print(f"  {cid:<5} {name:<22} {email_text:<28} {birthday_text:<12} {group_name:<12} {phones}")


def search_contacts_menu():
    query = input("Search (name/email/phone): ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s);", (query,))
            rows = cur.fetchall()

        if not rows:
            print("No results.")
            return

        print(f"\n  {'ID':<5} {'Name':<22} {'Email':<28} {'Birthday':<12} {'Group':<12} Phone / Type")
        print("  " + "-" * 110)
        for row in rows:
            cid, name, email, birthday, group_name, phone, phone_type = row
            birthday_text = birthday.isoformat() if birthday else "-"
            email_text = email or "-"
            phone_text = f"{phone} ({phone_type})" if phone else "-"
            print(f"  {cid:<5} {name:<22} {email_text:<28} {birthday_text:<12} {group_name or '-':<12} {phone_text}")
    finally:
        conn.close()


def filter_by_group():
    group_name = input("Group name: ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            rows = _fetch_contacts(
                cur,
                where_sql="WHERE g.name ILIKE %s",
                params=(f"%{group_name}%",),
                order_sql="c.name"
            )
        _print_contacts(rows)
    finally:
        conn.close()


def search_by_email():
    email_part = input("Email part: ").strip()
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            rows = _fetch_contacts(
                cur,
                where_sql="WHERE c.email ILIKE %s",
                params=(f"%{email_part}%",),
                order_sql="c.name"
            )
        _print_contacts(rows)
    finally:
        conn.close()


def show_sorted_contacts():
    print("Sort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")
    choice = input("Choose: ").strip()
    order_sql = SORT_MAP.get(choice, "c.name")

    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            rows = _fetch_contacts(cur, order_sql=order_sql)
        _print_contacts(rows)
    finally:
        conn.close()


def paginated_navigation():
    try:
        page_size = int(input("Contacts per page: ").strip())
        if page_size <= 0:
            raise ValueError
    except ValueError:
        print("Enter a valid positive number.")
        return

    page = 1
    conn = get_connection()
    if not conn:
        return

    try:
        while True:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (page, page_size))
                rows = cur.fetchall()

            print(f"\n--- Page {page} ---")
            if not rows:
                print("No results.")
            else:
                print(f"  {'ID':<5} {'Name':<22} {'Email'}")
                print("  " + "-" * 60)
                for row in rows:
                    cid, name, email = row
                    print(f"  {cid:<5} {name:<22} {email or '-'}")

            cmd = input("next / prev / quit: ").strip().lower()
            if cmd == "next":
                page += 1
            elif cmd == "prev":
                page = max(1, page - 1)
            elif cmd == "quit":
                break
            else:
                print("Invalid command.")
    finally:
        conn.close()


def export_json():
    filename = input("JSON file name: ").strip() or "contacts.json"
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    c.id,
                    c.name,
                    c.email,
                    c.birthday,
                    g.name AS group_name
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                ORDER BY c.id;
            """)
            contacts = cur.fetchall()

            result = []
            for contact_id, name, email, birthday, group_name in contacts:
                cur.execute("""
                    SELECT phone, type
                    FROM phones
                    WHERE contact_id = %s
                    ORDER BY id;
                """, (contact_id,))
                phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]

                result.append({
                    "name": name,
                    "email": email,
                    "birthday": birthday.isoformat() if birthday else None,
                    "group": group_name,
                    "phones": phones
                })

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Exported to {filename}")
    finally:
        conn.close()


def import_json():
    filename = input("JSON file name: ").strip() or "contacts.json"
    path = Path(filename)

    if not path.exists():
        print("File not found.")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = get_connection()
    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                for item in data:
                    name = item.get("name")
                    email = item.get("email")
                    birthday = item.get("birthday")
                    group_name = item.get("group")
                    phones = item.get("phones", [])

                    cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
                    existing = cur.fetchone()

                    if existing:
                        choice = input(f'"{name}" exists. Skip or overwrite? (s/o): ').strip().lower()
                        if choice == "s":
                            continue

                        contact_id = existing[0]
                        group_id = _get_group_id(cur, group_name)

                        cur.execute("""
                            UPDATE contacts
                            SET email = %s,
                                birthday = %s,
                                group_id = %s
                            WHERE id = %s;
                        """, (email, birthday, group_id, contact_id))

                        cur.execute("DELETE FROM phones WHERE contact_id = %s;", (contact_id,))
                    else:
                        group_id = _get_group_id(cur, group_name)
                        cur.execute("""
                            INSERT INTO contacts (name, email, birthday, group_id)
                            VALUES (%s, %s, %s, %s)
                            RETURNING id;
                        """, (name, email, birthday, group_id))
                        contact_id = cur.fetchone()[0]

                    for phone_item in phones:
                        phone = phone_item.get("phone")
                        ptype = phone_item.get("type", "mobile")

                        if ptype not in VALID_PHONE_TYPES:
                            ptype = "mobile"

                        if phone:
                            cur.execute("""
                                INSERT INTO phones (contact_id, phone, type)
                                VALUES (%s, %s, %s);
                            """, (contact_id, phone, ptype))

        print("Imported.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def import_csv():
    filename = input("CSV file name: ").strip() or "contacts.csv"
    path = Path(filename)

    if not path.exists():
        print("File not found.")
        return

    conn = get_connection()
    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)

                    for row in reader:
                        name = row.get("name", "").strip()
                        email = row.get("email", "").strip() or None
                        birthday = row.get("birthday", "").strip() or None
                        group_name = row.get("group", "").strip() or None
                        phone = row.get("phone", "").strip()
                        ptype = row.get("type", "").strip() or "mobile"

                        if not name or not phone:
                            continue

                        if ptype not in VALID_PHONE_TYPES:
                            ptype = "mobile"

                        cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
                        existing = cur.fetchone()

                        group_id = _get_group_id(cur, group_name)

                        if existing:
                            contact_id = existing[0]
                            cur.execute("""
                                UPDATE contacts
                                SET email = COALESCE(%s, email),
                                    birthday = COALESCE(%s, birthday),
                                    group_id = COALESCE(%s, group_id)
                                WHERE id = %s;
                            """, (email, birthday, group_id, contact_id))
                        else:
                            cur.execute("""
                                INSERT INTO contacts (name, email, birthday, group_id)
                                VALUES (%s, %s, %s, %s)
                                RETURNING id;
                            """, (name, email, birthday, group_id))
                            contact_id = cur.fetchone()[0]

                        cur.execute("""
                            INSERT INTO phones (contact_id, phone, type)
                            VALUES (%s, %s, %s);
                        """, (contact_id, phone, ptype))

        print("CSV imported.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def add_phone():
    name = input("Contact name: ").strip()
    phone = input("Phone: ").strip()
    ptype = input("Type (home/work/mobile): ").strip().lower()

    conn = get_connection()
    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, ptype))
        print("Phone added.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def move_to_group():
    name = input("Contact name: ").strip()
    group_name = input("New group: ").strip()

    conn = get_connection()
    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("CALL move_to_group(%s, %s);", (name, group_name))
        print("Contact moved.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


MENU = """
--- PhoneBook ---
1. Search contacts
2. Filter by group
3. Search by email
4. Show sorted contacts
5. Paginated browse
6. Export to JSON
7. Import from JSON
8. Import from CSV
9. Add phone
10. Move contact to group
0. Exit
"""

ACTIONS = {
    "1": search_contacts_menu,
    "2": filter_by_group,
    "3": search_by_email,
    "4": show_sorted_contacts,
    "5": paginated_navigation,
    "6": export_json,
    "7": import_json,
    "8": import_csv,
    "9": add_phone,
    "10": move_to_group,
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