# -*- coding: utf-8 -*-
"""
Tests for Telegram command handlers.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Mock the Google Sheets dependency for all handler tests in this file
# This prevents real API calls during testing.
from utils import gsheets
gsheets.find_row_by_id = MagicMock(return_value=None) # Default to user not found
gsheets.append_row = MagicMock()

from handlers import migration_status

# --- Mocks for telegram.ext objects ---

class MockUser:
    def __init__(self, user_id, full_name, username=None):
        self.id = user_id
        self.full_name = full_name
        self.username = username

class MockMessage:
    def __init__(self, text, user):
        self.text = text
        self.from_user = user
        self.reply_text = AsyncMock()

class MockUpdate:
    def __init__(self, message):
        self.effective_user = message.from_user
        self.message = message
        self.callback_query = None

class MockContext:
    def __init__(self):
        self.user_data = {}
        self.bot = MagicMock()
        self.bot.send_message = AsyncMock()

# --- Tests ---

@pytest.mark.asyncio
async def test_migration_status_handler():
    """
    Tests the simple /migration_status command handler.
    """
    # 1. Setup
    user = MockUser(user_id=123, full_name="Test User")
    message = MockMessage(text="/migration_status", user=user)
    update = MockUpdate(message)
    context = MockContext()
    context.user_data['language'] = 'en' # Explicitly set language for the test

    # 2. Make the user "registered" for the @require_registration gate
    # We patch the gate's dependency and the handler's language function
    with patch('utils.gates.find_row_by_id') as mock_find, \
         patch('handlers.migration_status.get_user_language') as mock_lang:

        mock_find.return_value = ['123', 'Test User', '30', 'Testland', 'CS', 'test@test.com', 'en']
        mock_lang.return_value = 'en'

        # 3. Call the handler
        await migration_status.show_migration_status(update, context)

    # 4. Assertions
    # Check that reply_text was called
    update.message.reply_text.assert_called_once()

    # Check that the reply contains expected text from the checklist
    args, kwargs = update.message.reply_text.call_args
    reply_text = args[0]
    assert "Migration & Residency Checklist" in reply_text
    assert "Apply for Residence Permit" in reply_text


from handlers import isee
from telegram.ext import ConversationHandler

@pytest.mark.asyncio
async def test_isee_conversation_flow():
    """
    Tests the full multi-step flow of the /isee ConversationHandler.
    """
    # 1. Setup
    user = MockUser(user_id=456, full_name="Isee User")
    context = MockContext()
    context.user_data['language'] = 'en'

    # --- Step 1: Start the conversation with /isee ---
    message1 = MockMessage("/isee", user)
    update1 = MockUpdate(message1)

    # Patch dependencies for the gate and the language function for the whole test
    with patch('utils.gates.find_row_by_id') as mock_find, \
         patch('handlers.isee.get_user_language') as mock_lang:

        # Setup the mocks' return values
        mock_find.return_value = ['456', 'Isee User', '25', 'Testland', 'Econ', 'isee@test.com', 'en']
        mock_lang.return_value = 'en'

        # --- Step 1: Start the conversation ---
        next_state = await isee.start_isee_conversation(update1, context)
        # Assertions for step 1
        update1.message.reply_text.assert_called_with(
            "This is an educational simulator for ISEE calculation. Results may not be exact.\n\n"
            "Please enter your annual family income in EUR:"
        )
        assert next_state == isee.INCOME

        # --- Step 2: User provides income ---
        message2 = MockMessage("40000", user)
        update2 = MockUpdate(message2)
        next_state = await isee.ask_property(update2, context)
        # Assertions for step 2
        update2.message.reply_text.assert_called_with(
            "Please enter the total size of your family's properties in square meters (0 if none):"
        )
        assert context.user_data['isee_income'] == 40000.0
        assert next_state == isee.PROPERTY

        # --- Step 3: User provides property size ---
        message3 = MockMessage("100", user)
        update3 = MockUpdate(message3)
        next_state = await isee.ask_family(update3, context)
        # Assertions for step 3
        update3.message.reply_text.assert_called_with("How many members are in your family?")
        assert context.user_data['isee_property'] == 100.0
        assert next_state == isee.FAMILY

        # --- Step 4: User provides family members, conversation ends ---
        message4 = MockMessage("3", user)
        update4 = MockUpdate(message4)
        next_state = await isee.calculate_and_finish(update4, context)

    # Assertions for step 4
    update4.message.reply_text.assert_called_once()
    args, kwargs = update4.message.reply_text.call_args
    final_reply = args[0]

    # ISEE = (40000 + (100 * 500 * 0.2)) / 2.04 = (40000 + 10000) / 2.04 = 24509.8
    assert "Your ISEE value: `24509.80`" in final_reply
    assert "Scholarship Status: `Partial`" in final_reply # It's over the 23000 threshold

    # Check that conversation ended
    assert next_state == ConversationHandler.END
    # Check that context was cleaned up
    assert 'isee_income' not in context.user_data
