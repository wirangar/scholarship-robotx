# -*- coding: utf-8 -*-
"""
Decorators for access control and state checking (gates).
"""
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

from utils.gsheets import find_row_by_id
from utils.i18n import get_text

# In-memory cache for user registration status to reduce GSheet lookups
# For a multi-worker setup, a Redis cache would be better.
_user_registration_cache = {}

def get_user_language(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Retrieves the user's preferred language.
    Placeholder logic: should be fetched from user profile in GSheets or context.
    """
    # For now, we can store it in bot_data or user_data after registration
    return context.user_data.get('language', 'fa')

def require_registration(func):
    """
    A decorator that checks if a user is registered before allowing access to a command.
    It checks for the user's Telegram ID in the 'users' sheet.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        if not user:
            return

        # 1. Check local cache first
        if user.id in _user_registration_cache and _user_registration_cache[user.id]:
            return await func(update, context, *args, **kwargs)

        # 2. If not in cache, check Google Sheets
        user_profile = find_row_by_id('users', user.id, id_column_index=0)

        if user_profile:
            # Cache the positive result
            _user_registration_cache[user.id] = True
            # Store language preference from profile
            # Assuming language is in column 6 (index 5) of the 'users' sheet
            if len(user_profile) > 5:
                context.user_data['language'] = user_profile[5]
            return await func(update, context, *args, **kwargs)
        else:
            # User is not registered
            lang = get_user_language(user.id, context)
            await update.message.reply_text(get_text('register_prompt', lang))
            return

    return wrapper

def require_admin(role: str = 'admin'):
    """
    A decorator to restrict access to admin-only commands.
    Checks for user's role in the 'admins' sheet.

    Args:
        role: The minimum role required (e.g., 'news_admin', 'superadmin').
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        if not user:
            return

        # In a real implementation, this would check the 'admins' GSheet
        # admin_record = find_row_by_id('admins', user.id)
        # if admin_record and has_permission(admin_record.role, required_role=role):
        #     return await func(update, context, *args, **kwargs)

        # Placeholder logic: only allow if user is the global ADMIN_CHAT_ID
        from config import ADMIN_CHAT_ID
        if str(user.id) == str(ADMIN_CHAT_ID):
             return await func(update, context, *args, **kwargs)
        else:
            lang = get_user_language(user.id, context)
            await update.message.reply_text(get_text('error_general', lang)) # Generic error
            return

    return wrapper
