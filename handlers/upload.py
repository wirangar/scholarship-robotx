# -*- coding: utf-8 -*-
"""
Handler for the /upload command.
Allows users to upload files to be stored in Google Drive.
"""
import datetime
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from utils.gates import require_registration
from utils.gdrive import upload_file_to_drive
from utils.gsheets import append_row
from utils.i18n import get_text

# --- Conversation States ---
WAITING_FILE = 0

# Supported MIME types
SUPPORTED_MIMETYPES = [
    'application/pdf',
    'image/jpeg',
    'image/png',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]
MAX_FILE_SIZE = 10 * 1024 * 1024 # 10 MB

@require_registration
async def start_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks the user to send a file."""
    lang = context.user_data.get('language', 'fa')
    await update.message.reply_text(get_text('upload_prompt', lang))
    return WAITING_FILE

async def process_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processes the received file, uploads it to Drive, and logs it in Sheets."""
    user = update.effective_user
    lang = context.user_data.get('language', 'fa')

    # Determine if the message contains a document or photo
    file_to_process = update.message.document or update.message.photo[-1] # Photo is a list of sizes

    if not file_to_process:
        await update.message.reply_text(get_text('error_upload_no_file', lang))
        return WAITING_FILE

    if file_to_process.file_size > MAX_FILE_SIZE:
        await update.message.reply_text(get_text('error_upload_too_large', lang))
        return WAITING_FILE

    if file_to_process.mime_type not in SUPPORTED_MIMETYPES:
        await update.message.reply_text(get_text('error_upload_mime_type', lang).format(mime_type=file_to_process.mime_type))
        return WAITING_FILE

    # Download the file into memory
    await update.message.reply_text(get_text('upload_processing', lang))
    try:
        tele_file = await file_to_process.get_file()
        file_content_bytes = await tele_file.download_as_bytearray()
    except Exception as e:
        await update.message.reply_text(get_text('error_upload_telegram_download', lang))
        return ConversationHandler.END

    # Upload to Google Drive
    file_id = upload_file_to_drive(
        file_content=bytes(file_content_bytes),
        filename=f"user_{user.id}_{file_to_process.file_name or 'photo.jpg'}",
        mimetype=file_to_process.mime_type
    )

    if not file_id:
        await update.message.reply_text(get_text('error_upload_drive', lang))
        return ConversationHandler.END

    # Log to Google Sheets
    try:
        log_data = [
            user.id,
            file_id,
            file_to_process.file_name or 'photo.jpg',
            file_to_process.mime_type,
            file_to_process.file_size,
            datetime.datetime.utcnow().isoformat()
        ]
        append_row('uploads', log_data)
    except Exception as e:
        # If logging fails, we should ideally handle it, maybe by deleting the Drive file
        # For now, we just log the error and inform the user.
        print(f"CRITICAL: Failed to log upload for file {file_id} from user {user.id}. Error: {e}")
        await update.message.reply_text(get_text('error_upload_log_failed', lang))
        return ConversationHandler.END

    await update.message.reply_text(get_text('upload_success', lang))
    return ConversationHandler.END

async def cancel_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the upload process."""
    lang = context.user_data.get('language', 'fa')
    await update.message.reply_text(get_text('upload_canceled', lang))
    return ConversationHandler.END

# --- Conversation Handler Setup ---
upload_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('upload', start_upload)],
    states={
        WAITING_FILE: [MessageHandler(filters.Document.ALL | filters.PHOTO, process_file)],
    },
    fallbacks=[CommandHandler('cancel', cancel_upload)],
)
