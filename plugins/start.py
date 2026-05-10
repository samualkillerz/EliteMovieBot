from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.private & filters.command("start"))
async def start_command(client, message: Message):

    await message.reply_text(
        f"""
TEXT:
{message.text}

COMMAND:
{message.command}
"""
    )
