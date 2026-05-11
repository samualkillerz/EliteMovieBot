from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

MONGO_URI = getenv("MONGO_URI")

ADMINS = list(map(int, getenv("ADMINS").split()))

STORAGE_CHANNEL = int(getenv("STORAGE_CHANNEL"))
LOG_CHANNEL = int(getenv("LOG_CHANNEL"))

FORCE_SUB_CHANNELS = list(
    map(int, getenv("FORCE_SUB_CHANNELS").split())
)

BOT_USERNAME = getenv("BOT_USERNAME")

TMDB_API="1384bfa0b3d377f1c34362d45c38235f"
