from pymongo import MongoClient

from settings import mongo_settings

client = MongoClient(
    host=mongo_settings.host,
    port=mongo_settings.port,
    username=mongo_settings.username,
    password=mongo_settings.password,
    authSource=mongo_settings.auth_source,
    authMechanism=mongo_settings.auth_mechanism,
)

database = client[mongo_settings.database]

shows_collection = database.get_collection(mongo_settings.shows_collection)
shows_history_collection = database.get_collection(
    mongo_settings.shows_history_collection
)
