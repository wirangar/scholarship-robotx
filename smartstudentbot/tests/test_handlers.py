import pytest
import sys
import os
import importlib
from unittest.mock import AsyncMock, patch

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, Chat, User, Update, CallbackQuery

# Import the handler module itself to allow for reloading
from handlers import cmd_start as cmd_start_handler
from models_db import User as DBUser

@pytest.fixture
def bot():
    """Fixture to create a mocked, awaitable bot."""
    bot_mock = AsyncMock(spec=Bot)
    bot_mock.me = User(id=42, is_bot=True, first_name="Test Bot")
    return bot_mock

@pytest.fixture
async def dispatcher(bot):
    """Fixture to create a dispatcher with a fresh router for each test."""
    importlib.reload(cmd_start_handler)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(cmd_start_handler.router)
    dp["bot"] = bot # Pass bot to context
    return dp

@pytest.mark.asyncio
@patch('handlers.cmd_start.get_or_create_user')
async def test_cmd_start_shows_language_keyboard(mock_get_user, dispatcher, bot):
    """
    Tests that the /start command shows the language selection keyboard.
    """
    mock_get_user.return_value = DBUser(id=1, user_id=123, first_name="Test")
    chat = Chat(id=123, type="private")
    user = User(id=123, is_bot=False, first_name="Test")
    message = Message(message_id=1, date=1234567890, chat=chat, from_user=user, text="/start")

    await dispatcher.feed_update(bot, Update(update_id=1, message=message))

    bot.send_message.assert_called_once()
    args, kwargs = bot.send_message.call_args
    assert "Please select your language" in kwargs['text']
    assert kwargs['reply_markup'] is not None
    assert "English" in str(kwargs['reply_markup'])

@pytest.mark.asyncio
@patch('handlers.cmd_start.update_user_language')
async def test_language_selection_callback(mock_update_lang, dispatcher, bot):
    """
    Tests that selecting a language updates the DB and shows the correct message.
    """
    chat = Chat(id=123, type="private")
    user = User(id=123, is_bot=False, first_name="Test")
    message = Message(message_id=1, date=1234567890, chat=chat, from_user=user, text="...")

    callback_query = CallbackQuery(id="1", from_user=user, chat_instance="1", data="set_lang_fa", message=message)

    await dispatcher.feed_update(bot, Update(update_id=1, callback_query=callback_query))

    mock_update_lang.assert_called_once_with(user.id, "fa")

    bot.edit_message_text.assert_called_once()
    args, kwargs = bot.edit_message_text.call_args
    assert "خوش آمدید" in kwargs['text']
