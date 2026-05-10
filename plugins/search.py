from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.files import search_files

from database.requests import (
    get_request,
    create_request,
    add_request_user
)


BOT_USERNAME = "LordVT4ProBot"


@Client.on_message(
    filters.text &
    ~filters.command("start")
)
async def search_handler(client, message: Message):

    query = message.text.strip()

    # IGNORE SHORT SEARCHES
    if len(query) < 3:
        return

    results = await search_files(query)

    # RESULTS FOUND
    if results:

        buttons = []

        for file in results:

            url = (
                f"https://t.me/{BOT_USERNAME}"
                f"?start=file_{file['deep_link']}"
            )

            buttons.append(
                [
                    InlineKeyboardButton(
                        file["file_name"][:50],
                        url=url
                    )
                ]
            )

        return await message.reply_text(
            "🎬 Search Results",
            reply_markup=InlineKeyboardMarkup(
                buttons
            )
        )

    # NOT FOUND
    request_data = await get_request(query)

    if not request_data:

        await create_request(
            query,
            message.from_user.id
        )

    else:

        await add_request_user(
            query,
            message.from_user.id
        )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Request Added ✅",
                    callback_data="requested"
                )
            ]
        ]
    )

    return await message.reply_text(
        f"""
❌ No files found.

Your request has been added.

Example format:
Iron Man 2008
""",
        reply_markup=buttons
    )
