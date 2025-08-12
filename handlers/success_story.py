# -*- coding: utf-8 -*-
"""
Handler for the /success_story command.
Allows users to submit their success stories.
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
from utils.gdrive import upload_file_to_drive
from utils.i18n import get_text
from handlers.upload import MAX_FILE_SIZE

# --- Conversation States ---
GET_STORY, GET_PHOTO = range(2)

@require_registration
async def start_story(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the success story submission process."""
    lang = get_user_language(update.effective_user.id, context)
    await update.message.reply_text(get_text('story_start', lang))
    return GET_STORY

async def ask_for_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the story text and asks for an optional photo."""
    lang = get_user_language(update.effective_user.id, context)
    context.user_data['story_text'] = update.message.text

    buttons = [
        [InlineKeyboardButton(get_text('button_yes', lang), callback_data="story_photo_yes")],
        [InlineKeyboardButton(get_text('button_no', lang), callback_data="story_photo_no")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(get_text('story_ask_photo', lang), reply_markup=reply_markup)
    return GET_PHOTO

async def process_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processes the optional photo and saves the story."""
    user = update.effective_user
    lang = get_user_language(user.id, context)

    photo_file = update.message.photo[-1] # Get the largest size

    if photo_file.file_size > MAX_FILE_SIZE:
        await update.message.reply_text(get_text('error_upload_too_large', lang))
        return GET_PHOTO # Ask again

    await update.message.reply_text(get_text('upload_processing', lang))

    tele_file = await photo_file.get_file()
    file_content = await tele_file.download_as_bytearray()
    file_id = upload_file_to_drive(
        file_content=bytes(file_content),
        filename=f"story_{user.id}.jpg",
        mimetype='image/jpeg'
    )

    return await save_story(update, context, photo_file_id=file_id)


async def save_story(update: Update, context: ContextTypes.DEFAULT_TYPE, photo_file_id: str = None) -> int:
    """Saves the story to Google Sheets and ends the conversation."""
    query = update.callback_query
    if query:
        await query.answer()
        message = query.message
    else:
        message = update.message

    user = update.effective_user
    lang = get_user_language(user.id, context)

    try:
        story_data = [
            datetime.datetime.utcnow().isoformat(),
            user.id,
            user.full_name,
            context.user_data['story_text'],
            photo_file_id or "",
            'pending'
        ]
        append_row('success_stories', story_data)
        await message.reply_text(get_text('story_success', lang))
    except Exception as e:
        print(f"Failed to save success story for user {user.id}: {e}")
        await message.reply_text(get_text('error_general', lang))

    del context.user_data['story_text']
    return ConversationHandler.END

async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo step and saves the story."""
    return await save_story(update, context, photo_file_id=None)

# --- Conversation Handler Setup ---
success_story_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('success_story', start_story)],
    states={
        GET_STORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_photo)],
        GET_PHOTO: [
            CallbackQueryHandler(skip_photo, pattern='^story_photo_no$'),
            MessageHandler(filters.PHOTO, process_photo)
        ],
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
)
