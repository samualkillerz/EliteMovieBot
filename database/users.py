from database.mongo import users_db


async def is_user_exist(user_id):
    user = await users_db.find_one(
        {"user_id": user_id}
    )
    return bool(user)


async def add_user(user_id, name):
    data = {
        "user_id": user_id,
        "name": name,
        "credits": 5,
        "joined": False,
        "unlocked": False,
        "referrals": 0,
        "daily_searches": 3,
        "premium": False,
        "banned": False
    }

    await users_db.insert_one(data)


async def get_user(user_id):
    return await users_db.find_one(
        {"user_id": user_id}
    )


async def add_credits(user_id, amount):
    await users_db.update_one(
        {"user_id": user_id},
        {"$inc": {"credits": amount}}
    )


async def remove_credits(user_id, amount):
    await users_db.update_one(
        {"user_id": user_id},
        {"$inc": {"credits": -amount}}
    )
