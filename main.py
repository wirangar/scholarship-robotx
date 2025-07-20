import json
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from config import TELEGRAM_BOT_TOKEN, DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Language and Content Loading ---
def load_text(lang, key):
    """Loads a text string from the language JSON files."""
    try:
        with open(f"lang/{lang}.json", "r", encoding="utf-8") as f:
            texts = json.load(f)
            return texts.get(key, f"_{key}_")
    except FileNotFoundError:
        with open(f"lang/{DEFAULT_LANGUAGE}.json", "r", encoding="utf-8") as f:
            texts = json.load(f)
            return texts.get(key, f"_{key}_")

# --- Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    user_lang = context.user_data.get("language", DEFAULT_LANGUAGE)

    welcome_message = load_text(user_lang, "welcome")

    main_menu_keyboard = [
        [load_text(user_lang, "scholarships"), load_text(user_lang, "accommodation")],
        [load_text(user_lang, "contact_us")],
    ]
    reply_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
