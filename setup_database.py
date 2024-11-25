import sqlite3
import os

def execute_script(conn, script_path):
    """
    Executes a SQL script from the given file path.
    """
    if not os.path.exists(script_path):
        print(f"Error: {script_path} does not exist.")
        return

    with open(script_path, 'r') as file:
        sql_script = file.read()
    try:
        conn.executescript(sql_script)
        print(f"Executed {script_path} successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while executing {script_path}: {e}")

def main():
    database = "business.db"

    # Remove existing database for a fresh setup
    if os.path.exists(database):
        os.remove(database)
        print(f"Existing database '{database}' removed for a fresh setup.")

    # Connect to SQLite database
    try:
        conn = sqlite3.connect(database)
        print(f"Connected to SQLite database: {database}\n")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    # Execute SQL scripts
    execute_script(conn, "create_tables.sql")
    execute_script(conn, "insert_sample_data.sql")

    # Close the connection
    conn.close()
    print("\nDatabase setup completed successfully.")

if __name__ == "__main__":
    main()
