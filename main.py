import json
import logging
import asyncio
from fastapi import FastAPI, Request, Response
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import config
import database

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
        with open(f"lang/{config.DEFAULT_LANGUAGE}.json", "r", encoding="utf-8") as f:
            texts = json.load(f)
            return texts.get(key, f"_{key}_")

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

    user_lang = context.user_data.get("language", user.language_code or config.DEFAULT_LANGUAGE)
    if user_lang not in config.SUPPORTED_LANGUAGES:
        user_lang = config.DEFAULT_LANGUAGE
    context.user_data["language"] = user_lang

    welcome_message = load_text(user_lang, "welcome")

    main_menu_keyboard = [
        [load_text(user_lang, "scholarships"), load_text(user_lang, "accommodation")],
        [load_text(user_lang, "contact_us")],
    ]
    reply_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Add handlers to the application
ptb.add_handler(CommandHandler("start", start))

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
