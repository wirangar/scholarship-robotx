from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import json
import os

from utils.logger import log_action

router = Router()

DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "success_stories.json")

def load_stories_data() -> list:
    """Loads the success_stories.json file."""
    try:
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("data", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def format_story(story: dict, current: int, total: int) -> str:
    """Formats a single story for display."""
    return (
        f"**Success Story ({current}/{total})**\n\n"
        f"👤 **Author:** {story.get('author', 'N/A')}\n"
        f"🎓 **Field:** {story.get('field', 'N/A')}\n\n"
        f"_{story.get('story', 'No story text.')}_"
    )

def get_story_keyboard(current_index: int, total_stories: int) -> types.InlineKeyboardMarkup:
    """Creates the navigation keyboard for stories."""
    builder = InlineKeyboardBuilder()

    # Previous button (disabled if it's the first story)
    prev_disabled = current_index == 0
    builder.button(text="⬅️ Previous", callback_data=f"story_nav_{current_index - 1}")

    # Next button (disabled if it's the last story)
    next_disabled = current_index == total_stories - 1
    builder.button(text="Next ➡️", callback_data=f"story_nav_{current_index + 1}")

    # Manually disable buttons if needed (visual cue, not functional disablement in this simple case)
    # A better implementation would involve not adding the button or using a placeholder callback

    return builder.as_markup()


@router.message(Command("success_story"))
async def cmd_success_story(message: types.Message):
    """
    Handles the /success_story command by showing the first story.
    """
    log_action("success_story_command", message.from_user.id)

    stories = load_stories_data()
    if not stories:
        await message.reply("Sorry, no success stories are available right now.")
        return

    story_index = 0
    story = stories[story_index]
    total = len(stories)

    text = format_story(story, story_index + 1, total)
    keyboard = get_story_keyboard(story_index, total)

    await message.reply(text, reply_markup=keyboard, parse_mode="Markdown")

@router.callback_query(F.data.startswith("story_nav_"))
async def navigate_stories(callback_query: types.CallbackQuery):
    """
    Handles navigation between success stories.
    """
    try:
        new_index = int(callback_query.data.split("_")[-1])
    except (ValueError, IndexError):
        await callback_query.answer("Invalid action.", show_alert=True)
        return

    stories = load_stories_data()
    total = len(stories)

    if not 0 <= new_index < total:
        await callback_query.answer("You've reached the end of the stories.", show_alert=True)
        return

    story = stories[new_index]
    text = format_story(story, new_index + 1, total)
    keyboard = get_story_keyboard(new_index, total)

    await callback_query.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback_query.answer()
