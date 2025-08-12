# -*- coding: utf-8 -*-
"""
Handler for the /news feature.
Fetches and displays news from an RSS feed.
"""
import feedparser
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from utils.i18n import get_text
from utils.gates import require_registration, get_user_language
from utils.common import build_menu, sanitize_markdown
from utils.redis_utils import get_cache, set_cache
from config import NEWS_RSS_URL, CACHE_TTL_SECONDS

NEWS_CACHE_KEY = "news_feed_cache"
ARTICLES_PER_PAGE = 5

def fetch_news_feed():
    """
    Fetches the news feed from the RSS URL, using a cache.
    """
    # 1. Check cache first
    cached_feed = get_cache(NEWS_CACHE_KEY)
    if cached_feed:
        return cached_feed

    # 2. If not in cache, fetch from source
    try:
        feed = feedparser.parse(NEWS_RSS_URL)
        if feed.bozo: # bozo is 1 if the feed is malformed
            raise ValueError(f"Malformed RSS feed: {feed.bozo_exception}")

        # We only need a subset of data, so we extract it to keep the cache light
        articles = [
            {
                'title': entry.get('title', 'No Title'),
                'link': entry.get('link', 'No Link'),
                'summary': entry.get('summary', 'No Summary'),
                'published': entry.get('published', 'No Date'),
            }
            for entry in feed.entries
        ]

        set_cache(NEWS_CACHE_KEY, articles, ttl=CACHE_TTL_SECONDS)
        return articles
    except Exception as e:
        # In a real app, you might want a logger here
        print(f"Error fetching or parsing RSS feed: {e}")
        return None

@require_registration
async def news_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Displays the first page of news articles.
    """
    user = update.effective_user
    lang = get_user_language(user.id, context)

    page = 0
    if update.callback_query:
        # Extract page number from callback data, e.g., "news_page_1"
        try:
            page = int(update.callback_query.data.split('_')[2])
        except (ValueError, IndexError):
            page = 0

    articles = fetch_news_feed()

    if not articles:
        text = "Sorry, the news service is currently unavailable." # i18n
        await update.message.reply_text(text)
        return

    # --- Pagination ---
    start_index = page * ARTICLES_PER_PAGE
    end_index = start_index + ARTICLES_PER_PAGE
    paginated_articles = articles[start_index:end_index]

    if not paginated_articles:
        text = "No more news articles found." # i18n
        # Logic to handle this case, maybe just edit the message
        await update.callback_query.edit_message_text(text)
        return

    text = "📰 *Latest News*\n\n"
    for article in paginated_articles:
        title = sanitize_markdown(article['title'])
        link = article['link']
        text += f"▪️ [{title}]({link})\n"

    # --- Build Buttons ---
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"news_page_{page-1}"))
    if end_index < len(articles):
        pagination_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"news_page_{page+1}"))

    footer_buttons = [InlineKeyboardButton(get_text('button_back', lang), callback_data='main_menu')]

    menu = []
    if pagination_buttons:
        menu.append(pagination_buttons)
    menu.append(footer_buttons)
    reply_markup = InlineKeyboardMarkup(menu)

    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='MarkdownV2', disable_web_page_preview=True)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode='MarkdownV2', disable_web_page_preview=True)

# --- Handlers to be added to main.py ---
# CommandHandler('news', news_menu)
# CallbackQueryHandler(news_menu, pattern='^news_page_')
