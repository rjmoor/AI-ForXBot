import os
import sqlite3

def connect_db(db_name=None):
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(db_name)

def connect_commit_close(database_path, schema_sql):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()

def initialize_db(db_type='sqlite', db_name=None):
    """
    Initializes the database based on the provided type and file name.

    :param db_type: Type of the database to create (e.g., 'sqlite').
    :param db_name: The name of the database file.
    """
    # Define the directory for databases
    databases_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'databases')

    # Ensure the directory exists
    if not os.path.exists(databases_dir):
        os.makedirs(databases_dir)

    # Define the path for the database file
    database_path = os.path.join(databases_dir, db_name)

    # Define the path for the schema file
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')
    # print(f"Schema path: {schema_path}")

    if not os.path.isfile(schema_path):
        print(f"Schema file not found: {schema_path}")
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with open(schema_path, 'r') as f:
        schema_sql = f.read()

    if db_type != 'sqlite':
        raise NotImplementedError(f"Database type '{db_type}' is not supported.")
    connect_commit_close(database_path, schema_sql)
    print(f"SQLite database '{db_name}' initialized successfully at '{database_path}'.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python setup-database.py <db_type> <db_name>")
        sys.exit(1)
    
    db_type = sys.argv[1]
    db_name = sys.argv[2]
    
    initialize_db(db_type, db_name)


def add_indicator(name, period):
    """Add a new indicator to the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO indicators (name, period) VALUES (?, ?)", (name, period))
    conn.commit()
    conn.close()

def get_indicator_parameters(indicator_id):
    """Get parameters for a given indicator."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM parameters WHERE indicator_id = ?", (indicator_id,))
    params = cursor.fetchall()
    conn.close()
    return dict(params)

def update_indicator_parameter(indicator_id, key, value):
    """Update parameters for a given indicator."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO parameters (indicator_id, key, value) VALUES (?, ?, ?)", (indicator_id, key, value))
    conn.commit()
    conn.close()
