import time

cooldowns = {}


def check_cooldown(user_id, seconds):

    now = time.time()

    last = cooldowns.get(user_id, 0)

    remaining = seconds - (now - last)

    if remaining > 0:
        return round(remaining)

    cooldowns[user_id] = now

    return 0
