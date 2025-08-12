# -*- coding: utf-8 -*-
"""
Handler for the /language command.
Provides simple language lessons.
"""
import json
from telegram import Update, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
)

from utils.gates import require_registration, get_user_language
from utils.common import build_menu
from utils.i18n import get_text

# --- Conversation States ---
CATEGORY_SELECTION, PHRASE_VIEW = range(2)
DATA_FILE_PATH = "data/languages.json"
PHRASES_PER_PAGE = 5

def get_language_data() -> dict:
    """Loads the language data from the JSON file."""
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

@require_registration
async def start_language_lessons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays the language lesson categories."""
    lang = get_user_language(update.effective_user.id, context)
    language_data = get_language_data()

    if not language_data or 'categories' not in language_data:
        await update.message.reply_text(get_text('error_language_unavailable', lang))
        return ConversationHandler.END

    buttons = [
        InlineKeyboardButton(
            cat.get(f'title_{lang}', cat.get('title_en')),
            callback_data=f"lang_cat_{cat['id']}_0"
        ) for cat in language_data['categories']
    ]

    footer_buttons = [InlineKeyboardButton(get_text('button_back', lang), callback_data='main_menu')]
    reply_markup = build_menu(buttons, n_cols=2, footer_buttons=footer_buttons)

    text = get_text('language_select_category', lang)

    if update.callback_query:
        # This happens when user clicks "Back to categories"
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)

    return CATEGORY_SELECTION

async def show_phrases(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays phrases for a selected category with pagination."""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update.effective_user.id, context)
    # e.g., "lang_cat_greetings_0"
    _, _, category_id, page_str = query.data.split('_')
    page = int(page_str)

    language_data = get_language_data()
    category = next((cat for cat in language_data['categories'] if cat['id'] == category_id), None)

    if not category:
        await query.edit_message_text(get_text('error_category_not_found', lang))
        return CATEGORY_SELECTION

    phrases = category['phrases']
    start_index = page * PHRASES_PER_PAGE
    end_index = start_index + PHRASES_PER_PAGE
    paginated_phrases = phrases[start_index:end_index]

    cat_title = category.get(f'title_{lang}', category.get('title_en'))
    text = f"🇮🇹 *{cat_title}*\n\n"
    for phrase in paginated_phrases:
        text += f"▪️ *{phrase['it']}*\n"
        text += f"  - _{phrase.get(lang, phrase.get('en'))}_\n\n"

    # --- Pagination Buttons ---
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton(get_text('button_previous', lang), callback_data=f"lang_cat_{category_id}_{page-1}"))
    if end_index < len(phrases):
        pagination_buttons.append(InlineKeyboardButton(get_text('button_next', lang), callback_data=f"lang_cat_{category_id}_{page+1}"))

    footer_buttons = [InlineKeyboardButton(get_text('button_back_to_categories', lang), callback_data="lang_start")]

    menu = []
    if pagination_buttons:
        menu.append(pagination_buttons)
    menu.append(footer_buttons)
    reply_markup = InlineKeyboardMarkup(menu)

    await query.edit_message_text(text, parse_mode='MarkdownV2', reply_markup=reply_markup)
    return CATEGORY_SELECTION


# --- Conversation Handler Setup ---
language_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('language', start_language_lessons)],
    states={
        CATEGORY_SELECTION: [
            CallbackQueryHandler(show_phrases, pattern='^lang_cat_'),
            CallbackQueryHandler(start_language_lessons, pattern='^lang_start$')
        ],
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
    # Add a callback handler for main_menu to exit the conversation
    map_to_parent={
        ConversationHandler.END: ConversationHandler.END,
    }
)
