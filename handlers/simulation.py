# -*- coding: utf-8 -*-
"""
Handler for the /simulation command.
A multi-step conversation to estimate a student's monthly budget.
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
from utils.i18n import get_text
from handlers.cost import get_cost_data # Reuse the function from the cost handler

# --- Conversation States ---
CITY, HOUSING, LIFESTYLE = range(3)

@require_registration
async def start_simulation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the simulation by asking the user to select a city."""
    lang = get_user_language(update.effective_user.id, context)
    cost_data = get_cost_data()

    if not cost_data or 'cities' not in cost_data:
        await update.message.reply_text(get_text('error_cost_data_unavailable', lang))
        return ConversationHandler.END

    buttons = [
        InlineKeyboardButton(
            city.get(f'city_name_{lang}', city.get('city_name_en')),
            callback_data=f"sim_city_{city['city_id']}"
        ) for city in cost_data['cities']
    ]

    reply_markup = InlineKeyboardMarkup([buttons[i:i+2] for i in range(0, len(buttons), 2)])
    await update.message.reply_text(get_text('sim_select_city', lang), reply_markup=reply_markup)

    return CITY

async def ask_housing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the city and asks about housing preference."""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update.effective_user.id, context)
    city_id = query.data.split('_')[2]
    context.user_data['sim_city_id'] = city_id

    buttons = [
        InlineKeyboardButton(get_text('sim_housing_single', lang), callback_data="sim_housing_single"),
        InlineKeyboardButton(get_text('sim_housing_shared', lang), callback_data="sim_housing_shared"),
    ]
    reply_markup = InlineKeyboardMarkup([buttons])
    await query.edit_message_text(text=get_text('sim_ask_housing', lang), reply_markup=reply_markup)
    return HOUSING

async def ask_lifestyle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves housing choice and asks about lifestyle."""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update.effective_user.id, context)
    context.user_data['sim_housing'] = query.data.split('_')[2] # 'single' or 'shared'

    buttons = [
        InlineKeyboardButton(" frugal", callback_data="sim_life_1"),
        InlineKeyboardButton(" moderate", callback_data="sim_life_3"),
        InlineKeyboardButton(" extra", callback_data="sim_life_5"),
    ]
    reply_markup = InlineKeyboardMarkup([buttons])
    await query.edit_message_text(text=get_text('sim_ask_lifestyle', lang), reply_markup=reply_markup)
    return LIFESTYLE

async def calculate_and_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Calculates and displays the final budget simulation."""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update.effective_user.id, context)
    lifestyle_factor = int(query.data.split('_')[2]) # 1, 3, or 5

    # --- Retrieve data ---
    city_id = context.user_data['sim_city_id']
    housing_choice = context.user_data['sim_housing']
    cost_data = get_cost_data()
    city_info = next((city for city in cost_data['cities'] if city['city_id'] == city_id), None)

    if not city_info:
        await query.edit_message_text(get_text('error_city_not_found', lang))
        return ConversationHandler.END

    costs = city_info['costs']

    # --- Calculation ---
    rent = costs['rent_single_room_avg'] if housing_choice == 'single' else costs['rent_shared_room_avg']
    utilities = costs['utilities_avg']
    transport = costs['transport_pass']

    # Base groceries + lifestyle factor
    groceries = costs['groceries_monthly_avg'] + (lifestyle_factor * 20) # €20 per lifestyle point
    leisure = 20 + (lifestyle_factor * 15) # Base leisure + €15 per lifestyle point

    total = rent + utilities + transport + groceries + leisure

    text = get_text('sim_results_template', lang).format(
        rent=rent, utilities=utilities, transport=transport,
        groceries=groceries, leisure=leisure, total=total
    )

    # Cleanup
    del context.user_data['sim_city_id']
    del context.user_data['sim_housing']

    await query.edit_message_text(text, parse_mode='MarkdownV2')
    return ConversationHandler.END


# --- Conversation Handler Setup ---
simulation_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('simulation', start_simulation)],
    states={
        CITY: [CallbackQueryHandler(ask_housing, pattern='^sim_city_')],
        HOUSING: [CallbackQueryHandler(ask_lifestyle, pattern='^sim_housing_')],
        LIFESTYLE: [CallbackQueryHandler(calculate_and_finish, pattern='^sim_life_')],
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
)
