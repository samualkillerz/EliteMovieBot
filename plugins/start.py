from pyrogram import filters
from pyrogram.types import Message

from main import app

from database.users import (
    is_user_exist,
    add_user
)


@app.on_message(filters.private & filters.command("start"))
async def start_command(client, message: Message):

    user_id = message.from_user.id
    name = message.from_user.first_name

    if not await is_user_exist(user_id):
        await add_user(user_id, name)

    await message.reply_text(
        f"""
Hello {name} 👋

Welcome to LordVT4ProBot
"""
    )
