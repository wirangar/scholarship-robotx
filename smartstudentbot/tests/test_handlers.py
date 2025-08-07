import pytest
import sys
import os
from unittest.mock import AsyncMock, patch

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aiogram import Bot, Dispatcher
from aiogram.types import Message, Chat, User
from handlers.cmd_start import cmd_start


@pytest.mark.asyncio
async def test_cmd_start():
    """
    Tests the /start command handler.
    """
    # Mock the bot and dispatcher
    bot = Bot(token="123456789:AABBCCDDEEFFggHHIIJJkkLLMMNNOOPPqq")

    # Mock the message object
    chat = Chat(id=12345, type="private")
    user = User(id=12345, is_bot=False, first_name="Test", last_name="User", username="testuser")
    message = Message(
        message_id=1,
        date=1234567890,
        chat=chat,
        from_user=user,
        text="/start"
    )

    # Patch the reply method directly on the Message class for this test
    with patch('aiogram.types.Message.reply', new_callable=AsyncMock) as mock_reply:
        # Call the handler
        await cmd_start(message)

        # Assert that the reply method was called
        mock_reply.assert_called_once()

        # Assert that the reply message is correct
        args, _ = mock_reply.call_args
        assert "Welcome to SmartStudentBot!" in args[0]
