# -*- coding: utf-8 -*-
"""
Handler for the /search feature.
Provides a global search across the Resources Hub and News.
"""
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from utils.i18n import get_text
from utils.gates import require_registration, get_user_language
from utils.common import sanitize_markdown
from handlers.resources_hub import fetch_json, GITHUB_DATA_URL
from handlers.news import fetch_news_feed

# --- Conversation States ---
QUERY = 0

@require_registration
async def start_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the search conversation by asking for a query."""
    user = update.effective_user
    lang = get_user_language(user.id, context)
    # i18n
    await update.message.reply_text("What would you like to search for?")
    return QUERY

async def perform_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Performs the search and returns the results."""
    user = update.effective_user
    lang = get_user_language(user.id, context)
    query = update.message.text.lower()

    if not query or len(query) < 3:
        # i18n
        await update.message.reply_text("Please enter a search query of at least 3 characters.")
        return QUERY

    # --- Search in Resources Hub ---
    hub_results = []
    index_data = fetch_json(f"{GITHUB_DATA_URL}hub/index.json")
    if index_data:
        for item in index_data.get('items', []):
            # Search in title, tags
            if query in item.get(f'title_{lang}', '').lower() or \
               query in item.get('title_en', '').lower() or \
               any(query in tag.lower() for tag in item.get('tags', [])):
                hub_results.append(item)

    # --- Search in News ---
    news_results = []
    articles = fetch_news_feed()
    if articles:
        for article in articles:
            if query in article.get('title', '').lower() or \
               query in article.get('summary', '').lower():
                news_results.append(article)

    # --- Format Results ---
    if not hub_results and not news_results:
        # i18n
        await update.message.reply_text("No results found.")
        return ConversationHandler.END

    text = f"🔎 *Search Results for '{sanitize_markdown(query)}'*\n\n"

    if hub_results:
        text += "*Resources Hub:*\n"
        for item in hub_results[:5]: # Limit results
            title = sanitize_markdown(item.get(f'title_{lang}', item.get('title_en')))
            # The callback data allows users to directly jump to the topic
            text += f"▪️ {title} (use /hub to find it)\n" # Simple text for now

    if news_results:
        text += "\n*News:*\n"
        for article in news_results[:5]: # Limit results
            title = sanitize_markdown(article['title'])
            link = article['link']
            text += f"▪️ [{title}]({link})\n"

    await update.message.reply_text(text, parse_mode='MarkdownV2', disable_web_page_preview=True)

    return ConversationHandler.END


async def cancel_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the search conversation."""
    await update.message.reply_text("Search canceled.")
    return ConversationHandler.END

# --- Conversation Handler Setup ---
search_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('search', start_search)],
    states={
        QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, perform_search)],
    },
    fallbacks=[CommandHandler('cancel', cancel_search)],
)
