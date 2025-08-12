# -*- coding: utf-8 -*-
"""
Handler for the Resources Hub feature.
"""
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from utils.i18n import get_text
from utils.gates import require_registration, get_user_language
from utils.common import build_menu, sanitize_markdown
from utils.network import fetch_json
from config import GITHUB_DATA_URL

# --- Main Hub View ---

@require_registration
async def hub_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays the main categories of the Resources Hub.
    """
    user = update.effective_user
    lang = get_user_language(user.id, context)

    index_url = f"{GITHUB_DATA_URL}hub/index.json"
    index_data = fetch_json(index_url)

    if not index_data or 'items' not in index_data:
        # i18n key for this error
        await update.callback_query.edit_message_text(text=get_text('error_general', lang))
        return

    # Group items by category
    categories = {}
    for item in index_data['items']:
        cat = item.get('category', 'other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    buttons = [
        InlineKeyboardButton(
            text=f"📂 {category.capitalize()}", # Simple text for now
            callback_data=f"hub_cat_{category}"
        ) for category in categories.keys()
    ]

    # Add a back button to the main bot menu
    footer_buttons = [
        InlineKeyboardButton(get_text('button_back', lang), callback_data='main_menu')
    ]
    reply_markup = build_menu(buttons, n_cols=2, footer_buttons=footer_buttons)

    text = "📚 *Resources Hub*\n\nPlease select a category:"

    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='MarkdownV2')
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode='MarkdownV2')


# --- Handler for callback queries ---

async def hub_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    lang = get_user_language(user.id, context)

    # command is like "hub_cat_living" or "hub_topic_residency_page_0"
    command_parts = query.data.split('_')

    if command_parts[1] == 'cat':
        # --- Category View ---
        category_id = command_parts[2]
        await display_category_topics(update, context, category_id, lang)
    elif command_parts[1] == 'topic':
        # --- Topic View ---
        topic_id = command_parts[2]
        page = int(command_parts[4]) if len(command_parts) > 4 else 0
        await display_topic_content(update, context, topic_id, lang, page)


async def display_category_topics(update: Update, context: ContextTypes.DEFAULT_TYPE, category_id: str, lang: str):
    index_url = f"{GITHUB_DATA_URL}hub/index.json"
    index_data = fetch_json(index_url)

    if not index_data:
        await update.callback_query.edit_message_text(text=get_text('error_general', lang))
        return

    items_in_category = [item for item in index_data.get('items', []) if item.get('category') == category_id]

    buttons = [
        InlineKeyboardButton(
            text=item.get(f'title_{lang}', item.get('title_en')),
            callback_data=f"hub_topic_{item['id']}_page_0"
        ) for item in items_in_category
    ]

    footer_buttons = [InlineKeyboardButton(get_text('button_back', lang), callback_data='hub_main')]
    reply_markup = build_menu(buttons, n_cols=1, footer_buttons=footer_buttons)
    text = f"*{category_id.capitalize()}* Topics"
    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='MarkdownV2')


async def display_topic_content(update: Update, context: ContextTypes.DEFAULT_TYPE, topic_id: str, lang: str, page: int = 0):
    topic_url = f"{GITHUB_DATA_URL}hub/{topic_id}.json"
    topic_data = fetch_json(topic_url)

    if not topic_data or 'sections' not in topic_data:
        await update.callback_query.edit_message_text(text=get_text('error_general', lang))
        return

    sections = topic_data['sections']

    # --- Pagination Logic ---
    section = sections[page]

    title = sanitize_markdown(section.get(f'title_{lang}', section.get('title_en', '')))
    content = sanitize_markdown(section.get(f'content_{lang}', section.get('content_en', '')))

    text = f"*{title}*\n\n{content}"

    # Add links if they exist
    if 'links' in section and section['links']:
        links_text = "\n\n*Useful Links:*"
        for link in section['links']:
            link_title = sanitize_markdown(link.get(f'text_{lang}', link.get('text_en', 'Link')))
            links_text += f"\n- [{link_title}]({link['url']})"
        text += links_text

    # --- Build Pagination Buttons ---
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"hub_topic_{topic_id}_page_{page-1}"))
    if page < len(sections) - 1:
        pagination_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"hub_topic_{topic_id}_page_{page+1}"))

    # Find the category of the current topic to build the "back" button
    index_url = f"{GITHUB_DATA_URL}hub/index.json"
    index_data = fetch_json(index_url)
    topic_info = next((item for item in index_data['items'] if item['id'] == topic_id), None)
    back_callback = f"hub_cat_{topic_info['category']}" if topic_info else "hub_main"

    footer_buttons = [InlineKeyboardButton(get_text('button_back', lang), callback_data=back_callback)]

    # Combine buttons
    menu = []
    if pagination_buttons:
        menu.append(pagination_buttons)
    menu.append(footer_buttons)
    reply_markup = InlineKeyboardMarkup(menu)

    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='MarkdownV2', disable_web_page_preview=True)

# --- Handlers to be added to main.py ---
# CommandHandler('hub', hub_main_menu)
# CallbackQueryHandler(hub_main_menu, pattern='^hub_main$')
# CallbackQueryHandler(hub_callback_handler, pattern='^hub_')
