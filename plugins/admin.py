from pyrogram import Client, filters
from pyrogram.types import Message

from database.users import (
    is_user_exist,
    add_user
)

from database.mongo import files_db


@Client.on_message(filters.private & filters.command("start"))
async def start_command(client, message: Message):

    user_id = message.from_user.id
    name = message.from_user.first_name

    if not await is_user_exist(user_id):
        await add_user(user_id, name)

    # GET PAYLOAD
    payload = None

    if len(message.command) > 1:
        payload = message.command[1]

    # FILE DELIVERY
    if payload and payload.startswith("file_"):

        deep_link = payload.replace(
            "file_", ""
        )

        file_data = await files_db.find_one(
            {"deep_link": deep_link}
        )

        if not file_data:

            return await message.reply_text(
                "File not found in database."
            )

        try:

            await client.send_cached_media(
                chat_id=message.chat.id,
                file_id=file_data["file_id"],
                caption=file_data["file_name"]
            )

        except Exception as e:

            await message.reply_text(
                f"Delivery Error:\n{e}"
            )

        return

    await message.reply_text(
        f"Hello {name} 👋"
    )
