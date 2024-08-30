# data/repositories/mongo_connection.py

from pymongo import MongoClient
import os

def get_mongo_client():
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    return MongoClient(mongo_url)

def get_database(db_name):
    client = get_mongo_client()
    return client[db_name]

def close_connection(client):
    client.close()
