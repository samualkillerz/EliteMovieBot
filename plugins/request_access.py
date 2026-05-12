from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from config import ADMINS


@Client.on_callback_query(
    filters.regex("^request#")
)
async def request_access_callback(client, query: CallbackQuery):

    user = query.from_user

    text = f"""
🔔 New Access Request

👤 User: {user.first_name}
🆔 ID: {user.id}
📎 Username: @{user.username if user.username else 'None'}
"""

    buttons = [
        [
            {
                "text": "✅ Unlock",
                "callback_data": f"unlock#{user.id}"
            }
        ],
        [
            {
                "text": "🗑 Remove User",
                "callback_data": f"remove#{user.id}"
            }
        ]
    ]

    from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Unlock",
                    callback_data=f"unlock#{user.id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🗑 Remove User",
                    callback_data=f"remove#{user.id}"
                )
            ]
        ]
    )

    for admin in ADMINS:

        await client.send_message(
            admin,
            text,
            reply_markup=keyboard
        )

    await query.answer(
        "Request sent to admin."
    )
