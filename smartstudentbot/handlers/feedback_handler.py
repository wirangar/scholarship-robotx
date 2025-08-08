from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.logger import log_action

router = Router()

# Define FSM States for feedback submission
class FeedbackForm(StatesGroup):
    waiting_for_rating = State()
    waiting_for_text = State()

# Handler to start the feedback flow
@router.message(Command("feedback"))
async def cmd_feedback(message: types.Message, state: FSMContext):
    """
    Starts the feedback process by asking for a rating.
    """
    log_action("feedback_command_start", message.from_user.id)

    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.button(text="⭐" * i, callback_data=f"feedback_rating_{i}")
    builder.adjust(3, 2) # Adjust keyboard layout

    await message.reply(
        "We appreciate your feedback! Please rate your experience with the bot (1 to 5 stars).",
        reply_markup=builder.as_markup()
    )
    await state.set_state(FeedbackForm.waiting_for_rating)

# Handler for the rating callback
@router.callback_query(FeedbackForm.waiting_for_rating, F.data.startswith("feedback_rating_"))
async def process_rating_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Processes the rating and asks for the feedback text.
    """
    try:
        rating = int(callback_query.data.split("_")[-1])
        await state.update_data(rating=rating)
        await state.set_state(FeedbackForm.waiting_for_text)

        await callback_query.message.edit_text(
            f"You selected {'⭐' * rating}.\n"
            "Now, please write your feedback, suggestion, or bug report."
        )
    except (ValueError, IndexError):
        await callback_query.message.edit_text("Invalid selection. Please try again.")

    await callback_query.answer()

# Handler for the feedback text
@router.message(FeedbackForm.waiting_for_text, F.text)
async def process_feedback_text(message: types.Message, state: FSMContext):
    """
    Processes the feedback text, saves it to the DB, and ends the conversation.
    """
    from utils.db_utils import save_feedback

    user_data = await state.get_data()
    feedback_text = message.text
    rating = user_data.get("rating", 0)
    user_id = message.from_user.id

    # Save the feedback
    await save_feedback(user_id=user_id, rating=rating, text=feedback_text)

    log_action("feedback_submitted", user_id, f"Rating: {rating}")

    await message.reply("Thank you for your feedback! We appreciate your help in improving this bot.")

    # End the conversation
    await state.clear()
