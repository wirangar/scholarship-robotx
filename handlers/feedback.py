# -*- coding: utf-8 -*-
"""
Handler for the /feedback command.
Collects user feedback and saves it to a Google Sheet.
"""
import datetime
from telegram import Update, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from utils.gates import require_registration
from utils.gsheets import append_row

# --- Conversation States ---
RATING, MESSAGE = range(2)

@require_registration
async def start_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks the user to rate their experience."""
    buttons = [
        InlineKeyboardButton(f"{'⭐'*i}", callback_data=f"feedback_rating_{i}") for i in range(1, 6)
    ]
    reply_markup = InlineKeyboardMarkup([buttons])
    # i18n
    await update.message.reply_text("How would you rate your experience with the bot?", reply_markup=reply_markup)
    return RATING

async def ask_for_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the rating and asks for a text message."""
    query = update.callback_query
    await query.answer()

    rating = int(query.data.split('_')[2])
    context.user_data['feedback_rating'] = rating

    await query.edit_message_text(text=f"You gave a rating of {rating} stars. Thank you!\n\nPlease send a message with your comments or suggestions.")
    return MESSAGE

async def save_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the complete feedback to Google Sheets."""
    user = update.effective_user
    rating = context.user_data.get('feedback_rating', 'N/A')
    message = update.message.text
    timestamp = datetime.datetime.utcnow().isoformat()

    feedback_data = [
        user.id,
        user.full_name,
        rating,
        message,
        timestamp
    ]

    try:
        append_row('feedback', feedback_data)
        # i18n
        await update.message.reply_text("Thank you for your feedback! It helps us improve the bot.")
    except Exception as e:
        # logger should be used here
        print(f"Failed to save feedback: {e}")
        await update.message.reply_text("Sorry, there was an error saving your feedback.")

    # Clean up context
    if 'feedback_rating' in context.user_data:
        del context.user_data['feedback_rating']

    return ConversationHandler.END

async def cancel_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the feedback conversation."""
    await update.message.reply_text("Feedback submission canceled.")
    if 'feedback_rating' in context.user_data:
        del context.user_data['feedback_rating']
    return ConversationHandler.END

# --- Conversation Handler Setup ---
feedback_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('feedback', start_feedback)],
    states={
        RATING: [CallbackQueryHandler(ask_for_message, pattern='^feedback_rating_')],
        MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_feedback)],
    },
    fallbacks=[CommandHandler('cancel', cancel_feedback)],
)
