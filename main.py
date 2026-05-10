from pyrogram import Client, idle
from config import *

app = Client(
    "ZlixBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

app.start()

me = app.get_me()

print(f"Bot Started : @{me.username}")

idle()

app.stop()
