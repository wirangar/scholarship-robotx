from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.logger import log_action
from utils.db_utils import get_or_create_user
from utils.common import load_language_data

router = Router()

from aiogram import Bot

@router.message(Command("start"))
async def cmd_start(message: types.Message, bot: Bot):
    """
    Handles the /start command.
    Greets the user, ensures they are in the database, and prompts them to select a language.
    """
    # Get or create the user in the database
    db_user = await get_or_create_user(message.from_user)
    log_action("start_command", message.from_user.id)

    # Create an inline keyboard for language selection
    builder = InlineKeyboardBuilder()
    builder.button(text="🇬🇧 English", callback_data="set_lang_en")
    builder.button(text="🇮🇷 فارسی", callback_data="set_lang_fa")
    builder.button(text="🇮🇹 Italiano", callback_data="set_lang_it")
    builder.adjust(1)  # Arrange buttons in a single column

    # Get a generic, multi-language greeting
    en_data = load_language_data("en")
    fa_data = load_language_data("fa")
    it_data = load_language_data("it")

    greeting_text = (
        f"{en_data.get('welcome_message', 'Welcome!')}\n"
        f"{fa_data.get('welcome_message', 'خوش آمدید!')}\n"
        f"{it_data.get('welcome_message', 'Benvenuto!')}\n\n"
        "Please select your language:"
    )
    # Use bot.send_message for easier mocking
    await bot.send_message(message.chat.id, greeting_text, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("set_lang_"))
async def set_language(callback_query: types.CallbackQuery):
    """
    Handles the language selection callback.
    Updates the user's language in the database and sends a confirmation.
    """
    from utils.db_utils import update_user_language

    lang_code = callback_query.data.split("_")[-1]
    user_id = callback_query.from_user.id

    await update_user_language(user_id, lang_code)
    log_action("set_language", user_id, f"Lang: {lang_code}")

    lang_data = load_language_data(lang_code)
    welcome_msg = lang_data.get("welcome_message", "Welcome!")

    await callback_query.message.edit_text(welcome_msg, reply_markup=None)
    await callback_query.answer()
