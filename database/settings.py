from database.mongo import settings_db


DEFAULT_SETTINGS = {
    "_id": "main",

    "credits_enabled": False,

    "auto_delete": False,

    "delete_mode": "free",

    "delete_timer": 120
}


async def get_settings():

    settings = await settings_db.find_one(
        {"_id": "main"}
    )

    if not settings:

        await settings_db.insert_one(
            DEFAULT_SETTINGS
        )

        settings = DEFAULT_SETTINGS

    return settings


async def update_setting(
    key,
    value
):

    await settings_db.update_one(
        {"_id": "main"},
        {
            "$set": {
                key: value
            }
        }
    )
