from aiogram import Router, types
from aiogram.filters import Command

from utils.logger import log_action
from utils.gamification_utils import get_user_profile

router = Router()

@router.message(Command("points"))
async def cmd_points(message: types.Message):
    """
    Handles the /points command by displaying the user's current points and badges.
    """
    user_id = message.from_user.id
    log_action("points_command", user_id)

    points, badges = await get_user_profile(user_id)

    response_text = f"🏆 **Your Profile** 🏆\n\n"
    response_text += f"**Points:** {points} ✨\n\n"

    if badges:
        response_text += "**Badges:**\n"
        for badge in badges:
            response_text += f"- {badge.icon} {badge.name}\n"
    else:
        response_text += "**Badges:**\n_You haven't earned any badges yet. Keep interacting with the bot to get them!_"

    await message.reply(response_text, parse_mode="Markdown")
