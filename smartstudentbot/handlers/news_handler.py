import uuid
import os
import json
from datetime import datetime, timezone

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from filters import AdminFilter
from utils.logger import log_action

router = Router()

# Define the states for the news adding process
class AddNews(StatesGroup):
    waiting_for_content = State()
    waiting_for_confirmation = State()

@router.message(Command("news"), AdminFilter())
async def cmd_news(message: types.Message, state: FSMContext):
    """
    Handles the /news command for admins to start adding a new article.
    """
    await state.set_state(AddNews.waiting_for_content)
    await message.reply(
        "You've started the process of adding a new article.\n"
        "Please send the news content. It can be text, a photo with a caption, a video with a caption, or a document (PDF) with a caption."
    )
    log_action("news_command_start", message.from_user.id)

@router.message(AddNews.waiting_for_content, F.text | F.photo | F.video | F.document)
async def process_news_content(message: types.Message, state: FSMContext):
    """
    Handles the content submission for the news article.
    """
    news_type = ""
    file_id = None
    text = ""
    error_message = None

    if message.text:
        news_type = "text"
        text = message.text
    elif message.photo:
        news_type = "photo"
        file_id = message.photo[-1].file_id
        text = message.caption or ""
    elif message.video:
        news_type = "video"
        file_id = message.video.file_id
        text = message.caption or ""
    elif message.document:
        if "pdf" in message.document.mime_type:
            news_type = "pdf"
            file_id = message.document.file_id
            text = message.caption or ""
        else:
            error_message = "Unsupported document type. Please send a PDF file."

    if error_message:
        await message.reply(error_message)
        return

    # Store the news data in the FSM context
    news_item_data = {
        "id": str(uuid.uuid4()),
        "type": news_type,
        "text": text,
        "file_id": file_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "published": False
    }
    await state.update_data(news_item=news_item_data)

    # Transition to the confirmation state
    await state.set_state(AddNews.waiting_for_confirmation)

    # Show a preview to the admin
    await message.answer("Here is a preview of your news article:")
    if news_type == "text":
        await message.answer(text)
    elif news_type == "photo":
        await message.answer_photo(photo=file_id, caption=text)
    elif news_type == "video":
        await message.answer_video(video=file_id, caption=text)
    elif news_type == "pdf":
        await message.answer_document(document=file_id, caption=text)

    # Create confirmation keyboard
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="✅ Publish", callback_data="publish_news"),
            types.InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_news"),
        ]
    ])
    await message.answer("Do you want to publish this article to the channel?", reply_markup=keyboard)
    log_action("news_content_received", message.from_user.id, f"Type: {news_type}")

@router.callback_query(F.data == "cancel_news", AddNews.waiting_for_confirmation)
async def cancel_news_process(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Cancels the news adding process.
    """
    await state.clear()
    await callback_query.message.edit_text("Action canceled.")
    await callback_query.answer()
    log_action("news_process_canceled", callback_query.from_user.id)

@router.callback_query(F.data == "publish_news", AddNews.waiting_for_confirmation)
async def publish_news_process(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Publishes the news to the channel.
    """
    from utils.file_utils import save_news_item
    from config import CHANNEL_ID

    user_data = await state.get_data()
    news_item = user_data.get("news_item")

    if not news_item:
        await callback_query.message.edit_text("Error: Could not find news data. Please start over.")
        await state.clear()
        return

    # Save the news item to the JSON file
    save_news_item(news_item)

    # Broadcast the news to the channel
    bot = callback_query.bot
    news_type = news_item.get("type")
    text = news_item.get("text", "")
    file_id = news_item.get("file_id")

    try:
        if news_type == "text":
            await bot.send_message(chat_id=CHANNEL_ID, text=text)
        elif news_type == "photo":
            await bot.send_photo(chat_id=CHANNEL_ID, photo=file_id, caption=text)
        elif news_type == "video":
            await bot.send_video(chat_id=CHANNEL_ID, video=file_id, caption=text)
        elif news_type == "pdf":
            await bot.send_document(chat_id=CHANNEL_ID, document=file_id, caption=text)

        await callback_query.message.edit_text("✅ News published successfully!")
        log_action("news_published", callback_query.from_user.id, f"News ID: {news_item['id']}")

    except Exception as e:
        await callback_query.message.edit_text(f"❌ Failed to publish news. Error: {e}")
        log_action("news_publish_failed", callback_query.from_user.id, f"Error: {e}")

    finally:
        await state.clear()
        await callback_query.answer()
