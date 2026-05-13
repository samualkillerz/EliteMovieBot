from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from database.settings import (
    get_settings,
    update_setting
)

from utils.filters import is_admin


@Client.on_message(
    filters.command("settings")
)
async def settings_panel(
    client,
    message: Message
):

    if not is_admin(
        message.from_user.id
    ):
        return

    settings = await get_settings()

    auto_delete = (
        "✅ ON"
        if settings["auto_delete"]
        else "❌ OFF"
    )

    credits = (
        "✅ ON"
        if settings["credits_enabled"]
        else "❌ OFF"
    )

    text = f"""
⚙️ Bot Settings

🗑 Auto Delete:
{auto_delete}

💰 Credits:
{credits}

🕒 Timer:
{settings['delete_timer']} sec

👥 Mode:
{settings['delete_mode']}
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Toggle Auto Delete",
                    callback_data="toggle_auto_delete"
                )
            ],
            [
                InlineKeyboardButton(
                    "Toggle Credits",
                    callback_data="toggle_credits"
                )
            ],
            [
                InlineKeyboardButton(
                    "Mode: FREE",
                    callback_data="mode_free"
                ),

                InlineKeyboardButton(
                    "Mode: ALL",
                    callback_data="mode_all"
                )
            ],
            [
                InlineKeyboardButton(
                    "Mode: PREMIUM",
                    callback_data="mode_premium"
                )
            ]
        ]
    )

    await message.reply_text(
        text,
        reply_markup=buttons
    )


@Client.on_callback_query(
    filters.regex("^toggle_auto_delete$")
)
async def toggle_auto_delete(
    client,
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):
        return

    settings = await get_settings()

    new_value = not settings[
        "auto_delete"
    ]

    await update_setting(
        "auto_delete",
        new_value
    )

    await callback.answer(
        "Updated"
    )

    return await callback.message.edit_text(
        f"🗑 Auto Delete = {new_value}"
    )


@Client.on_callback_query(
    filters.regex("^toggle_credits$")
)
async def toggle_credits(
    client,
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):
        return

    settings = await get_settings()

    new_value = not settings[
        "credits_enabled"
    ]

    await update_setting(
        "credits_enabled",
        new_value
    )

    await callback.answer(
        "Updated"
    )

    return await callback.message.edit_text(
        f"💰 Credits = {new_value}"
    )


@Client.on_callback_query(
    filters.regex("^mode_")
)
async def mode_handler(
    client,
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):
        return

    mode = callback.data.replace(
        "mode_",
        ""
    )

    await update_setting(
        "delete_mode",
        mode
    )

    await callback.answer(
        f"Mode = {mode}"
    )

    return await callback.message.edit_text(
        f"🗑 Delete Mode Updated\n\nMode: {mode}"
    )
