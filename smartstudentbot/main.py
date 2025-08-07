import uvicorn
import os
from fastapi import FastAPI, Request, Response
from aiogram import Bot, Dispatcher, types
from config import TELEGRAM_BOT_TOKEN, BASE_URL, WEBHOOK_SECRET, BOT_ID, PORT
from utils.logger import logger

# Import handlers
from handlers import cmd_start, news_handler
from aiogram.fsm.storage.memory import MemoryStorage

# Initialize Bot and Dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
# Use MemoryStorage for FSM. For production, a persistent storage like Redis is recommended.
dp = Dispatcher(storage=MemoryStorage())

# Include routers
dp.include_router(cmd_start.router)
dp.include_router(news_handler.router)

# Initialize FastAPI app
app = FastAPI()

# Define the webhook endpoint
WEBHOOK_PATH = f"/{BOT_ID}/{WEBHOOK_SECRET}"

@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    """
    Handles incoming updates from Telegram.
    """
    telegram_update = await request.json()
    update = types.Update(**telegram_update)
    await dp.feed_update(bot=bot, update=update)
    return Response(status_code=200)

from utils.db_utils import init_db

@app.on_event("startup")
async def on_startup():
    """
    Actions to be performed on application startup.
    This includes initializing the database and setting the webhook.
    """
    logger.info("Initializing database...")
    await init_db()

    logger.info("Setting webhook...")
    webhook_url = f"{BASE_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(url=webhook_url)
    logger.info(f"Webhook set for bot {BOT_ID} at {webhook_url}")

@app.on_event("shutdown")
async def on_shutdown():
    """
    Actions to be performed on application shutdown.
    This includes deleting the webhook.
    """
    logger.info("Shutting down... Deleting webhook.")
    await bot.delete_webhook()

@app.get("/")
async def root():
    """
    Root endpoint for health checks.
    """
    return {"status": "ok", "bot_id": BOT_ID}

if __name__ == "__main__":
    # Note: Running this directly is for local development.
    # Production servers like Render will use a command like:
    # uvicorn main:app --host 0.0.0.0 --port 8000
    logger.info("Starting bot in polling mode for local development...")
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
