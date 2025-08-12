# -*- coding: utf-8 -*-
"""
Handler for the /weather command.
"""
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
from utils.weather_api import get_weather
from utils.i18n import get_text

# --- Conversation States ---
CITY_INPUT = 0

@require_registration
async def start_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks the user for a city, offering Perugia as a default."""
    lang = context.user_data.get('language', 'fa')
    text = get_text('weather_prompt', lang)
    buttons = [
        InlineKeyboardButton(get_text('weather_button_perugia', lang), callback_data="weather_city_Perugia")
    ]
    reply_markup = InlineKeyboardMarkup([buttons])

    await update.message.reply_text(text, reply_markup=reply_markup)
    return CITY_INPUT

async def show_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Fetches and displays the weather for the chosen city."""
    lang = context.user_data.get('language', 'fa')
    city = ""
    if update.callback_query:
        await update.callback_query.answer()
        city = update.callback_query.data.split('_')[2]
        # Use the original message to edit, avoids "message not modified" error
        message = update.callback_query.message
    else:
        city = update.message.text
        message = update.message

    if not city:
        await message.reply_text(get_text('error_invalid_city', lang))
        return CITY_INPUT

    weather_data = get_weather(city)

    if not weather_data:
        await message.edit_text(get_text('error_weather_unavailable', lang))
        return ConversationHandler.END

    if weather_data.get("error") == "city_not_found":
        await message.reply_text(get_text('error_weather_city_not_found', lang).format(city=city))
        return CITY_INPUT

    # Format the message
    text = get_text('weather_details_template', lang).format(
        emoji=weather_data['emoji'],
        city=weather_data['city'],
        description=weather_data['description'],
        temp=weather_data['temp'],
        feels_like=weather_data['feels_like'],
        humidity=weather_data['humidity'],
        wind_speed=weather_data['wind_speed']
    )

    # We edit the message if it came from a callback, otherwise reply
    if update.callback_query:
        await message.edit_text(text, parse_mode='MarkdownV2')
    else:
        await message.reply_text(text, parse_mode='MarkdownV2')

    return ConversationHandler.END

async def cancel_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the weather conversation."""
    await update.message.reply_text("Weather check canceled.")
    return ConversationHandler.END

# --- Conversation Handler Setup ---
weather_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('weather', start_weather)],
    states={
        CITY_INPUT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, show_weather),
            CallbackQueryHandler(show_weather, pattern='^weather_city_')
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel_weather)],
)
