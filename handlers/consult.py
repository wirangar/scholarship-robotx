# -*- coding: utf-8 -*-
"""
Handler for the /consult command.
A multi-step form for academic consultation requests.
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
from utils.gsheets import append_row
from utils.gdrive import upload_file_to_drive
from handlers.upload import MAX_FILE_SIZE
from utils.i18n import get_text

# Only PDF and DOCX are supported for CVs
CV_MIMETYPES = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]

# --- Conversation States ---
MAJOR, GPA, BUDGET, LANGUAGE, CV = range(5)

@require_registration
async def start_consult(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the consultation request form."""
    lang = get_user_language(update.effective_user.id, context)
    await update.message.reply_text(get_text('consult_start', lang))
    return MAJOR

async def ask_gpa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves major and asks for GPA."""
    lang = get_user_language(update.effective_user.id, context)
    context.user_data['consult_major'] = update.message.text
    await update.message.reply_text(get_text('consult_ask_gpa', lang))
    return GPA

async def ask_budget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves GPA and asks for budget."""
    lang = get_user_language(update.effective_user.id, context)
    context.user_data['consult_gpa'] = update.message.text
    await update.message.reply_text(get_text('consult_ask_budget', lang))
    return BUDGET

async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves budget and asks for language level."""
    lang = get_user_language(update.effective_user.id, context)
    context.user_data['consult_budget'] = update.message.text
    await update.message.reply_text(get_text('consult_ask_language', lang))
    return LANGUAGE

async def ask_cv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves language level and asks for a CV."""
    lang = get_user_language(update.effective_user.id, context)
    context.user_data['consult_language'] = update.message.text
    await update.message.reply_text(get_text('consult_ask_cv', lang))
    return CV

async def process_cv_and_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processes the CV, saves the full application, and ends the conversation."""
    user = update.effective_user
    lang = get_user_language(update.effective_user.id, context)

    cv_file = update.message.document
    if not cv_file or cv_file.mime_type not in CV_MIMETYPES:
        await update.message.reply_text(get_text('consult_error_cv_format', lang))
        return CV

    if cv_file.file_size > MAX_FILE_SIZE:
        await update.message.reply_text(get_text('error_upload_too_large', lang)) # Reuse from upload handler
        return CV

    await update.message.reply_text(get_text('consult_uploading_cv', lang))

    # Upload to Drive
    tele_file = await cv_file.get_file()
    file_content = await tele_file.download_as_bytearray()
    file_id = upload_file_to_drive(
        file_content=bytes(file_content),
        filename=f"consult_cv_{user.id}_{cv_file.file_name}",
        mimetype=cv_file.mime_type
    )

    if not file_id:
        await update.message.reply_text(get_text('consult_error_cv_upload', lang))
        return ConversationHandler.END

    # Save all data to Google Sheets
    try:
        consult_data = [
            datetime.datetime.utcnow().isoformat(),
            user.id,
            user.full_name,
            context.user_data['consult_major'],
            context.user_data['consult_gpa'],
            context.user_data['consult_budget'],
            context.user_data['consult_language'],
            file_id # Link to the CV in Google Drive
        ]
        append_row('consultations', consult_data)
        await update.message.reply_text(get_text('consult_success', lang))
    except Exception as e:
        print(f"Failed to save consultation for user {user.id}: {e}")
        await update.message.reply_text(get_text('consult_error_saving', lang))

    # Cleanup
    for key in [k for k in context.user_data if k.startswith('consult_')]:
        del context.user_data[key]

    return ConversationHandler.END

# --- Conversation Handler Setup ---
consult_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('consult', start_consult)],
    states={
        MAJOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_gpa)],
        GPA: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_budget)],
        BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_language)],
        LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_cv)],
        CV: [MessageHandler(filters.Document.ALL, process_cv_and_finish)],
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
)
