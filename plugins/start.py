from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.mongo import files_db

from utils.checks import check_force_sub

from config import FORCE_SUB_CHANNELS


@Client.on_message(filters.private & filters.command("start"))
async def start_command(client, message: Message):

    payload = None

    if len(message.command) > 1:
        payload = message.command[1]

    # FORCE SUB CHECK
    joined = await check_force_sub(
        client,
        message.from_user.id
    )

    if not joined:

        buttons = []

        for channel in FORCE_SUB_CHANNELS:

            chat = await client.get_chat(channel)

            buttons.append(
                [
                    InlineKeyboardButton(
                        chat.title,
                        url=chat.invite_link
                    )
                ]
            )

        buttons.append(
            [
                InlineKeyboardButton(
                    "Try Again",
                    url=f"https://t.me/LordVT4ProBot?start={payload}"
                )
            ]
        )

        return await message.reply_text(
            "Join all channels first.",
            reply_markup=InlineKeyboardMarkup(
                buttons
            )
        )

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
                "File not found."
            )

        try:

            await client.send_cached_media(
                chat_id=message.chat.id,
                file_id=file_data["file_id"],
                caption=file_data["file_name"]
            )

        except Exception as e:

            return await message.reply_text(
                f"ERROR:\n{e}"
            )

        return

    await message.reply_text(
        "Welcome to LordVT4ProBot"
    )
