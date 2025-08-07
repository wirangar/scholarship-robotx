from aiogram.filters import Filter
from aiogram.types import Message
from config import ADMIN_CHAT_IDS

class AdminFilter(Filter):
    """
    A filter to check if a user is an admin.
    """
    async def __call__(self, message: Message) -> bool:
        # Ensure ADMIN_CHAT_IDS contains integers for comparison
        admin_ids = [int(admin_id) for admin_id in ADMIN_CHAT_IDS if str(admin_id).isdigit()]
        return message.from_user.id in admin_ids
