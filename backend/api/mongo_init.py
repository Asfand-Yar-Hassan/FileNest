from pymongo import MongoClient
from django.conf import settings
from pymongo.errors import ConnectionFailure

client = MongoClient(settings.MONGO_URI)
try:
    client.admin.command('ping')
except ConnectionFailure:
    print("Server not available")
