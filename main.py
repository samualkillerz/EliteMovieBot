from pyrogram import Client, idle
from config import *

app = Client(
    "LordVT4",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

app.run()
