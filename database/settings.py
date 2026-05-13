from database.mongo import settings_db


async def save_thumb(file_id):

    await settings_db.update_one(
        {"_id": "thumb"},
        {
            "$set": {
                "file_id": file_id
            }
        },
        upsert=True
    )


async def get_thumb():

    data = await settings_db.find_one(
        {"_id": "thumb"}
    )

    if not data:
        return None

    return data.get("file_id")
