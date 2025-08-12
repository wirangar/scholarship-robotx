# -*- coding: utf-8 -*-
"""
Handler for the /profile command.
Allows users to view and manage their data.
"""
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from utils.gates import require_registration
from utils.gsheets import find_row_by_id
from utils.common import build_menu, sanitize_markdown

@require_registration
async def view_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays the user's profile information fetched from Google Sheets.
    """
    user = update.effective_user

    # Fetch user data from the 'users' sheet
    # Column mapping: 0:id, 1:name, 2:age, 3:country, 4:major, 5:email
    user_data = find_row_by_id('users', user.id, id_column_index=0)

    if not user_data:
        # This case should ideally not be reached due to the @require_registration gate
        await update.message.reply_text("Could not find your profile. Please try registering again with /register.")
        return

    try:
        name = sanitize_markdown(user_data[1])
        age = sanitize_markdown(user_data[2])
        country = sanitize_markdown(user_data[3])
        major = sanitize_markdown(user_data[4])
        email = sanitize_markdown(user_data[5])
    except IndexError:
        await update.message.reply_text("Your profile data seems incomplete. Please contact an admin.")
        return

    text = (
        f"👤 *Your Profile*\n\n"
        f"*Name*: {name}\n"
        f"*Age*: {age}\n"
        f"*Country*: {country}\n"
        f"*Field of Study*: {major}\n"
        f"*Email*: {email}"
    )

    buttons = [
        InlineKeyboardButton("✏️ Edit Profile", callback_data="edit_profile_start"), # Placeholder
        InlineKeyboardButton("🗑️ Delete My Data", callback_data="delete_me_confirm") # GDPR
    ]

    # Add a back button to the main bot menu
    footer_buttons = [
        InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')
    ]
    reply_markup = build_menu(buttons, n_cols=2, footer_buttons=footer_buttons)

    await update.message.reply_text(text, parse_mode='MarkdownV2', reply_markup=reply_markup)

async def delete_me_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asks for confirmation before deleting user data."""
    query = update.callback_query
    await query.answer()

    text = (
        "⚠️ *Are you sure?*\n\n"
        "This will permanently delete all your data, including your profile, "
        "activity, and any uploaded files. This action cannot be undone."
    )
    buttons = [
        InlineKeyboardButton("✅ Yes, Delete Everything", callback_data="delete_me_execute"),
        InlineKeyboardButton("❌ No, Keep My Data", callback_data="profile_view") # Go back to profile view
    ]
    reply_markup = InlineKeyboardMarkup([buttons])
    await query.edit_message_text(text, parse_mode='MarkdownV2', reply_markup=reply_markup)

async def delete_me_execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the actual data deletion.
    (This is a placeholder and needs careful implementation).
    """
    query = update.callback_query
    await query.answer()

    # --- Deletion Logic ---
    # 1. Find the row number in Google Sheets and delete it.
    # 2. Find all user files in Google Drive and delete them.
    # 3. Clear any related data from Redis.
    # 4. Remove the user from the local cache in gates.py

    # For now, we'll just simulate it.
    text = "Your data deletion request has been processed. Thank you for using the bot."
    await query.edit_message_text(text)


async def profile_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles callbacks from the profile view."""
    query = update.callback_query
    command = query.data

    if command == 'profile_view':
        # Re-display the profile. We need to get the message object to edit it.
        # A simple way is to just call the main function again.
        # view_profile expects a message, not a callback query, so we adapt.
        await query.message.delete() # delete the old message
        await view_profile(query.message.reply_to_message or query.message, context) # call with original message
    elif command == 'delete_me_confirm':
        await delete_me_confirmation(update, context)
    elif command == 'delete_me_execute':
        await delete_me_execute(update, context)
    elif command == 'edit_profile_start':
        await query.answer("This feature is not yet implemented.", show_alert=True)


# Command handler to be added to main.py
profile_handler = CommandHandler('profile', view_profile)
# Callback handler to be added to main.py
profile_callback = CallbackQueryHandler(profile_callback_handler, pattern='^(profile_view|delete_me_confirm|delete_me_execute|edit_profile_start)$')
