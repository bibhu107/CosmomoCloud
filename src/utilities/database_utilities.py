from pymongo.database import Database
from bson import ObjectId


def get_data_from_id(collection_name: Database, id: str):
    return collection_name.find_one({"_id": ObjectId(get_striped_id(id))})


def get_object_id(id: str):
    return ObjectId(get_striped_id(id))


def get_striped_id(id: str):
    return id.strip()
