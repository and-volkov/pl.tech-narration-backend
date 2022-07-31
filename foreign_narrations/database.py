from pymongo import MongoClient
from pymongo.collection import Collection
from pydantic_mongo import AbstractRepository

import models
from settings import mongo_settings


class ShowsRepository(AbstractRepository[models.Show]):
    class Meta:
        collection_name = mongo_settings.collection


client = MongoClient(
    host=mongo_settings.host,
    port=mongo_settings.port,
    username=mongo_settings.username,
    password=mongo_settings.password,
    authSource=mongo_settings.auth_source,
    authMechanism=mongo_settings.auth_mechanism,
)

database = client[mongo_settings.database]

shows_repository = ShowsRepository(database=database)

print(shows_repository.find_one_by({'name': 'WAS'}).narrations.get('fr').file_path)
