from database.mongo import files_db
from utils.parser import normalize_query


async def get_file_by_unique(unique_id):

    return await files_db.find_one(
        {"unique_id": unique_id}
    )


async def add_file(data):

    await files_db.insert_one(data)



async def search_files(query):

    query = normalize_query(query)

    words = query.split()

    regex_pattern = ".*".join(words)

    files = files_db.find(
        {
            "search_name": {
                "$regex": regex_pattern,
                "$options": "i"
            }
        }
    ).limit(10)

    return await files.to_list(
        length=10
    )

async def get_file_by_link(link):

    return await files_db.find_one(
        {"deep_link": link}
    )


async def update_file_name(
    link,
    new_name,
    search_name
):

    await files_db.update_one(
        {"deep_link": link},
        {
            "$set": {
                "file_name": new_name,
                "search_name": search_name
            }
        }
    )


async def update_deep_link(
    old_link,
    new_link
):

    await files_db.update_one(
        {"deep_link": old_link},
        {
            "$set": {
                "deep_link": new_link
            }
        }
    )


