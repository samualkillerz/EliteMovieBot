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
        "referrals": 0,
        "unlocked": False
    }

    await users_db.insert_one(data)


async def get_user(user_id):

    return await users_db.find_one(
        {"user_id": user_id}
    )


async def add_referral(user_id):

    await users_db.update_one(
        {"user_id": user_id},
        {"$inc": {"referrals": 1}}
    )


async def unlock_user(user_id):

    await users_db.update_one(
        {"user_id": user_id},
        {"$set": {"unlocked": True}}
    )


async def deny_user(user_id):

    await users_db.update_one(
        {"user_id": user_id},
        {"$set": {"unlocked": False}}
    )

async def add_credits(user_id, amount):

    await users_db.update_one(
        {"user_id": user_id},
        {
            "$inc": {
                "credits": amount
            }
        }
    )


async def remove_credits(user_id, amount):

    await users_db.update_one(
        {"user_id": user_id},
        {
            "$inc": {
                "credits": -amount
            }
        }
    )

