# -*- coding: utf-8 -*-
"""
Handler for the /cost command.
Displays cost of living information for different cities.
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
from utils.common import sanitize_markdown
from utils.i18n import get_text

# --- Conversation States ---
CITY_SELECTION = 0
DATA_FILE_PATH = "data/cost_of_living.json"

def get_cost_data() -> dict:
    """Loads the cost of living data from the JSON file."""
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

@require_registration
async def start_cost(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation by asking the user to select a city."""
    lang = get_user_language(update.effective_user.id, context)
    cost_data = get_cost_data()

    if not cost_data or 'cities' not in cost_data:
        await update.message.reply_text(get_text('error_cost_data_unavailable', lang))
        return ConversationHandler.END

    buttons = [
        InlineKeyboardButton(
            city.get(f'city_name_{lang}', city.get('city_name_en')),
            callback_data=f"cost_city_{city['city_id']}"
        ) for city in cost_data['cities']
    ]

    reply_markup = InlineKeyboardMarkup([buttons[i:i+2] for i in range(0, len(buttons), 2)])
    await update.message.reply_text(get_text('cost_select_city', lang), reply_markup=reply_markup)

    return CITY_SELECTION

async def show_cost(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays the cost of living for the selected city."""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update.effective_user.id, context)
    city_id = query.data.split('_')[2]

    cost_data = get_cost_data()
    city_info = next((city for city in cost_data['cities'] if city['city_id'] == city_id), None)

    if not city_info:
        await query.edit_message_text(get_text('error_city_not_found', lang))
        return ConversationHandler.END

    costs = city_info['costs']
    city_name = sanitize_markdown(city_info.get(f'city_name_{lang}', city_info.get('city_name_en')))

    text = get_text('cost_details_template', lang).format(
        city_name=city_name,
        rent_single=costs['rent_single_room_avg'],
        rent_shared=costs['rent_shared_room_avg'],
        utilities=costs['utilities_avg'],
        transport=costs['transport_pass'],
        groceries=costs['groceries_monthly_avg'],
        pizza=costs['eating_out_pizza'],
        notes=sanitize_markdown(city_info.get(f'notes_{lang}', city_info.get('notes_en')))
    )

    # Back button
    back_button = InlineKeyboardButton(get_text('button_back_to_cities', lang), callback_data="cost_start")
    reply_markup = InlineKeyboardMarkup([[back_button]])

    await query.edit_message_text(text, parse_mode='MarkdownV2', reply_markup=reply_markup)
    return CITY_SELECTION # Stay in the same state to allow going back

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the 'back' button by restarting the conversation."""
    # This effectively re-runs the start_cost function on the message
    query = update.callback_query
    await query.answer()
    # To properly restart, we call the start function logic again
    # but on the existing message
    lang = get_user_language(update.effective_user.id, context)
    cost_data = get_cost_data()
    buttons = [
        InlineKeyboardButton(
            city.get(f'city_name_{lang}', city.get('city_name_en')),
            callback_data=f"cost_city_{city['city_id']}"
        ) for city in cost_data['cities']
    ]
    reply_markup = InlineKeyboardMarkup([buttons[i:i+2] for i in range(0, len(buttons), 2)])
    await query.edit_message_text("Please select a city:", reply_markup=reply_markup)
    return CITY_SELECTION

# --- Conversation Handler Setup ---
cost_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('cost', start_cost)],
    states={
        CITY_SELECTION: [
            CallbackQueryHandler(show_cost, pattern='^cost_city_'),
            CallbackQueryHandler(back_to_start, pattern='^cost_start$'),
        ],
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
)
