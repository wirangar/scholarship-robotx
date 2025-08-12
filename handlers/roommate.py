# -*- coding: utf-8 -*-
"""
Handler for the /roommate feature.
Allows users to create a profile and search for roommates.
"""
from telegram import Update, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from utils.gates import require_registration
from utils.gsheets import append_row, find_row_by_id, get_sheet_data, update_row
from utils.i18n import get_text

# --- Conversation States ---
MENU, CREATE_BUDGET, CREATE_LOCATION, CREATE_HABITS, CREATE_BIO, SEARCH = range(6)

@require_registration
async def start_roommate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays the main roommate menu."""
    lang = get_user_language(update.effective_user.id, context)
    buttons = [
        [InlineKeyboardButton(get_text('roommate_button_create', lang), callback_data="roommate_create_start")],
        [InlineKeyboardButton(get_text('roommate_button_search', lang), callback_data="roommate_search_start")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(get_text('roommate_welcome', lang), reply_markup=reply_markup)
    return MENU

# --- Profile Creation Flow ---

async def start_create_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the profile creation flow."""
    query = update.callback_query
    await query.answer()
    lang = get_user_language(update.effective_user.id, context)
    await query.edit_message_text(get_text('roommate_create_start', lang))
    return CREATE_BUDGET

async def ask_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves budget and asks for location."""
    lang = get_user_language(update.effective_user.id, context)
    try:
        context.user_data['roommate_budget'] = int(update.message.text)
    except ValueError:
        await update.message.reply_text(get_text('error_invalid_budget', lang))
        return CREATE_BUDGET
    await update.message.reply_text(get_text('roommate_ask_location', lang))
    return CREATE_LOCATION

async def ask_habits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves location and asks for habits."""
    lang = get_user_language(update.effective_user.id, context)
    context.user_data['roommate_location'] = update.message.text
    await update.message.reply_text(get_text('roommate_ask_habits', lang))
    return CREATE_HABITS

async def ask_bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves habits and asks for a short bio."""
    lang = get_user_language(update.effective_user.id, context)
    context.user_data['roommate_habits'] = update.message.text
    await update.message.reply_text(get_text('roommate_ask_bio', lang))
    return CREATE_BIO

async def save_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the complete profile to the 'roommates' sheet."""
    user = update.effective_user
    lang = get_user_language(update.effective_user.id, context)
    context.user_data['roommate_bio'] = update.message.text

    profile_data = [
        user.id,
        user.username or "", # Store username for contact
        context.user_data['roommate_budget'],
        context.user_data['roommate_location'],
        context.user_data['roommate_habits'],
        context.user_data['roommate_bio']
    ]

    # Check if user already has a profile to update it, otherwise create a new one.
    all_roommates = get_sheet_data('roommates')
    row_index = -1
    for i, row in enumerate(all_roommates):
        if len(row) > 0 and str(row[0]) == str(user.id):
            row_index = i + 1 # Google Sheets are 1-indexed
            break

    try:
        if row_index != -1:
            update_row('roommates', row_index, profile_data)
        else:
            append_row('roommates', profile_data)

        await update.message.reply_text(get_text('roommate_profile_saved', lang))
    except Exception as e:
        print(f"Failed to save roommate profile for {user.id}: {e}")
        await update.message.reply_text(get_text('roommate_error_saving', lang))

    # Cleanup
    for key in [k for k in context.user_data if k.startswith('roommate_')]:
        del context.user_data[key]

    return ConversationHandler.END

# --- Search Flow ---

def calculate_match_score(user_profile: dict, match_profile: dict) -> int:
    """Calculates a compatibility score between two roommate profiles."""
    score = 0

    # 1. Budget Score (Max 50 points)
    user_budget = user_profile['budget']
    match_budget = match_profile['budget']
    if abs(match_budget - user_budget) <= (user_budget * 0.1): # 10% range
        score += 50
    elif abs(match_budget - user_budget) <= (user_budget * 0.2): # 20% range
        score += 25

    # 2. Location Score (Max 30 points)
    if user_profile['location'].lower() in match_profile['location'].lower() or \
       match_profile['location'].lower() in user_profile['location'].lower():
        score += 30

    # 3. Habits Score (Max 20 points)
    if user_profile['habits'].lower() == match_profile['habits'].lower():
        score += 20

    return score

async def start_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the search flow by fetching, scoring, and displaying matches."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    lang = get_user_language(user.id, context)

    # 1. Check if the user has a profile
    user_profile_row = find_row_by_id('roommates', user.id)
    if not user_profile_row:
        await query.edit_message_text(get_text('roommate_error_no_profile', lang))
        return ConversationHandler.END

    user_profile = {
        'budget': int(user_profile_row[2]), 'location': user_profile_row[3], 'habits': user_profile_row[4]
    }

    # 2. Get all profiles
    all_profiles = get_sheet_data('roommates')

    # 3. Score and filter matches
    matches = []
    for profile in all_profiles:
        if not profile or str(profile[0]) == 'user_id' or str(profile[0]) == str(user.id):
            continue

        try:
            match_profile_dict = {
                'id': profile[0], 'username': profile[1], 'budget': int(profile[2]),
                'location': profile[3], 'habits': profile[4], 'bio': profile[5]
            }
            score = calculate_match_score(user_profile, match_profile_dict)
            if score > 0: # Only show profiles with some level of match
                match_profile_dict['score'] = score
                matches.append(match_profile_dict)
        except (ValueError, IndexError):
            continue

    # 4. Sort by score
    matches.sort(key=lambda x: x['score'], reverse=True)

    context.user_data['roommate_matches'] = matches

    if not matches:
        await query.edit_message_text(get_text('roommate_no_matches', lang))
        return ConversationHandler.END

    return await show_search_results(update, context, page=0)


async def show_search_results(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0) -> int:
    """Displays a paginated list of roommate matches."""
    query = update.callback_query
    user = update.effective_user
    lang = get_user_language(user.id, context)

    matches = context.user_data.get('roommate_matches', [])

    # --- Pagination ---
    start_index = page
    if start_index >= len(matches):
        await query.edit_message_text(get_text('roommate_no_more_matches', lang))
        return SEARCH

    match = matches[start_index]

    # Format the message
    contact = f"@{match['username']}" if match['username'] else f"User ID: {match['id']}"
    text = get_text('roommate_match_template_scored', lang).format(
        score=match['score'],
        bio=match['bio'],
        budget=match['budget'],
        location=match['location'],
        habits=match['habits'],
        contact=contact
    )

    # --- Buttons ---
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(get_text('button_previous', lang), callback_data=f"roommate_search_page_{page-1}"))
    if page < len(matches) - 1:
        buttons.append(InlineKeyboardButton(get_text('button_next', lang), callback_data=f"roommate_search_page_{page+1}"))

    reply_markup = InlineKeyboardMarkup([buttons, [InlineKeyboardButton(get_text('button_back', lang), callback_data='roommate_menu_start')]])

    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='MarkdownV2')
    return SEARCH


async def search_pagination_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the pagination for search results."""
    query = update.callback_query
    await query.answer()
    page = int(query.data.split('_')[3])
    return await show_search_results(update, context, page=page)


# --- Conversation Handler Setup ---
roommate_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('roommate', start_roommate)],
    states={
        MENU: [
            CallbackQueryHandler(start_create_profile, pattern='^roommate_create_start$'),
            CallbackQueryHandler(start_search, pattern='^roommate_search_start$'),
        ],
        SEARCH: [
            CallbackQueryHandler(search_pagination_handler, pattern='^roommate_search_page_'),
            CallbackQueryHandler(start_roommate, pattern='^roommate_menu_start$') # Go back to main menu
        ],
        CREATE_BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_location)],
        CREATE_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_habits)],
        CREATE_HABITS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_bio)],
        CREATE_BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_profile)],
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
)
