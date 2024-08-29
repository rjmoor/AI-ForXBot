# scripts/setup/setup-database.py
from data.repositories.database import initialize_db

'''
This script is used to set up the database.
'''

def main():
    initialize_db()
    print("Database initialized.")

if __name__ == '__main__':
    main()
