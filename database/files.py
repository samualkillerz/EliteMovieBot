from database.mongo import files_db


async def get_file_by_unique(unique_id):

    return await files_db.find_one(
        {"unique_id": unique_id}
    )


async def add_file(data):

    await files_db.insert_one(data)
