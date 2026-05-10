from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from utils.filters import is_admin

from database.requests import (
    get_all_requests,
    mark_uploaded,
    delete_request
)


@Client.on_message(
    filters.private &
    filters.command("requests")
)
async def requests_panel(client, message: Message):

    if not is_admin(message.from_user.id):
        return

    requests = await get_all_requests()

    if not requests:

        return await message.reply_text(
            "No pending requests."
        )

    text = "📌 Pending Requests\n\n"

    for req in requests:

        title = req.get("title", "Unknown")

        count = req.get("count", 0)

        text += (
            f"🎬 {title.title()}\n"
            f"📊 Requests: {count}\n\n"
        )

    await message.reply_text(text)


@Client.on_callback_query()
async def request_callbacks(
    client,
    query: CallbackQuery
):

    data = query.data

    if data.startswith("done#"):

        if not is_admin(query.from_user.id):
            return

        title = data.split(
            "#",
            1
        )[1]

        await mark_uploaded(title)

        return await query.message.edit_text(
            f"✅ Uploaded:\n{title}"
        )

    if data.startswith("delreq#"):

        if not is_admin(query.from_user.id):
            return

        title = data.split(
            "#",
            1
        )[1]

        await delete_request(title)

        return await query.message.edit_text(
            f"🗑 Deleted:\n{title}"
        )
