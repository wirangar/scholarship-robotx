import json
import os
from aiogram import Router, types
from aiogram.filters import Command
from utils.logger import log_action

router = Router()

# Construct the absolute path to the lang directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG_DIR = os.path.join(BASE_DIR, "lang")

def load_lang(lang: str = "en") -> dict:
    """
    Loads the language JSON file.
    """
    lang_file_path = os.path.join(LANG_DIR, f"{lang}.json")
    try:
        with open(lang_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to English if the specified language is not found
        with open(os.path.join(LANG_DIR, "en.json"), "r", encoding="utf-8") as f:
            return json.load(f)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Handles the /start command.
    """
    # For now, we use the default language. Later, this can be tied to user profile.
    lang_data = load_lang()
    welcome_msg = lang_data.get("welcome_message", "Welcome to SmartStudentBot!")

    await message.reply(welcome_msg)
    log_action("start_command", message.from_user.id)
