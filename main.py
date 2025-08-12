# -*- coding: utf-8 -*-
"""
Main entry point for the Telegram Bot application.
Sets up the FastAPI server and the Telegram bot webhook.
"""
import asyncio
import uvicorn
from fastapi import FastAPI, Request, Response

import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler

from config import TELEGRAM_BOT_TOKEN, BASE_URL, WEBHOOK_SECRET, PORT, LOG_LEVEL
from utils.logger import get_logger, setup_bot_instance_for_logging
from utils.redis_utils import redis_client
from utils.gsheets import service as gsheets_service

# --- Import Handlers ---
from handlers import start_menu, register, isee, resources_hub, news, search, live_chat, weather, cost, language, profile, feedback, upload, discounts, simulation, consult, roommate
# ... other handlers will be imported here as they are implemented

# --- Logging ---
logger = get_logger(__name__)

# --- Bot and FastAPI Initialization ---
# Set up the Telegram Application
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# Pass bot instance to logger for admin alerts
setup_bot_instance_for_logging(application.bot)

# Set up the FastAPI app
app = FastAPI(
    title="Perugia Helper Bot",
    description="A Telegram bot to assist students and immigrants in Perugia.",
    version="1.0.0"
)

# --- Webhook and Health Check Endpoints ---

@app.on_event("startup")
async def on_startup():
    """
    Actions to perform on application startup.
    This includes setting the Telegram webhook.
    """
    webhook_url = f"{BASE_URL}/telegram/webhook"
    try:
        await application.bot.set_webhook(
            url=webhook_url,
            secret_token=WEBHOOK_SECRET,
            allowed_updates=Update.ALL_TYPES
        )
        logger.info(f"Webhook successfully set to {webhook_url}")
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")

    # Register handlers here
    application.add_handler(CommandHandler("start", start_menu.protected_start))
    application.add_handler(register.register_conv_handler)
    application.add_handler(isee.isee_conv_handler)

    # Add Resources Hub handlers
    application.add_handler(CommandHandler("hub", resources_hub.hub_main_menu))
    application.add_handler(CallbackQueryHandler(resources_hub.hub_main_menu, pattern='^hub_main$'))
    application.add_handler(CallbackQueryHandler(resources_hub.hub_callback_handler, pattern='^hub_'))

    # Add News handlers
    application.add_handler(CommandHandler("news", news.news_menu))
    application.add_handler(CallbackQueryHandler(news.news_menu, pattern='^news_page_'))

    # Add Search handler
    application.add_handler(search.search_conv_handler)

    # Add Live Chat handlers
    application.add_handler(live_chat.live_chat_conv_handler)
    application.add_handler(live_chat.admin_reply_handler)

    # Add Weather handler
    application.add_handler(weather.weather_conv_handler)

    # Add Cost of Living handler
    application.add_handler(cost.cost_conv_handler)

    # Add Language handler
    application.add_handler(language.language_conv_handler)

    # Add Profile handlers
    application.add_handler(profile.profile_handler)
    application.add_handler(profile.profile_callback)

    # Add Feedback handler
    application.add_handler(feedback.feedback_conv_handler)

    # Add Upload handler
    application.add_handler(upload.upload_conv_handler)

    # Add Discounts handlers
    application.add_handler(discounts.discounts_command_handler)
    application.add_handler(discounts.discounts_callback_handler)

    # Add Simulation handler
    application.add_handler(simulation.simulation_conv_handler)

    # Add Consultation handler
    application.add_handler(consult.consult_conv_handler)

    # Add Roommate handler
    application.add_handler(roommate.roommate_conv_handler)

    # The generic button handler from start_menu should be one of the last,
    # to act as a fallback for buttons not handled by more specific handlers.
    application.add_handler(CallbackQueryHandler(start_menu.button_handler))
    logger.info("Bot handlers successfully registered.")


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """
    Handles incoming updates from Telegram by passing them to the bot application.
    """
    # Validate the secret token
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        logger.warning("Invalid secret token received in webhook request.")
        return Response(status_code=403)

    try:
        async with asyncio.timeout(10): # Process updates with a 10s timeout
            update_data = await request.json()
            update = Update.de_json(update_data, application.bot)
            await application.process_update(update)
            return Response(status_code=200)
    except asyncio.TimeoutError:
        logger.error("Timeout processing webhook update.")
        return Response(status_code=504) # Gateway Timeout
    except Exception as e:
        logger.error(f"Error processing update: {e}", exc_info=True)
        return Response(status_code=500)


@app.get("/healthz", status_code=200)
def health_check():
    """Liveness probe: Checks if the server is running."""
    return {"status": "ok"}


@app.get("/readyz", status_code=200)
def readiness_check():
    """
    Readiness probe: Checks if the bot is ready to accept requests.
    Verifies connections to external services like Redis and Google Sheets.
    """
    # Check Redis connection
    try:
        if not redis_client or not redis_client.ping():
            logger.error("Readiness check failed: Redis connection error.")
            return Response(status_code=503, content='{"status": "service_unavailable", "service": "redis"}')
    except Exception as e:
        logger.error(f"Readiness check failed: Redis exception: {e}")
        return Response(status_code=503, content='{"status": "service_unavailable", "service": "redis"}')

    # Check Google Sheets connection
    if not gsheets_service:
        logger.error("Readiness check failed: Google Sheets service not available.")
        return Response(status_code=503, content='{"status": "service_unavailable", "service": "gsheets"}')

    return {"status": "ready"}


# --- Main Execution ---
if __name__ == "__main__":
    logger.info("Starting application server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        log_level=LOG_LEVEL.lower(),
        reload=True # Use reload for local development
    )
