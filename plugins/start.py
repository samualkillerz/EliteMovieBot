from database.settings import get_thumb
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.mongo import files_db

from database.users import (
    is_user_exist,
    add_user,
    get_user,
    add_referral,
    unlock_user,
    add_credits
)

from utils.checks import check_force_sub
from utils.filters import is_admin

from config import (
    FORCE_SUB_CHANNELS
)


BOT_USERNAME = "LordVT4ProBot"


@Client.on_message(
    filters.private &
    filters.command("start")
)
async def start_command(client, message: Message):

    user_id = message.from_user.id
    name = message.from_user.first_name

    admin = is_admin(user_id)

    payload = None

    if len(message.command) > 1:
        payload = message.command[1]

    # NEW USER
    if not await is_user_exist(user_id):

        await add_user(user_id, name)

        if admin:
            await unlock_user(user_id)

        # REFERRAL SYSTEM  
        if payload and payload.startswith("ref_"):

            try:

                referrer = int(
                    payload.replace("ref_", "")
                )

                if referrer != user_id:

                    await add_referral(referrer)

                    await add_credits(
                        referrer,
                        2
                    )

                    ref_data = await get_user(
                        referrer
                    )

                    if ref_data["referrals"] >= 1:

                        await unlock_user(
                            referrer
                        )

            except Exception as e:
                print(e)
        
    # #New Paylod 
    # if payload and payload.startswith("ref_"):

    # referrer = int(
    #     payload.replace("ref_", "")
    # )

    # already_referred = user_data.get(
    #     "referred_by"
    # )

    # if (
    #     referrer != user_id and
    #     not already_referred
    # ):

    #     await users_db.update_one(
    #         {"user_id": user_id},
    #         {
    #             "$set": {
    #                 "referred_by": referrer
    #             }
    #         }
    #     )

    #     await add_referral(referrer)
    #     await add_credits(referrer, 2)

    #     ref_data = await get_user(referrer)

    #     if ref_data["referrals"] >= 1:

    #         await unlock_user(referrer)
    # FORCE SUB CHECK
    joined = await check_force_sub(
        client,
        user_id
    )

    if not joined and not admin:

        buttons = []

        for channel in FORCE_SUB_CHANNELS:

            try:

                chat = await client.get_chat(
                    channel
                )

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

            except Exception as e:
                print(e)

        buttons.append(
            [
                InlineKeyboardButton(
                    "Try Again",
                    url=(
                        f"https://t.me/"
                        f"{BOT_USERNAME}"
                        f"?start={payload or ''}"
                    )
                )
            ]
        )

        return await message.reply_text(
            "⚠️ Join all channels first.",
            reply_markup=InlineKeyboardMarkup(
                buttons
            )
        )

    # USER DATA
    user_data = await get_user(user_id)

    # LOCK SYSTEM
    if (
        user_data and
        not user_data["unlocked"] and
        not admin
    ):

        referral_link = (
            f"https://t.me/{BOT_USERNAME}"
            f"?start=ref_{user_id}"
        )

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Invite Friend",
                        url=(
                            "https://t.me/share/url"
                            f"?url={referral_link}"
                        )
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Request Access",
                        callback_data=(
                            f"request#{user_id}"
                        )
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

    # FILE DELIVERY
    if payload and payload.startswith("file_"):

        deep_link = payload.replace(
            "file_",
            ""
        )

        file_data = await files_db.find_one(
            {"deep_link": deep_link}
        )

        if not file_data:

            return await message.reply_text(
                "❌ File not found."
            )

        try:
            thumb = await get_thumb()
            await client.send_cached_media(
                chat_id=message.chat.id,
                file_id=file_data["file_id"],
                # caption=file_data["file_name"]
                caption=f"""📂 {file_data['file_name']}
                
═══════════════════════
➜ 𝐔𝐩𝐝𝐚𝐭𝐞𝐬 @ZLIXOfficial
➜ 𝐌𝐨𝐯𝐢𝐞𝐬 @Moviewallahz_Official
➜ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 @ZLIXSupport
➜ 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 @ZlixPremium
═══════════════════════

♥️ 𝗧𝗲𝗮𝗺 ➜ @ZLIXOfficial
""",
            
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Updates",
                    url="https://t.me/ZLIXOfficial"
                ),

                InlineKeyboardButton(
                    "Movies",
                    url="https://t.me/Moviewallahz_Official"
                )
            ],

            [
                InlineKeyboardButton(
                    "Support",
                    url="https://t.me/ZLIXSupport"
                ),

                InlineKeyboardButton(
                    "Premium",
                    url="https://t.me/ZlixPremium"
                )
            ]
        ]
    )
)
        except Exception as e:

            print(e)

            return await message.reply_text(
                f"ERROR:\n{e}"
            )

        return

    # DEFAULT START
    await message.reply_text(
        "✅ Access Unlocked"
    )
