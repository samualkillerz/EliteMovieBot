import secrets

from utils.cleaner import clean_file_name

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from utils.parser import normalize_query
from utils.filters import is_admin

from database.files import (
    get_file_by_unique,
    add_file,
    get_file_by_link,
    update_deep_link
)

from database.requests import (
    get_request,
    mark_uploaded
)

from database.mongo import files_db

from config import STORAGE_CHANNEL


BOT_USERNAME = "LordVT4ProBot"

rename_cache = {}


# ==========================================
# MEDIA INDEX HANDLER
# ==========================================

@Client.on_message(
    filters.private &
    (filters.document | filters.video)
)
async def admin_media_handler(client, message: Message):

    user_id = message.from_user.id

    if not is_admin(user_id):
        return

    media = message.document or message.video

    if not media:
        return

    unique_id = media.file_unique_id

    existing = await get_file_by_unique(unique_id)

    # FILE ALREADY EXISTS
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
                ],
                [
                    InlineKeyboardButton(
                        "Rename",
                        callback_data=f"rename|{existing_link}"
                    ),

                    InlineKeyboardButton(
                        "New Link",
                        callback_data=f"newlink|{existing_link}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Delete",
                        callback_data=f"delete|{existing_link}"
                    )
                ]
            ]
        )

        return await message.reply_text(
            "📦 File already exists.",
            reply_markup=buttons
        )

    # STORE FILE
    forwarded = await message.copy(
        STORAGE_CHANNEL
    )

    stored_media = (
        forwarded.document or
        forwarded.video
    )

    deep_link = secrets.token_urlsafe(8)

    cleaned_name = clean_file_name(
    media.file_name
    )
    
    normalized_name = normalize_query(
        cleaned_name
    )

    compact_name = normalized_name.replace(
        " ",
        ""
    )

    data = {
        "file_id": stored_media.file_id,
        "unique_id": unique_id,
        "file_name": clean_file_name(media.file_name),
        "deep_link": deep_link,
        "message_id": forwarded.id,

        "search_name": normalized_name,

        "search_compact": compact_name, #both work same this one and below one
        # "search_compact": normalize_query(media.file_name).replace(" ", "")  # use this or above one
    }

    await add_file(data)

    # AUTO REQUEST MATCH
    request_data = await get_request(
        normalized_name
    )

    if request_data:

        await mark_uploaded(
            normalized_name
        )

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

    # GENERATED LINK
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
                    callback_data=f"delete|{deep_link}"
                ),

                InlineKeyboardButton(
                    "Get Link",
                    callback_data=f"get|{deep_link}"
                )
            ]
        ]
    )

    await message.reply_text(
        "✅ File Indexed Successfully",
        reply_markup=buttons
    )


# ==========================================
# CALLBACKS
# ==========================================

@Client.on_callback_query()
async def callbacks(client, query: CallbackQuery):

    data = query.data

    # GET LINK
    if data.startswith("get|"):

        link = data.split("|", 1)[1]

        url = (
            f"https://t.me/{BOT_USERNAME}"
            f"?start=file_{link}"
        )

        return await query.message.reply_text(
            f"🔗 {url}"
        )

    # DELETE FILE
    if data.startswith("delete|"):

        link = data.split("|", 1)[1]

        file_data = await get_file_by_link(link)

        if not file_data:

            return await query.answer(
                "Already deleted.",
                show_alert=True
            )

        try:

            await client.delete_messages(
                STORAGE_CHANNEL,
                file_data["message_id"]
            )

        except:
            pass

        await files_db.delete_one(
            {"deep_link": link}
        )

        return await query.message.edit_text(
            "🗑 File deleted successfully."
        )

    # RENAME
    if data.startswith("rename|"):

        link = data.split("|", 1)[1]

        rename_cache[
            query.from_user.id
        ] = link

        return await query.message.reply_text(
            "✏️ Send new file name."
        )

    # NEW LINK
    if data.startswith("newlink|"):

        old_link = data.split("|", 1)[1]

        new_link = secrets.token_urlsafe(8)

        await update_deep_link(
            old_link,
            new_link
        )

        url = (
            f"https://t.me/{BOT_USERNAME}"
            f"?start=file_{new_link}"
        )

        return await query.message.reply_text(
            f"🔗 New Link:\n{url}"
        )


# ==========================================
# RENAME HANDLER
# ==========================================

@Client.on_message(
    filters.private &
    filters.text,
    group=10
)
async def rename_handler(
    client,
    message: Message
):

    user_id = message.from_user.id

    # ONLY HANDLE ACTIVE RENAME USERS
    if user_id not in rename_cache:
        return

    # ADMIN CHECK
    if not is_admin(user_id):
        return

    # IGNORE COMMANDS
    if message.text.startswith("/"):
        return

    new_name = message.text.strip()

    if not new_name:
        return

    link = rename_cache[user_id]

    normalized_name = normalize_query(
        new_name
    )

    compact_name = normalized_name.replace(
        " ",
        ""
    )

    # UPDATE DATABASE
    await files_db.update_one(
        {"deep_link": link},
        {
            "$set": {
                "file_name": new_name,
                "search_name": normalized_name,
                "search_compact": compact_name
            }
        }
    )

    # REMOVE FROM CACHE
    del rename_cache[user_id]

    await message.reply_text(
        "✅ File renamed successfully."
    )
