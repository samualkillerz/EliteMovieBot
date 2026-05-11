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

    compact_query = query.replace(
        " ",
        ""
    )

    files = files_db.find(
        {
            "$or": [
                {
                    "search_name": {
                        "$regex": query,
                        "$options": "i"
                    }
                },
                {
                    "search_compact": {
                        "$regex": compact_query,
                        "$options": "i"
                    }
                }
            ]
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

    compact_name = search_name.replace(
        " ",
        ""
    )

    await files_db.update_one(
        {"deep_link": link},
        {
            "$set": {
                "file_name": new_name,
                "search_name": search_name,
                "search_compact": compact_name
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
