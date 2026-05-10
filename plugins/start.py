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

    # START PAYLOAD
    data = message.command

    if len(data) > 1:

        payload = data[1]

        # FILE LINK
        if payload.startswith("file_"):

            deep_link = payload.replace(
                "file_", ""
            )

            file_data = await files_db.find_one(
                {"deep_link": deep_link}
            )

            if not file_data:

                return await message.reply_text(
                    "File not found."
                )

            await message.reply_cached_media(
                file_data["file_id"]
            )

            return

    await message.reply_text(
        f"Hello {name} 👋"
    )
