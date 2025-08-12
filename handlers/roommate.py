# -*- coding: utf-8 -*-
"""
Handler for the /roommate feature.
Allows users to create a profile and search for roommates.
"""
from telegram import Update, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from utils.gates import require_registration
from utils.gsheets import append_row, find_row_by_id, get_sheet_data, update_row
from utils.i18n import get_text

# --- Conversation States ---
MENU, CREATE_BUDGET, CREATE_LOCATION, CREATE_HABITS, CREATE_BIO, SEARCH = range(6)

@require_registration
async def start_roommate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays the main roommate menu."""
    lang = get_user_language(update.effective_user.id, context)
    buttons = [
        [InlineKeyboardButton(get_text('roommate_button_create', lang), callback_data="roommate_create_start")],
        [InlineKeyboardButton(get_text('roommate_button_search', lang), callback_data="roommate_search_start")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(get_text('roommate_welcome', lang), reply_markup=reply_markup)
    return MENU

# --- Profile Creation Flow ---

async def start_create_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the profile creation flow."""
    query = update.callback_query
    await query.answer()
    lang = get_user_language(update.effective_user.id, context)
    await query.edit_message_text(get_text('roommate_create_start', lang))
    return CREATE_BUDGET

async def ask_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves budget and asks for location."""
    lang = get_user_language(update.effective_user.id, context)
    try:
        context.user_data['roommate_budget'] = int(update.message.text)
    except ValueError:
        await update.message.reply_text(get_text('error_invalid_budget', lang))
        return CREATE_BUDGET
    await update.message.reply_text(get_text('roommate_ask_location', lang))
    return CREATE_LOCATION

async def ask_habits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves location and asks for habits."""
    lang = get_user_language(update.effective_user.id, context)
    context.user_data['roommate_location'] = update.message.text
    await update.message.reply_text(get_text('roommate_ask_habits', lang))
    return CREATE_HABITS

async def ask_bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves habits and asks for a short bio."""
    lang = get_user_language(update.effective_user.id, context)
    context.user_data['roommate_habits'] = update.message.text
    await update.message.reply_text(get_text('roommate_ask_bio', lang))
    return CREATE_BIO

async def save_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the complete profile to the 'roommates' sheet."""
    user = update.effective_user
    lang = get_user_language(update.effective_user.id, context)
    context.user_data['roommate_bio'] = update.message.text

    profile_data = [
        user.id,
        user.username or "", # Store username for contact
        context.user_data['roommate_budget'],
        context.user_data['roommate_location'],
        context.user_data['roommate_habits'],
        context.user_data['roommate_bio']
    ]

    # Check if user already has a profile to update it, otherwise create a new one.
    all_roommates = get_sheet_data('roommates')
    row_index = -1
    for i, row in enumerate(all_roommates):
        if len(row) > 0 and str(row[0]) == str(user.id):
            row_index = i + 1 # Google Sheets are 1-indexed
            break

    try:
        if row_index != -1:
            update_row('roommates', row_index, profile_data)
        else:
            append_row('roommates', profile_data)

        await update.message.reply_text(get_text('roommate_profile_saved', lang))
    except Exception as e:
        print(f"Failed to save roommate profile for {user.id}: {e}")
        await update.message.reply_text(get_text('roommate_error_saving', lang))

    # Cleanup
    for key in [k for k in context.user_data if k.startswith('roommate_')]:
        del context.user_data[key]

    return ConversationHandler.END

# --- Search Flow (Placeholder) ---

async def start_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Placeholder for the search functionality."""
    query = update.callback_query
    await query.answer()
    lang = get_user_language(update.effective_user.id, context)
    await query.edit_message_text(get_text('roommate_search_wip', lang))
    return ConversationHandler.END

# --- Conversation Handler Setup ---
roommate_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('roommate', start_roommate)],
    states={
        MENU: [
            CallbackQueryHandler(start_create_profile, pattern='^roommate_create_start$'),
            CallbackQueryHandler(start_search, pattern='^roommate_search_start$'),
        ],
        CREATE_BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_location)],
        CREATE_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_habits)],
        CREATE_HABITS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_bio)],
        CREATE_BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_profile)],
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
)
