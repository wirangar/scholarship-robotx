from aiogram import Router, types
from aiogram.filters import Command

from utils.logger import log_action
from utils.weather_api import get_current_weather
from config import CITY_NAME

router = Router()

@router.message(Command("weather"))
async def cmd_weather(message: types.Message):
    """
    Handles the /weather command by fetching and displaying
    the current weather for the bot's configured city.
    """
    log_action("weather_command", message.from_user.id)

    # Show a "typing..." status to the user
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    weather_report = await get_current_weather(CITY_NAME)

    await message.reply(weather_report, parse_mode="Markdown")
