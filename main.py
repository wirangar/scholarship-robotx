import logging
import asyncio
from fastapi import FastAPI, Request, Response
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

import config
import database
import content_manager as cm

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Helper Functions ---
def get_user_lang(context: ContextTypes.DEFAULT_TYPE, user) -> str:
    """Gets the user's language, falling back to defaults."""
    lang = context.user_data.get("language", user.language_code if user else config.DEFAULT_LANGUAGE)
    if lang not in config.SUPPORTED_LANGUAGES:
        return config.DEFAULT_LANGUAGE
    return lang

# --- Telegram Bot Setup ---
ptb = (
    Application.builder()
    .token(config.TELEGRAM_TOKEN)
    .read_timeout(30)
    .write_timeout(30)
    .build()
)

# --- Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message and saves the user to the database."""
    user = update.effective_user
    if user:
        database.upsert_user(user)

    lang = get_user_lang(context, user)
    context.user_data["language"] = lang

    # Using the new content manager
    welcome_message = cm.get_text('main_menu.title', lang) # A more appropriate welcome

    # Dynamically create the main menu from content.json
    menu_keys = cm.get_text('main_menu.buttons', lang)
    buttons = [InlineKeyboardButton(cm.get_text(f'{key}.title', lang), callback_data=key) for key in menu_keys]

    # A simple way to create a 2-column layout
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        # If we came here from a back button, edit the message
        await update.callback_query.edit_message_text(text=welcome_message, reply_markup=reply_markup)
    else:
        # Otherwise, send a new message
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles all callback queries from inline buttons."""
    query = update.callback_query
    await query.answer() # Acknowledge the button press

    path = query.data
    lang = get_user_lang(context, update.effective_user)

    # Check if the path leads to a sub-menu (has 'options' or 'buttons')
    submenu_keys = cm.get_text(f'{path}.options', lang) or cm.get_text(f'{path}.buttons', lang)

    if isinstance(submenu_keys, dict): # 'options' gives a dict of items
        buttons = [
            InlineKeyboardButton(
                cm.get_text(f'{path}.options.{key}.title', lang),
                callback_data=f'{path}.options.{key}'
            ) for key in submenu_keys
        ]
        keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
        text = cm.get_text(f'{path}.description', lang) or cm.get_text(f'{path}.title', lang)

    elif isinstance(submenu_keys, list): # 'buttons' gives a list of keys
        buttons = [
            InlineKeyboardButton(
                cm.get_text(f'{key}.title', lang),
                callback_data=key
            ) for key in submenu_keys
        ]
        keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
        text = cm.get_text(f'{path}.description', lang) or cm.get_text(f'{path}.title', lang)

    else:
        # This is a leaf node, display the details
        details = cm.get_text(f'{path}.details', lang)
        title = cm.get_text(f'{path}.title', lang)

        # Nicely format the details
        text = f"*{title}*\n\n"
        if isinstance(details, str):
            text += details
        elif isinstance(details, dict):
            for key, value in details.items():
                text += f"*{key.replace('_', ' ').title()}:* {value}\n"

        # Also check for other fields like 'requirements' or 'deadline'
        requirements = cm.get_text(f'{path}.requirements', lang)
        if isinstance(requirements, list):
            text += "\n*Requirements:*\n- " + "\n- ".join(requirements)

        deadline = cm.get_text(f'{path}.deadline', lang)
        if isinstance(deadline, str):
            text += f"\n*Deadline:* {deadline}"

        keyboard = []

    # Add a "Back" button, except for the main menu
    if '.' in path: # A simple way to check if we are in a sub-menu
        parent_path = ".".join(path.split('.')[:-2]) # Go back to the parent 'options' or 'buttons' level
        if not parent_path: # If parent is top-level category like 'scholarships'
             parent_path = 'main_menu' # Special case to go back to main menu

        # If we are at the top level of a category, the back button should go to the main menu.
        if path in cm.get_text('main_menu.buttons', lang):
            parent_path = 'main_menu'

        back_text = cm.get_text(f'main_menu.title', lang) # Simplified back text
        if parent_path != 'main_menu':
            back_text = f"« {cm.get_text(f'{parent_path}.title', lang)}"
        else:
            back_text = "« " + back_text

        # Special handler for main menu 'start'
        back_callback = parent_path if parent_path != 'main_menu' else 'start'
        keyboard.append([InlineKeyboardButton(back_text, callback_data=back_callback)])


    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')


# Add handlers to the application
ptb.add_handler(CommandHandler("start", start))
ptb.add_handler(CallbackQueryHandler(button_handler, pattern=lambda d: d != 'start'))
# Special handler for the 'back to main menu' button
ptb.add_handler(CallbackQueryHandler(start, pattern='start'))

# --- FastAPI Web Server ---
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """On startup, initialize the database and set the webhook."""
    logger.info("Initializing database...")
    database.initialize_db()

    logger.info("Setting up webhook...")
    webhook_url = f"{config.BASE_URL}/telegram"
    await ptb.bot.set_webhook(
        url=webhook_url,
        secret_token=config.WEBHOOK_SECRET,
        allowed_updates=Update.ALL_TYPES
    )
    logger.info(f"Webhook set to {webhook_url}")

@app.on_event("shutdown")
async def shutdown_event():
    """On shutdown, delete the webhook."""
    logger.info("Deleting webhook...")
    await ptb.bot.delete_webhook()
    logger.info("Webhook deleted.")

@app.post("/telegram")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram updates."""
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret_token != config.WEBHOOK_SECRET:
        logger.warning("Invalid secret token received.")
        return Response(status_code=403)

    try:
        update_data = await request.json()
        update = Update.de_json(update_data, ptb.bot)
        await ptb.process_update(update)
        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Error processing update: {e}", exc_info=True)
        return Response(status_code=500)

@app.get("/")
def index():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "GlobalGuide Bot is running"}

# --- To run the app locally for development ---
# Note: For production, use a Gunicorn/Uvicorn worker.
# Example: uvicorn main:app --host 0.0.0.0 --port 8080
if __name__ == "__main__":
    import uvicorn
    # This is for local development only and should not be used in production.
    # It doesn't set up the webhook. For that, you need a tool like ngrok
    # or to deploy to a server like Render.

    # To properly test with a webhook locally:
    # 1. Run: uvicorn main:app --host 0.0.0.0 --port 8080
    # 2. Use ngrok to expose your local server: ngrok http 8080
    # 3. Take the ngrok URL (e.g., https://your-ngrok-url.ngrok.io) and set it as BASE_URL in your .env
    # 4. Restart the uvicorn server. It will set the webhook on startup.

    logger.info("Running in local development mode (polling).")
    ptb.run_polling()
