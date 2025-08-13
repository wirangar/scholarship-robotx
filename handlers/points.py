# -*- coding: utf-8 -*-
"""
Handler for the /points command.
Displays the user's points (placeholder).
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from utils.gates import require_registration, get_user_language
from utils.i18n import get_text

@require_registration
async def show_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays a placeholder message for user points."""
    lang = get_user_language(update.effective_user.id, context)

    # In a real implementation, this would fetch points from a 'users' or 'points' sheet.
    user_points = 100 # Placeholder value

    text = get_text('points_display', lang).format(points=user_points)
    await update.message.reply_text(text)
