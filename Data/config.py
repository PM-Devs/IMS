from pymongo import MongoClient
from Data.models import Student

# Connect to MongoDB
client = MongoClient("your_mongodb_connection_string")
db = client["your_database_name"]

