from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://mm:jYRQgedy6zMjjUma@cluster0.ewxlp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class MongoDBClient:
    def __init__(self):
        # Initialize the MongoDB client
        self.client = MongoClient(uri)
        self.db = self.client["hh"]
        self.users_collection = self.db["users"]

    def getUser(self):
        return self.users_collection.find_one()

    def getAllPhotos(self):
        user = self.getUser()
        return user["people"] if user else None

    def getPlaces(self):
        user = self.getUser()
        return user["places"] if user else None

    def addUser(self, user_data):
      result = self.users_collection.insert_one(user_data)
      return result.inserted_id

    def addPhotoForUser(self, user_id, person):
        result = self.users_collection.update_one(
            {"_id": user_id},
            {"$push": {"people": person}}
        )
        return result.modified_count

    def addPhotoForPlaces(self, user_id, place):
        result = self.users_collection.update_one(
            {"_id": user_id},
            {"$push": {"people": place}}
        )
        return result.modified_count
