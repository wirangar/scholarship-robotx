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
from utils.i18n import get_text
from sqlalchemy.orm import Session
from utils.database import SessionLocal
from utils.models import RoommateProfile

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

    db: Session = next(SessionLocal())
    try:
        # Check if a profile already exists
        existing_profile = db.query(RoommateProfile).filter(RoommateProfile.user_id == user.id).first()

        if existing_profile:
            # Update existing profile
            existing_profile.username = user.username or ""
            existing_profile.budget = context.user_data['roommate_budget']
            existing_profile.location = context.user_data['roommate_location']
            existing_profile.habits = context.user_data['roommate_habits']
            existing_profile.bio = context.user_data['roommate_bio']
        else:
            # Create new profile
            new_profile = RoommateProfile(
                user_id=user.id,
                username=user.username or "",
                budget=context.user_data['roommate_budget'],
                location=context.user_data['roommate_location'],
                habits=context.user_data['roommate_habits'],
                bio=context.user_data['roommate_bio'],
            )
            db.add(new_profile)

        db.commit()
        await update.message.reply_text(get_text('roommate_profile_saved', lang))

    except Exception as e:
        print(f"Failed to save roommate profile for {user.id}: {e}")
        db.rollback()
        await update.message.reply_text(get_text('roommate_error_saving', lang))
    finally:
        db.close()

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

    db: Session = next(SessionLocal())
    try:
        # 1. Check if the user has a profile
        user_profile = db.query(RoommateProfile).filter(RoommateProfile.user_id == user.id).first()
        if not user_profile:
            await query.edit_message_text(get_text('roommate_error_no_profile', lang))
            return ConversationHandler.END

        user_profile_dict = {
            'budget': user_profile.budget, 'location': user_profile.location, 'habits': user_profile.habits
        }

        # 2. Get all other profiles
        all_profiles = db.query(RoommateProfile).filter(RoommateProfile.user_id != user.id).all()

        # 3. Score and filter matches
        matches = []
        for profile in all_profiles:
            match_profile_dict = {
                'id': profile.user_id, 'username': profile.username, 'budget': profile.budget,
                'location': profile.location, 'habits': profile.habits, 'bio': profile.bio
            }
            score = calculate_match_score(user_profile_dict, match_profile_dict)
            if score > 0:
                match_profile_dict['score'] = score
                matches.append(match_profile_dict)
    finally:
        db.close()

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
