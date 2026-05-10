from pyrogram import Client, filters
from pyrogram.types import Message

from database.users import get_user


@Client.on_message(
    filters.private &
    filters.command("credits")
)
async def credits_command(
    client,
    message: Message
):

    user = await get_user(
        message.from_user.id
    )

    credits = user.get(
        "credits",
        0
    )

    referrals = user.get(
        "referrals",
        0
    )

    await message.reply_text(
        f"""
💰 Credits: {credits}

👥 Referrals: {referrals}

Invite friends to earn more.
"""
    )
