from pyrogram.errors import UserNotParticipant

from config import FORCE_SUB_CHANNELS


async def check_force_sub(client, user_id):

    for channel in FORCE_SUB_CHANNELS:

        try:

            member = await client.get_chat_member(
                channel,
                user_id
            )

            if member.status in [
                "left",
                "kicked"
            ]:
                return False

        except UserNotParticipant:
            return False

        except Exception:
            return False

    return True
