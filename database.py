from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

database = client["expense_tracker"]

expenses_collection = database["expenses"]