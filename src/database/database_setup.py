from pymongo import MongoClient, ASCENDING
from pymongo.database import Database


class DatabaseConnector:
    _instance = None

    def __new__(cls, url: str, database_name: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(url)
            cls._instance.database = cls._instance.client[database_name]
        return cls._instance

    def get_database(self) -> Database:
        return self.database


db_connector = DatabaseConnector('mongodb://localhost:27017/', 'mydatabase')
users = db_connector.get_database()['users']
users.create_index([('name', ASCENDING)])

organizations = db_connector.get_database()['organizations']
organizations.create_index([('name', ASCENDING)])

