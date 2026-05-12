from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from database.mongo import users_db


@Client.on_callback_query(
    filters.regex("^unlock#")
)
async def unlock_callback(client, query: CallbackQuery):

    user_id = int(
        query.data.split("#")[1]
    )

    await users_db.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "unlocked": True
            }
        }
    )

    await query.answer(
        "User unlocked."
    )

    try:

        await client.send_message(
            user_id,
            "✅ Access granted by admin."
        )

    except:
        pass


@Client.on_callback_query(
    filters.regex("^remove#")
)
async def remove_callback(client, query: CallbackQuery):

    user_id = int(
        query.data.split("#")[1]
    )

    await users_db.delete_one(
        {"user_id": user_id}
    )

    await query.answer(
        "User removed."
    )

    try:

        await client.send_message(
            user_id,
            "❌ Your access was removed."
        )

    except:
        pass
