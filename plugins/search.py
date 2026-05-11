from utils.cooldown import check_cooldown
from utils.tmdb import search_tmdb

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
    ~filters.command([
        "start",
        "requests",
        "credits"
    ])
)
async def search_handler(client, message: Message):

    query = message.text.strip()

    # IGNORE COMMANDS
    if query.startswith("/"):
        return

    # IGNORE SHORT SEARCHES
    if len(query) < 2:
        return

    # COOLDOWN
    cooldown_time = 3

    if message.chat.type in [
        "group",
        "supergroup"
    ]:
        cooldown_time = 8

    remaining = check_cooldown(
        message.from_user.id,
        cooldown_time
    )

    if remaining > 0:

        return await message.reply_text(
            f"⏳ Wait {remaining}s before searching again."
        )

    # SEARCH DATABASE
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

        text = "🎬 Search Results"

        # GROUP MODE
        if message.chat.type in [
            "group",
            "supergroup"
        ]:

            text = (
                "🎬 Results Found\n"
                "Open privately using buttons below."
            )

        return await message.reply_text(
            text,
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

    # GROUP RESPONSE
    if message.chat.type in [
        "group",
        "supergroup"
    ]:

        return await message.reply_text(
            "❌ Not found.\nRequest added ✅"
        )

    # PRIVATE RESPONSE
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
        """
❌ No files found.

Your request has been added.

Example:
<code>Dangal 2016</code>,
<code>Sholay 1975</code>, and 
<code>Dilwale Dulhania Le Jayenge 1995</code>
""",
        reply_markup=buttons
    )
