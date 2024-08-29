import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

# Ensure all required environment variables are set
required_vars = ["MONGODB_URI", "DATABASE_NAME", "SECRET_KEY"]
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Environment variable {var} is not set")

# Create a MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)
database = client[DATABASE_NAME]

@asynccontextmanager
async def get_database():
    try:
        yield database
    finally:
        client.close()

async def check_database_connection():
    try:
        await database.command('ping')
        print("Successfully connected to the database")
    except Exception as e:
        print(f"Unable to connect to the database. Error: {e}")
        raise