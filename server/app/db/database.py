from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI, server_api=ServerApi('1'))
db = client["tax-check-db"]
users_collection = db["users"]
strategyHistory_collection = db["strategyHistory"]