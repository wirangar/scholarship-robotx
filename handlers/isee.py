# -*- coding: utf-8 -*-
"""
Handler for the ISEE calculator (/isee).
Uses a ConversationHandler to guide the user through the calculation.
"""
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from utils.i18n import get_text
from utils.logger import get_logger
from utils.gates import require_registration, get_user_language
from utils.common import get_family_coeff
from config import ISEE_THRESHOLD, ISEE_PROPERTY_COEFF

logger = get_logger(__name__)

# --- Conversation States ---
INCOME, PROPERTY, FAMILY = range(3)

def calc_isee(income: float, property_size: float, family_n: int) -> float:
    """
    Calculates the estimated ISEE value.
    Formula: ISEE = (Income + (Property Value * 0.2)) / Family Coefficient
    Property Value is estimated as size * 500.
    """
    estate_value = property_size * ISEE_PROPERTY_COEFF
    numerator = income + (estate_value * 0.2)
    denominator = get_family_coeff(family_n)
    return numerator / denominator

@require_registration
async def start_isee_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the ISEE calculation conversation."""
    user = update.effective_user
    lang = get_user_language(user.id, context)

    text = get_text('isee_intro', lang) + "\n\n" + get_text('isee_ask_income', lang)

    if update.callback_query:
        await update.callback_query.edit_message_text(text)
    else:
        await update.message.reply_text(text)

    return INCOME

async def ask_property(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves income and asks for property size."""
    user = update.effective_user
    lang = get_user_language(user.id, context)

    try:
        income = float(update.message.text)
        context.user_data['isee_income'] = income
        await update.message.reply_text(get_text('isee_ask_property', lang))
        return PROPERTY
    except ValueError:
        await update.message.reply_text(get_text('invalid_input', lang) + " " + get_text('isee_ask_income', lang))
        return INCOME

async def ask_family(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves property size and asks for family member count."""
    user = update.effective_user
    lang = get_user_language(user.id, context)

    try:
        property_size = float(update.message.text)
        context.user_data['isee_property'] = property_size
        await update.message.reply_text(get_text('isee_ask_family', lang))
        return FAMILY
    except ValueError:
        await update.message.reply_text(get_text('invalid_input', lang) + " " + get_text('isee_ask_property', lang))
        return PROPERTY

async def calculate_and_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Calculates and shows the final ISEE result."""
    user = update.effective_user
    lang = get_user_language(user.id, context)

    try:
        family_n = int(update.message.text)
        if family_n <= 0:
            raise ValueError("Family number must be positive.")

        income = context.user_data['isee_income']
        property_size = context.user_data['isee_property']

        isee_value = calc_isee(income, property_size, family_n)

        # Determine scholarship status
        if isee_value <= ISEE_THRESHOLD:
            status = get_text('isee_status_full', lang)
        elif isee_value <= ISEE_THRESHOLD * 1.5: # Example for partial
             status = get_text('isee_status_partial', lang)
        else:
            status = get_text('isee_status_none', lang)

        result_text = get_text('isee_result', lang).format(isee_value=isee_value, status=status)
        await update.message.reply_text(result_text, reply_markup=ReplyKeyboardRemove())

        # TODO: Save calculation to 'isee_calcs' sheet with user consent.

        # Clean up context
        for key in [k for k in context.user_data if k.startswith('isee_')]:
            del context.user_data[key]

        return ConversationHandler.END

    except (ValueError, TypeError):
        await update.message.reply_text(get_text('invalid_input', lang) + " " + get_text('isee_ask_family', lang))
        return FAMILY
    except Exception as e:
        logger.error(f"Error in ISEE calculation for user {user.id}: {e}")
        await update.message.reply_text(get_text('error_general', lang), reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text("ISEE calculation canceled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# --- Conversation Handler Setup ---
isee_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler('isee', start_isee_conversation),
        CallbackQueryHandler(start_isee_conversation, pattern='^isee_start$')
    ],
    states={
        INCOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_property)],
        PROPERTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_family)],
        FAMILY: [MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_and_finish)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    per_user=True,
    per_chat=True,
)
