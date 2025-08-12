# -*- coding: utf-8 -*-
"""
Handler for the /start command and the main menu.
"""
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes

from utils.i18n import get_text
from utils.gates import require_registration, get_user_language
from utils.common import build_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /start command.
    If the user is registered, it shows the main menu.
    If not, it prompts them to register.
    """
    user = update.effective_user
    lang = get_user_language(user.id, context)

    # The @require_registration gate will handle non-registered users.
    # If the gate passes, we show the main menu.

    # We check if the user is registered again here to decide which welcome message to show.
    # The gate already protects the function, but we might want a different message for first-time /start after registration.
    if context.user_data.get('is_registered', False):
         # This is a returning user
        text = get_text('main_menu_title', lang)
    else:
        # First time seeing the menu after registration
        context.user_data['is_registered'] = True # Mark that they've seen the menu once
        text = get_text('registration_success', lang) + "\n\n" + get_text('main_menu_title', lang)

    # --- Build Main Menu Keyboard ---
    buttons = [
        InlineKeyboardButton(get_text('button_res_hub', lang), callback_data='hub_main'),
        InlineKeyboardButton(get_text('button_scholarships', lang), callback_data='scholarships_main'),
        InlineKeyboardButton(get_text('button_isee', lang), callback_data='isee_start'),
        InlineKeyboardButton(get_text('button_weather', lang), callback_data='weather_main'),
        InlineKeyboardButton(get_text('button_news', lang), callback_data='news_main'),
        InlineKeyboardButton(get_text('button_fx', lang), callback_data='fx_main'),
        InlineKeyboardButton(get_text('button_profile', lang), callback_data='profile_view'),
        InlineKeyboardButton(get_text('button_roommate', lang), callback_data='roommate_main'),
        InlineKeyboardButton(get_text('button_live_chat', lang), callback_data='live_chat_start'),
    ]

    reply_markup = build_menu(buttons, n_cols=3)

    # If it's a command, reply. If it's from a callback (like 'back_to_main_menu'), edit the message.
    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)


@require_registration
async def protected_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """A wrapper for the start command that enforces registration."""
    await start(update, context)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Generic callback query handler.
    It routes callback data to the appropriate function.
    """
    query = update.callback_query
    await query.answer() # Acknowledge the button press

    command = query.data

    # This is a simple router. In a larger app, this could be more sophisticated.
    if command == 'main_menu':
        await start(update, context)
    elif command == 'isee_start':
        # This will be handled by the ISEE conversation handler's entry point
        # We need to make sure the ISEE handler is triggered.
        # For now, we can just edit the message to show that the button works.
        from handlers.isee import start_isee_conversation # Avoid circular import
        await start_isee_conversation(update, context)
    elif command == 'register_start':
        from handlers.register import start_registration # Avoid circular import
        await start_registration(update, context)
    else:
        # Placeholder for other buttons
        lang = get_user_language(update.effective_user.id, context)
        await query.edit_message_text(text=f"'{command}' is not implemented yet.", reply_markup=None)

        # Example of how to build a back button
        back_button = InlineKeyboardButton(get_text('button_back', lang), callback_data='main_menu')
        reply_markup = build_menu([], n_cols=1, footer_buttons=back_button)
        await query.edit_message_text(text=f"'{command}' is not implemented yet.", reply_markup=reply_markup)
