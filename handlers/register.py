# -*- coding: utf-8 -*-
"""
Handler for the user registration process (/register).
Uses a ConversationHandler to manage a multi-step form.
"""
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from utils.i18n import get_text
from utils.logger import get_logger
from utils.gsheets import append_row, find_row_by_id
from utils.common import is_valid_email, is_valid_age
from handlers.start_menu import protected_start

logger = get_logger(__name__)

# --- Conversation States ---
NAME, AGE, COUNTRY, MAJOR, EMAIL = range(5)

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Starts the registration conversation.
    Checks if the user is already registered.
    """
    user = update.effective_user
    lang = context.user_data.get('language', 'fa')

    # Check if user is already registered
    if find_row_by_id('users', user.id):
        await update.message.reply_text("You are already registered.")
        await protected_start(update, context)
        return ConversationHandler.END

    await update.message.reply_text(get_text('register_ask_name', lang))
    return NAME

async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the user's name and asks for their age."""
    user_input = update.message.text
    context.user_data['registration_name'] = user_input
    lang = context.user_data.get('language', 'fa')

    await update.message.reply_text(get_text('register_ask_age', lang))
    return AGE

async def ask_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the user's age and asks for their country."""
    user_input = update.message.text
    lang = context.user_data.get('language', 'fa')

    if not is_valid_age(user_input):
        await update.message.reply_text(get_text('invalid_input', lang) + " " + get_text('register_ask_age', lang))
        return AGE # Stay in the same state

    context.user_data['registration_age'] = int(user_input)
    await update.message.reply_text(get_text('register_ask_country', lang))
    return COUNTRY

async def ask_major(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the country and asks for the major."""
    user_input = update.message.text
    context.user_data['registration_country'] = user_input
    lang = context.user_data.get('language', 'fa')

    await update.message.reply_text(get_text('register_ask_major', lang))
    return MAJOR

async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the major and asks for the email."""
    user_input = update.message.text
    context.user_data['registration_major'] = user_input
    lang = context.user_data.get('language', 'fa')

    await update.message.reply_text(get_text('register_ask_email', lang))
    return EMAIL

async def complete_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the email, completes registration, and saves to Google Sheets."""
    user = update.effective_user
    user_input = update.message.text
    lang = context.user_data.get('language', 'fa')

    if not is_valid_email(user_input):
        await update.message.reply_text(get_text('invalid_input', lang) + " " + get_text('register_ask_email', lang))
        return EMAIL

    context.user_data['registration_email'] = user_input

    # --- Save data to Google Sheets ---
    user_data = [
        user.id,
        context.user_data['registration_name'],
        context.user_data['registration_age'],
        context.user_data['registration_country'],
        context.user_data['registration_major'],
        context.user_data['registration_email'],
        lang, # Save preferred language
        # Add other fields like notification preferences here
    ]

    try:
        append_row('users', user_data)
        logger.info(f"New user registered: {user.id} - {user_data[1]}")
        await update.message.reply_text(get_text('registration_success', lang), reply_markup=ReplyKeyboardRemove())

        # Clean up temporary data
        for key in [k for k in context.user_data if k.startswith('registration_')]:
            del context.user_data[key]

        # Forward to the main menu
        await protected_start(update, context)
        return ConversationHandler.END

    except Exception as e:
        logger.error(f"Failed to save user {user.id} to Google Sheets: {e}")
        await update.message.reply_text(get_text('error_general', lang), reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text("Registration canceled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


# --- Conversation Handler Setup ---
register_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('register', start_registration)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_country)],
        COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_major)],
        MAJOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, complete_registration)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    per_user=True,
    per_chat=True,
)
