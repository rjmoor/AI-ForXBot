import os
import sys
from data.repositories.database import initialize_db
from logs.log_manager import LogManager  # Import the LogManager class

# Initialize logger for database setup
logger = LogManager('database_setup').get_logger()

# Configure logging
# import logging
logger.basicConfig(level=logger.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(db_name='indicators.db', db_type='sqlite'):
    """
    Main function to initialize the specified database.

    :param db_name: The name of the database file to be created.
    :param db_type: The type of database to initialize (currently supports 'sqlite').
    """
    try:
        logger.info("Starting database initialization...")
        initialize_db(db_type=db_type, db_name=db_name)
        logger.info(f"Database '{db_name}' initialized successfully.")
    except Exception as e:
        logger.error(f"An error occurred while initializing the database: {e}")
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    
    # Default database types and names
    databases = {
        'indicators': 'indicators.db',
        'optimizer': 'optimizer.db',
        'user': 'user.db',
        'configuration': 'configuration.db'
    }

    db_type = sys.argv[1] if len(sys.argv) > 1 else 'sqlite'
    db_name = sys.argv[2] if len(sys.argv) > 2 else None

    # Validate the database type
    if db_type not in ['sqlite']:
        logger.error(f"Unsupported database type: {db_type}")
        print(f"Unsupported database type: {db_type}")
        sys.exit(1)

    # Initialize specified database or all databases
    if db_name is None:
        for db_file in databases.values():
            logger.info(f"Initializing '{db_key}' database...")
            print(f"Initializing database '{db_file}'...")
            main(db_name=db_file, db_type=db_type)
    elif db_name in databases.values():
        main(db_name=db_name, db_type=db_type)
    else:
        logger.error(f"Database name '{db_name}' is not recognized.")
        print(f"Database name '{db_name}' is not recognized.")
        sys.exit(1)
