# data/repositories/mongo_connection.py
import os
from pymongo import MongoClient, errors
from logs.log_manager import LogManager

# Initialize the logger
logger = LogManager('mongo_connection_logs').get_logger()

class MongoDBHandler:
    def __init__(self, db_name, collection_name=None):
        """
        Initializes the MongoDBHandler with a connection to the specified database and optionally a collection.

        :param db_name: The name of the database to connect to.
        :param collection_name: The name of the collection to interact with (optional).
        """
        self.mongo_url = os.getenv('MONGO_URL', 'mongodb+srv://rjmoore:Anubis2030@dashxbot.q034as0.mongodb.net/')
        self.client = self._get_mongo_client()
        self.db = self.client[db_name]
        self.collection = self.db[collection_name] if collection_name else None

    def _get_mongo_client(self):
        """
        Establishes a connection to MongoDB using the MongoDB URL from environment variables.
        Returns a MongoClient instance.
        """
        try:
            client = MongoClient(self.mongo_url, serverSelectionTimeoutMS=5000)  # 5 seconds timeout
            # Check if the server is available
            client.admin.command('ping')
            logger.info(f"Connected to MongoDB at {self.mongo_url}")
            return client
        except errors.ServerSelectionTimeoutError as err:
            logger.error(f"Failed to connect to MongoDB: {err}")
            raise

    def create_collection(self, collection_name):
        """
        Creates a new collection within the database.

        :param collection_name: The name of the collection to create.
        :return: The created collection object.
        """
        try:
            collection = self.db.create_collection(collection_name)
            logger.info(f"Created collection: {collection_name}")
            return collection
        except errors.CollectionInvalid as err:
            logger.error(f"Failed to create collection '{collection_name}': {err}")
            raise

    def drop_collection(self, collection_name):
        """
        Drops a collection from the database.

        :param collection_name: The name of the collection to drop.
        """
        try:
            self.db.drop_collection(collection_name)
            logger.info(f"Dropped collection: {collection_name}")
        except errors.PyMongoError as err:
            logger.error(f"Failed to drop collection '{collection_name}': {err}")
            raise

    def create_database(self, db_name):
        """
        Creates a new database. In MongoDB, databases are created on demand by using them.

        :param db_name: The name of the database to create.
        :return: The created database object.
        """
        try:
            db = self.client[db_name]
            # To actually create the database, we need to insert a collection or create a collection
            db.create_collection("initial_collection")
            logger.info(f"Created database: {db_name}")
            return db
        except errors.PyMongoError as err:
            logger.error(f"Failed to create database '{db_name}': {err}")
            raise

    def drop_database(self, db_name):
        """
        Drops a database.

        :param db_name: The name of the database to drop.
        """
        try:
            self.client.drop_database(db_name)
            logger.info(f"Dropped database: {db_name}")
        except errors.PyMongoError as err:
            logger.error(f"Failed to drop database '{db_name}': {err}")
            raise

    def create(self, document):
        """
        Inserts a single document into the collection.

        :param document: A dictionary representing the document to insert.
        :return: The inserted ID of the document.
        """
        try:
            result = self.collection.insert_one(document)
            logger.info(f"Document inserted with ID: {result.inserted_id}")
            return result.inserted_id
        except errors.PyMongoError as err:
            logger.error(f"Failed to insert document: {err}")
            raise

    def read(self, query=None):
        """
        Reads documents from the collection.

        :param query: A dictionary representing the query to match documents.
        :return: A list of matched documents.
        """
        try:
            documents = self.collection.find(query or {})
            results = list(documents)
            logger.info(f"Found {len(results)} documents matching query: {query}")
            return results
        except errors.PyMongoError as err:
            logger.error(f"Failed to read documents: {err}")
            raise

    def update(self, query, update_values):
        """
        Updates documents in the collection based on a query.

        :param query: A dictionary representing the query to match documents.
        :param update_values: A dictionary representing the update values.
        :return: The count of documents updated.
        """
        try:
            result = self.collection.update_many(query, {'$set': update_values})
            logger.info(f"Updated {result.modified_count} documents matching query: {query}")
            return result.modified_count
        except errors.PyMongoError as err:
            logger.error(f"Failed to update documents: {err}")
            raise

    def delete(self, query):
        """
        Deletes documents from the collection based on a query.

        :param query: A dictionary representing the query to match documents.
        :return: The count of documents deleted.
        """
        try:
            result = self.collection.delete_many(query)
            logger.info(f"Deleted {result.deleted_count} documents matching query: {query}")
            return result.deleted_count
        except errors.PyMongoError as err:
            logger.error(f"Failed to delete documents: {err}")
            raise

    def close(self):
        """
        Closes the MongoDB connection.
        """
        try:
            self.client.close()
            logger.info("MongoDB connection closed.")
        except errors.PyMongoError as err:
            logger.error(f"Failed to close MongoDB connection: {err}")
            raise
