import psycopg2
import csv
from config import load_config
def create_phonebook_table():
    commands = [
        """ 
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL UNIQUE,
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
def load_sql(filename):
    with open(filename, 'r',encoding='UTF-8') as file:  
        return file.read()

def load_func_proc(filename):
    config = load_config()
    sql = load_sql(filename)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
    except(psycopg2.DatabaseError, Exception) as error:
        print("Error: ",error)

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
    load_func_proc("lab11/update_user.sql")
    first_name = input("Enter name: ")
    phone_number = input("Enter phone number: ")
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL user_update(%s::TEXT,%s::TEXT)",(first_name,phone_number))
                print("Successfully Inserted|Updated")
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print("Insert error:", error) 
import psycopg2

import psycopg2

def insert_users_batch():
    config = load_config()
    load_func_proc("lab11/insert_list.sql")

    list_name = input("Enter names separated by comma: ").split(',')
    list_phone = input("Enter phone numbers separated by comma: ").split(',')

    list_name = [name.strip() for name in list_name]
    list_phone = [phone.strip() for phone in list_phone]

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Очистим старые логи, если нужно
                cur.execute("DELETE FROM invalid_log")

                # Вызов процедуры
                cur.execute("CALL insert_users_batch(%s, %s, NULL)", (list_name, list_phone))

                # Выводим, что сохранилось в логах
                cur.execute("SELECT entry FROM invalid_log ORDER BY created_at DESC")
                rows = cur.fetchall()

                if rows:
                    print("Invalid entries:")
                    for row in rows:
                        print(row[0])
                else:
                    print("All entries inserted successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Inserting Error:", error)


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
    print("4. View by a pattern")
    print("5. View with a pagination")
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
    elif choice == 4:
        load_func_proc('lab11/query_by_pattern.sql')
        pattern = input("Enter a pattern of name|phone number: ")
        pattern = '%' + pattern + '%'
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM query_by_pattern(%s)",(pattern,))
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        except (psycopg2.DatabaseError , Exception) as error:
            print("Query Error:",error)
    elif choice == 5:
        load_func_proc("lab11/pagination.sql")
        limit = input("Enter a limit: ")
        offset = input("Enter a offset: ")
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM pagination(%s,%s)",(limit,offset))
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        except (psycopg2.DatabaseError,Exception) as error:
            print("Query Error: ",error)
def delete_data():
    choice = input("Enter name|phone_number: ")
    config = load_config()
    load_func_proc("lab11/deleting.sql")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL deleting(%s)",(choice,))
                print("Succesfully Deleted")
    except (psycopg2.DatabaseError , Exception) as error:
        print("Delete Error:",error)
def main():
    create_phonebook_table()
    while True:
        print("\nMenu")
        print("1. Insert from CSV file")
        print("2. Insert from console")
        print("3. Insert many contacts")
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
            insert_users_batch()
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