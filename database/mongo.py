from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

mongo = AsyncIOMotorClient(MONGO_URI)

db = mongo["VeilBot"]

users_db = db["users"]
files_db = db["files"]
referrals_db = db["referrals"]
requests_db = db["requests"]
settings_db = db["settings"]
