from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from database.mongo import files_db

from database.users import (
    is_user_exist,
    add_user,
    get_user,
    add_referral,
    unlock_user
)

from utils.checks import check_force_sub
from utils.filters import is_admin

from config import (
    FORCE_SUB_CHANNELS,
    ADMINS
)


BOT_USERNAME = "LordVT4ProBot"


@Client.on_message(filters.private & filters.command("start"))
async def start_command(client, message: Message):

    user_id = message.from_user.id
    name = message.from_user.first_name

    admin = is_admin(user_id)

    payload = None

    if len(message.command) > 1:
        payload = message.command[1]

    if not await is_user_exist(user_id):

        await add_user(user_id, name)

        if admin:
            await unlock_user(user_id)

        if payload and payload.startswith("ref_"):

            referrer = int(
                payload.replace("ref_", "")
            )

            if referrer != user_id:

                await add_referral(referrer)

                ref_data = await get_user(
                    referrer
                )

                if ref_data["referrals"] >= 1:

                    await unlock_user(referrer)

    joined = await check_force_sub(
        client,
        user_id
    )

    if not joined and not admin:

        buttons = []

        for channel in FORCE_SUB_CHANNELS:

            chat = await client.get_chat(channel)

            if chat.username:

                url = (
                    f"https://t.me/"
                    f"{chat.username}"
                )

            else:

                url = "https://t.me"

            buttons.append(
                [
                    InlineKeyboardButton(
                        chat.title,
                        url=url
                    )
                ]
            )

        buttons.append(
            [
                InlineKeyboardButton(
                    "Try Again",
                    url=f"https://t.me/{BOT_USERNAME}?start={payload}"
                )
            ]
        )

        return await message.reply_text(
            "⚠️ Join all channels first.",
            reply_markup=InlineKeyboardMarkup(
                buttons
            )
        )

    user_data = await get_user(user_id)

    if not user_data["unlocked"] and not admin:

        referral_link = (
            f"https://t.me/{BOT_USERNAME}"
            f"?start=ref_{user_id}"
        )

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Invite Friend",
                        url=f"https://t.me/share/url?url={referral_link}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Request Access",
                        callback_data=f"request#{user_id}"
                    )
                ]
            ]
        )

        return await message.reply_text(
            f"""
🔒 Bot Locked

Invite 1 user to unlock access.

Your Referrals:
{user_data['referrals']}/1
""",
            reply_markup=buttons
        )

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
        "✅ Access Unlocked"
    )
