from database.mongo import requests_db


async def get_request(title):

    return await requests_db.find_one(
        {"title": title.lower()}
    )


async def create_request(title, user_id):

    data = {
        "title": title.lower(),
        "requesters": [user_id],
        "count": 1,
        "uploaded": False
    }

    await requests_db.insert_one(data)


async def add_request_user(title, user_id):

    await requests_db.update_one(
        {"title": title.lower()},
        {
            "$addToSet": {
                "requesters": user_id
            },
            "$inc": {
                "count": 1
            }
        }
    )


async def mark_uploaded(title):

    await requests_db.update_one(
        {"title": title.lower()},
        {
            "$set": {
                "uploaded": True
            }
        }
    )
