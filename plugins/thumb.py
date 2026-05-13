from pyrogram import Client, filters
from pyrogram.types import Message

from utils.filters import is_admin

from database.settings import (
    save_thumb
)


@Client.on_message(
    filters.command("setthumb") &
    filters.private
)
async def set_thumb(client, message: Message):

    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    if not message.reply_to_message:

        return await message.reply_text(
            "Reply to photo."
        )

    photo = message.reply_to_message.photo

    if not photo:

        return await message.reply_text(
            "Reply to a photo."
        )

    await save_thumb(
        photo.file_id
    )

    await message.reply_text(
        "✅ Thumbnail saved."
    )
