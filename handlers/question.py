# -*- coding: utf-8 -*-
"""
Handler for the /question command.
Allows users to ask questions and saves them for admins to answer.
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
from utils.gsheets import append_row, get_sheet_data
from utils.i18n import get_text
from utils.common import sanitize_markdown

# --- Conversation States ---
GET_QUESTION, HANDLE_SUGGESTIONS = range(2)

def search_faq(query: str) -> list:
    """Searches the 'questions' sheet for already answered questions."""
    faq_data = get_sheet_data('questions')
    matches = []
    if not faq_data:
        return matches

    query_words = set(query.lower().split())

    for row in faq_data:
        # Assuming format: ID, UserID, Question, Answer, Status
        if len(row) >= 5 and row[4].lower() == 'answered':
            question_text = row[2].lower()
            question_words = set(question_text.split())
            # Simple matching: at least 2 words in common
            if len(query_words.intersection(question_words)) >= 2:
                matches.append({'question': row[2], 'answer': row[3]})
    return matches[:3] # Return top 3 matches

@require_registration
async def start_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks the user to type their question."""
    lang = get_user_language(update.effective_user.id, context)
    await update.message.reply_text(get_text('qna_ask_question', lang))
    return GET_QUESTION

async def process_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the question or shows suggestions if matches are found."""
    user = update.effective_user
    lang = get_user_language(user.id, context)
    question_text = update.message.text
    context.user_data['user_question'] = question_text

    # Search for similar questions
    suggestions = search_faq(question_text)

    if suggestions:
        context.user_data['qna_suggestions'] = suggestions
        text = get_text('qna_suggestions_found', lang)
        for i, sug in enumerate(suggestions):
            text += f"\n\n*Q: {sanitize_markdown(sug['question'])}*\nA: {sanitize_markdown(sug['answer'])}"

        buttons = [[InlineKeyboardButton(get_text('qna_submit_anyway', lang), callback_data="qna_submit_anyway")]]
        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='MarkdownV2')
        return HANDLE_SUGGESTIONS
    else:
        # No suggestions, save directly
        return await save_question(update, context)

async def save_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the question to the Google Sheet."""
    query = update.callback_query
    if query:
        await query.answer()
        message = query.message
    else:
        message = update.message

    user = update.effective_user
    lang = get_user_language(user.id, context)
    question_text = context.user_data.get('user_question', 'N/A')

    try:
        question_data = [
            len(get_sheet_data('questions')) + 1, # Simple ID
            user.id,
            question_text,
            "", # Answer
            "pending", # Status
            datetime.datetime.utcnow().isoformat()
        ]
        append_row('questions', question_data)
        await message.reply_text(get_text('qna_success', lang))
    except Exception as e:
        print(f"Failed to save question for user {user.id}: {e}")
        await message.reply_text(get_text('error_general', lang))

    if 'user_question' in context.user_data: del context.user_data['user_question']
    if 'qna_suggestions' in context.user_data: del context.user_data['qna_suggestions']

    return ConversationHandler.END

# --- Conversation Handler Setup ---
question_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('question', start_question)],
    states={
        GET_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_question)],
        HANDLE_SUGGESTIONS: [CallbackQueryHandler(save_question, pattern='^qna_submit_anyway$')]
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
)
