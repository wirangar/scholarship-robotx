# -*- coding: utf-8 -*-
"""
Handler for the /discounts command.
Displays a list of student discounts.
"""
import json
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from utils.gates import require_registration, get_user_language
from utils.common import build_menu, sanitize_markdown
from utils.i18n import get_text

DATA_FILE_PATH = "data/discounts.json"
DISCOUNTS_PER_PAGE = 3

def get_discounts_data() -> dict:
    """Loads the discounts data from the JSON file."""
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

@require_registration
async def show_discounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays a paginated list of discounts."""
    lang = get_user_language(update.effective_user.id, context)

    page = 0
    if update.callback_query:
        await update.callback_query.answer()
        try:
            page = int(update.callback_query.data.split('_')[1])
        except (ValueError, IndexError):
            page = 0

    discounts_data = get_discounts_data()
    if not discounts_data or 'discounts' not in discounts_data:
        text = get_text('error_discounts_unavailable', lang)
        if update.callback_query:
            await update.callback_query.edit_message_text(text)
        else:
            await update.message.reply_text(text)
        return

    discounts = discounts_data['discounts']

    # --- Pagination ---
    start_index = page * DISCOUNTS_PER_PAGE
    end_index = start_index + DISCOUNTS_PER_PAGE
    paginated_discounts = discounts[start_index:end_index]

    if not paginated_discounts:
        await update.callback_query.edit_message_text(get_text('error_no_more_discounts', lang))
        return

    text = get_text('discounts_title', lang)
    for item in paginated_discounts:
        name = sanitize_markdown(item.get(f'name_{lang}', item.get('name_en')))
        desc = sanitize_markdown(item.get(f'description_{lang}', item.get('description_en')))
        text += f"*{name}*\n_{desc}_\n\n"

    # --- Build Buttons ---
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton(get_text('button_previous', lang), callback_data=f"discounts_{page-1}"))
    if end_index < len(discounts):
        pagination_buttons.append(InlineKeyboardButton(get_text('button_next', lang), callback_data=f"discounts_{page+1}"))

    footer_buttons = [InlineKeyboardButton(get_text('button_back', lang), callback_data='main_menu')]

    menu = []
    if pagination_buttons:
        menu.append(pagination_buttons)
    menu.append(footer_buttons)
    reply_markup = InlineKeyboardMarkup(menu)

    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='MarkdownV2')
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode='MarkdownV2')


# Handlers to be added to main.py
discounts_command_handler = CommandHandler('discounts', show_discounts)
discounts_callback_handler = CallbackQueryHandler(show_discounts, pattern='^discounts_')
