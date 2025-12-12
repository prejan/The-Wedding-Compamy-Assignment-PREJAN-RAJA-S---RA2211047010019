from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)

master_db = client["master_db"]  # Stores organization + admin metadata
