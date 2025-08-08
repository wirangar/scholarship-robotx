from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import json
import os

from utils.db_utils import get_user_language
from utils.logger import log_action

router = Router()

# Define the path to the guide data file
GUIDE_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "guide.json")

def load_guide_data() -> dict:
    """Loads the guide.json file."""
    try:
        with open(GUIDE_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("data", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

@router.message(Command("guide"))
async def cmd_guide(message: types.Message):
    """
    Handles the /guide command.
    Displays a menu of guide topics based on the user's language.
    """
    user_id = message.from_user.id
    log_action("guide_command", user_id)

    lang_code = await get_user_language(user_id)
    guide_data = load_guide_data()

    lang_guide = guide_data.get(lang_code)
    if not lang_guide:
        # Fallback to English if the user's language has no guide content
        lang_guide = guide_data.get("en", {})

    if not lang_guide:
        await message.reply("Sorry, the guide is currently unavailable.")
        return

    builder = InlineKeyboardBuilder()
    for topic_key, topic_data in lang_guide.items():
        # The callback data will be like: guide_en_residency_permit
        builder.button(text=topic_data.get("title", topic_key), callback_data=f"guide_{lang_code}_{topic_key}")

    builder.adjust(1) # One button per row

    await message.reply("Here are some topics that might help you:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("guide_"))
async def show_guide_topic(callback_query: types.CallbackQuery):
    """
    Handles the selection of a guide topic.
    Displays the content for the selected topic.
    """
    # e.g., "guide_en_residency_permit" -> ["guide", "en", "residency_permit"]
    parts = callback_query.data.split("_")
    if len(parts) < 3:
        await callback_query.answer("Invalid selection.", show_alert=True)
        return

    lang_code = parts[1]
    topic_key = "_".join(parts[2:])

    guide_data = load_guide_data()
    topic_data = guide_data.get(lang_code, {}).get(topic_key)

    if not topic_data:
        await callback_query.answer("Content not found.", show_alert=True)
        return

    content = f"**{topic_data.get('title')}**\n\n{topic_data.get('content')}"

    # Create a "Back" button
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Back to Topics", callback_data="guide_back")

    await callback_query.message.edit_text(
        content,
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )
    await callback_query.answer()

@router.callback_query(F.data == "guide_back")
async def back_to_guide_menu(callback_query: types.CallbackQuery):
    """
    Handles the "Back" button, returning the user to the main guide menu.
    """
    # This is essentially the same logic as the /guide command,
    # but we edit the existing message instead of sending a new one.
    user_id = callback_query.from_user.id
    lang_code = await get_user_language(user_id)
    guide_data = load_guide_data()
    lang_guide = guide_data.get(lang_code) or guide_data.get("en", {})

    builder = InlineKeyboardBuilder()
    if lang_guide:
        for topic_key, topic_data in lang_guide.items():
            builder.button(text=topic_data.get("title", topic_key), callback_data=f"guide_{lang_code}_{topic_key}")
        builder.adjust(1)

    await callback_query.message.edit_text(
        "Here are some topics that might help you:",
        reply_markup=builder.as_markup()
    )
    await callback_query.answer()
