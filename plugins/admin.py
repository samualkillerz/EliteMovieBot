import secrets

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from utils.filters import is_admin

from database.files import (
    get_file_by_unique,
    add_file
)

from config import STORAGE_CHANNEL


@Client.on_message(
    filters.private &
    (filters.document | filters.video)
)
async def admin_media_handler(client, message: Message):

    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    media = message.document or message.video

    unique_id = media.file_unique_id

    existing = await get_file_by_unique(unique_id)

    if existing:

        await message.reply_text(
            "File already exists."
        )

        return

    forwarded = await message.copy(
        STORAGE_CHANNEL
    )

    deep_link = secrets.token_urlsafe(8)

    data = {
        "file_id": media.file_id,
        "unique_id": unique_id,
        "file_name": media.file_name,
        "deep_link": deep_link,
        "message_id": forwarded.id
    }

    await add_file(data)

    url = (
        f"https://t.me/"
        f"LordVT4ProBot?start=file_{deep_link}"
    )


    buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Open Link",
                url=url
            )
        ],
        [
            InlineKeyboardButton(
                "Delete",
                callback_data=f"delete#{deep_link}"
            ),

            InlineKeyboardButton(
                "Get Link",
                callback_data=f"get#{deep_link}"
                )
            ]
        ]
    )
    await message.reply_text(
        "File Indexed Successfully ✅",
        reply_markup=buttons
    )
