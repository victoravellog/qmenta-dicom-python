from pymongo import MongoClient
from config.config import Settings

settings = Settings()

db_client = MongoClient(settings.MONGO_CONNECTION).local
