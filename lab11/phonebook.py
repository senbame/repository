import psycopg2
import csv
from config import load_config
def create_phonebook_table():
    commands = [
        """ 
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) UNIQUE NOT NULL,
            phone_number VARCHAR(255) UNIQUE NOT NULL
        )
        """]
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


import csv
import psycopg2

def insert_from_csv():
    config = load_config()
    file_path = input("Enter CSV file path: ")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(file_path, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        try:
                            cur.execute("""
                                INSERT INTO contacts (first_name, phone_number) 
                                VALUES (%s, %s)
                                ON CONFLICT (first_name) 
                                DO UPDATE SET phone_number = EXCLUDED.phone_number
                            """, (row[0], row[1]))
                        except Exception as e:
                            print(f"Error inserting {row}: {e}")
                    conn.commit()  
                    print("CSV data inserted successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Database error:", error)


def insert_from_console():
    config = load_config()
    first_name = input("Enter name: ")
    phone_number = input("Enter phone number: ")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO contacts (first_name , phone_number) VALUES(%s , %s) ON CONFLICT (first_name) DO UPDATE SET phone_number = EXCLUDED.phone_number
            """,(first_name , phone_number))
                conn.commit()
                print("Successfully Inserted or Updated")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Insert error:", error)
def insert_many_contacts():
    config = load_config()
    contacts_input = input("Enter contacts in format name:phone, comma-separated: ")

    try:
        # Преобразуем строку в словарь
        contacts = dict(map(lambda x: (x.split(':')[0].strip(), x.split(':')[1].strip()), contacts_input.split(',')))
        incorrect = []

        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for name, phone in contacts.items():
                    if phone.isdigit() and len(phone) >= 5:
                        try:
                            cur.execute("""
                                INSERT INTO contacts (first_name, phone_number)
                                VALUES (%s, %s)
                                ON CONFLICT (first_name) DO UPDATE SET phone_number = EXCLUDED.phone_number
                            """, (name, phone))
                        except Exception as e:
                            print(f"Insert error for {name}: {e}")
                            incorrect.append((name, phone))
                    else:
                        incorrect.append((name, phone))
                conn.commit()

        if incorrect:
            print("Incorrect entries:")
            for name, phone in incorrect:
                print(f"{name}: {phone}")
        else:
            print("All contacts inserted successfully.")

    except Exception as e:
        print("Error parsing input or inserting:", e)


def update_data():
    config = load_config()
    print("\nChose update option")
    print("1. Change name")
    print("2. Change number")
    choice = int(input("Choose your option: "))
    if choice == 1:
        new_name = input("Enter new name: ")
        phone_number = input("Enter the phone number: ")
        try:
             with psycopg2.connect(**config) as conn:
                 with conn.cursor() as cur:
                     cur.execute("""
                        UPDATE contacts SET first_name = %s WHERE phone_number = %s
                """, (new_name , phone_number))
                     conn.commit()
                     print("Name Succesfully Changed")
        except (psycopg2.DatabaseError , Exception) as error:
            print("Update Error:",error)
    elif choice == 2:
        new_number = input("Enter new phone number: ")
        first_name = input("Enter the name of a person: ")
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE contacts SET phone_number = %s WHERE first_name = %s
                """, (new_number , first_name))
                    conn.commit()
                    print("Phone Number Successfully Changed")
        except (psycopg2.DatabaseError,Exception) as error:
            print("Update Error:",error)
def query_data():
    config = load_config()
    print("\nChoose Query Option")
    print("1. View All")
    print("2. View by name")
    print("3. View by phone number")
    print("4. View by pattern of name")
    print("5. View by a pattern of phone number")
    choice = int(input("Choose your option: "))
    if choice == 1:
        try:
            limit = 5
            offset = 0
            while True:
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(""" 
                                SELECT * FROM contacts ORDER BY id LIMIT %s OFFSET %s
                                """,(limit,offset))
                        rows = cur.fetchall()
                        if not rows:
                            print("No more contacts.")
                        print(f"\n---Showing {limit} contacts starting from {offset+1}---")
                        for row in rows:
                            print(row)
                        command = input("Type 'n' for next 'p' for previous and 'q' to quit: ").strip().lower()
                        if command == 'n':
                            offset += limit
                        elif command == 'p':
                            offset = max(0,offset-limit)
                        elif command == 'q':
                            break
                        else:
                            print("Invalid command")
        except (psycopg2.DatabaseError , Exception) as error:
            print("Query Error", error )
    elif choice == 2:
        first_name = input("Enter name: ")
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT * FROM contacts WHERE first_name = %s
                    """, (first_name,))
                    conn.commit()
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        except (psycopg2.DatabaseError, Exception) as error:
            print("Query Error:",error)
    elif choice == 3:
        phone_number = input("Enter Phone Number: ")
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT * FROM contacts WHERE phone_number = %s
                    """,(phone_number,))
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
                    conn.commit()
        except (psycopg2.DatabaseError, Exception) as error:
            print("Query Error:",error)
    elif choice == 4:
        pattern_name = input("Enter pattern of name: ")
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    pattern = '%' + pattern_name + '%'
                    cur.execute("SELECT * FROM contacts WHERE first_name LIKE %s" , (pattern,))
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        except (psycopg2.DatabaseError , Exception) as error:
            print("Query Error: ",error)
    elif choice == 5:
        pattern_number = input("Enter pattern of phone number: ")
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    pattern2 = '%' + pattern_number + '%'
                    cur.execute("SELECT * FROM contacts WHERE phone_number LIKE %s" , (pattern2,))
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        except (psycopg2.DatabaseError , Exception) as error:
            print("Query Error: ",error)
def delete_data():
    print("\nDelete by:")
    print("1. Name")
    print("2. Phone Number")
    choice = int(input("Enter your option: "))
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if choice == 1:
                    first_name = input("Enter name: ")
                    cur.execute("""
                        DELETE FROM contacts WHERE first_name = %s
                         """, (first_name,))
                elif choice == 2:
                    phone_number = input("Enter phone number: ")
                    cur.execute(""" 
                        DELETE FROM contacts WHERE phone_number = %s  
                        """, (phone_number,))
                conn.commit()
                print("Successfully Deleted")
    except (psycopg2.DatabaseError , Exception) as error:
        print("Delete Error:",error)
def main():
    create_phonebook_table()
    while True:
        print("\nMenu")
        print("1. Insert from CSV file")
        print("2. Insert from console")
        print("3. Insert many contacts from console")
        print("4. Update data")
        print("5. Query Data")
        print('6. Delete Data')
        print('7. Exit')
        choice = int(input("Choose your option: "))
        if choice == 1:
            insert_from_csv()
        elif choice == 2:
            insert_from_console()
        elif choice == 3:
            insert_many_contacts()
        elif choice == 4:
            update_data()
        elif choice == 5:
            query_data()
        elif choice == 6:
            delete_data()
        elif choice == 7:
            break
        else:
            print("Invalid option")
if __name__ == '__main__':
    main()