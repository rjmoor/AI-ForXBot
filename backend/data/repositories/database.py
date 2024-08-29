import sqlite3

def connect_db(db_name='indicators.db'):
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(db_name)

def initialize_db():
    """Initialize the database schema."""
    with open('schema.sql', 'r') as f:
        schema = f.read()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()

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
