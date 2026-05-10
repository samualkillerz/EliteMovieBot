import secrets

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from utils.parser import normalize_query

from database.files import (
    get_file_by_unique,
    add_file,
    get_file_by_link,
    update_file_name,
    update_deep_link
)

from utils.filters import is_admin

from database.files import (
    get_file_by_unique,
    add_file
)

from database.requests import (
    get_request,
    mark_uploaded
)

from database.mongo import files_db

from config import STORAGE_CHANNEL


BOT_USERNAME = "LordVT4ProBot"


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

        existing_link = existing["deep_link"]

        url = (
            f"https://t.me/{BOT_USERNAME}"
            f"?start=file_{existing_link}"
        )

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Open Existing",
                        url=url
                    )
                ]
            ]
        )

        return await message.reply_text(
            "File already exists.",
            reply_markup=buttons
        )

    forwarded = await message.copy(
        STORAGE_CHANNEL
    )

    stored_media = (
        forwarded.document or
        forwarded.video
    )

    deep_link = secrets.token_urlsafe(8)

    data = {
        "file_id": stored_media.file_id,
        "unique_id": unique_id,
        "file_name": media.file_name,
        "deep_link": deep_link,
        "message_id": forwarded.id,
        "search_name": normalize_query(media.file_name)
    }

    await add_file(data)

    title = media.file_name.lower()

    request_data = await get_request(title)

    if request_data:

        await mark_uploaded(title)

        for user in request_data["requesters"]:

            try:

                await client.send_message(
                    user,
                    f"""
🎬 Requested Content Added

📦 {media.file_name}

Now Available ✅
"""
                )

            except:
                pass

    url = (
        f"https://t.me/{BOT_USERNAME}"
        f"?start=file_{deep_link}"
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
