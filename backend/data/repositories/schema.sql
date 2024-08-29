-- schema.sql

-- Create the indicators table
CREATE TABLE indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    period INTEGER NOT NULL
);

-- Create the parameters table
CREATE TABLE parameters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_id INTEGER,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    FOREIGN KEY (indicator_id) REFERENCES indicators (id)
);
