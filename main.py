from pyrogram import Client
from config import *

print("MAIN FILE RUNNING")
app = Client(
    "LordVT4",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

print("✅ Bot Started Successfully")

app.run()
