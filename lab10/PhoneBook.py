import psycopg2
import csv
from config import load_config
def create_phonebook_table():
    commands = [
        """ 
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
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
                            cur.execute(
                                "INSERT INTO contacts (first_name, phone_number) VALUES (%s, %s)",
                                (row[0], row[1])
                            )
                        except psycopg2.errors.UniqueViolation:
                            conn.rollback() 
                            print(f"Duplicate phone or name: {row}")
                        except Exception as e:
                            conn.rollback()
                            print(f"Error inserting {row}: {e}")
                    conn.commit()  
                    print("CSV data inserted successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Database error:", error)

def insert_from_console():
    config = load_config()
    first_name = input("Enter name: ")
    phone_number = input("Enter phone number: ")
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO contacts (first_name , phone_number) VALUES(%s , %s)
            """,(first_name , phone_number))
                conn.commit()
                print("Successfully Inserted")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Insert error:", error) 
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
    choice = int(input("Choose your option: "))
    if choice == 1:
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(""" 
                        SELECT * FROM contacts
                """)
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
                    conn.commit()
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
        print("3. Update data")
        print("4. Query Data")
        print('5. Delete Data')
        print('6. Exit')
        choice = int(input("Choose your option: "))
        if choice == 1:
            insert_from_csv()
        elif choice == 2:
            insert_from_console()
        elif choice == 3:
            update_data()
        elif choice == 4:
            query_data()
        elif choice == 5:
            delete_data()
        elif choice == 6:
            break
        else:
            print("Invalid option")
if __name__ == '__main__':
    main()