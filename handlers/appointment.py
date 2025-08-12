# -*- coding: utf-8 -*-
"""
Handler for the /appointment command.
Allows users to book an appointment for various services.
"""
import json
import datetime
from telegram import Update, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
)

from utils.gates import require_registration
from utils.gsheets import append_row
from utils.i18n import get_text

# --- Conversation States ---
SERVICE, TIMESLOT, CONFIRMATION = range(3)
DATA_FILE_PATH = "data/appointments.json"

def get_appointment_data() -> dict:
    """Loads the appointment data from the JSON file."""
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

@require_registration
async def start_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the appointment booking process by showing available services."""
    lang = get_user_language(update.effective_user.id, context)
    appointment_data = get_appointment_data()

    if not appointment_data or 'services' not in appointment_data:
        await update.message.reply_text(get_text('error_appointments_unavailable', lang))
        return ConversationHandler.END

    buttons = [
        InlineKeyboardButton(
            srv.get(f'name_{lang}', srv.get('name_en')),
            callback_data=f"appt_service_{srv['id']}"
        ) for srv in appointment_data['services']
    ]

    reply_markup = InlineKeyboardMarkup([buttons[i:i+1] for i in range(0, len(buttons))])
    await update.message.reply_text(get_text('appt_select_service', lang), reply_markup=reply_markup)

    return SERVICE

async def select_timeslot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Shows available time slots for the selected service."""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update.effective_user.id, context)
    service_id = query.data.split('_')[2]
    context.user_data['appt_service_id'] = service_id

    appointment_data = get_appointment_data()
    service_info = next((srv for srv in appointment_data['services'] if srv['id'] == service_id), None)

    if not service_info or 'slots' not in service_info:
        await query.edit_message_text(get_text('error_appointments_unavailable', lang))
        return ConversationHandler.END

    buttons = [
        InlineKeyboardButton(slot, callback_data=f"appt_slot_{slot}") for slot in service_info['slots']
    ]
    # Add a back button
    buttons.append(InlineKeyboardButton(get_text('button_back', lang), callback_data="appt_start"))

    reply_markup = InlineKeyboardMarkup([buttons[i:i+1] for i in range(0, len(buttons))])
    await query.edit_message_text(text=get_text('appt_select_slot', lang), reply_markup=reply_markup)
    return TIMESLOT

async def confirm_booking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks the user to confirm their selected time slot."""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update.effective_user.id, context)
    slot = ' '.join(query.data.split('_')[2:])
    context.user_data['appt_slot'] = slot

    buttons = [
        InlineKeyboardButton(get_text('button_confirm', lang), callback_data="appt_book_confirm"),
        InlineKeyboardButton(get_text('button_cancel', lang), callback_data="appt_book_cancel"),
    ]
    reply_markup = InlineKeyboardMarkup([buttons])
    await query.edit_message_text(text=get_text('appt_confirm_booking', lang).format(slot=slot), reply_markup=reply_markup)
    return CONFIRMATION

async def save_booking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the confirmed booking to Google Sheets."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    lang = get_user_language(user.id, context)

    service_id = context.user_data['appt_service_id']
    slot = context.user_data['appt_slot']

    appointment_data = get_appointment_data()
    service_info = next((srv for srv in appointment_data['services'] if srv['id'] == service_id), None)
    service_name = service_info.get(f'name_{lang}', service_info.get('name_en', service_id))

    try:
        booking_data = [
            datetime.datetime.utcnow().isoformat(),
            user.id,
            user.full_name,
            service_name,
            slot,
            'booked'
        ]
        append_row('appointments', booking_data)
        await query.edit_message_text(get_text('appt_success', lang))
    except Exception as e:
        print(f"Failed to save appointment for user {user.id}: {e}")
        await query.edit_message_text(get_text('error_general', lang))

    # Cleanup
    del context.user_data['appt_service_id']
    del context.user_data['appt_slot']

    return ConversationHandler.END

async def cancel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the booking process."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(get_text('appt_canceled', lang))
    # Cleanup
    if 'appt_service_id' in context.user_data: del context.user_data['appt_service_id']
    if 'appt_slot' in context.user_data: del context.user_data['appt_slot']
    return ConversationHandler.END


# --- Conversation Handler Setup ---
appointment_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('appointment', start_appointment)],
    states={
        SERVICE: [CallbackQueryHandler(select_timeslot, pattern='^appt_service_')],
        TIMESLOT: [
            CallbackQueryHandler(confirm_booking, pattern='^appt_slot_'),
            CallbackQueryHandler(start_appointment, pattern='^appt_start$'), # Back button
        ],
        CONFIRMATION: [
            CallbackQueryHandler(save_booking, pattern='^appt_book_confirm$'),
            CallbackQueryHandler(cancel_booking, pattern='^appt_book_cancel$')
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel_booking)],
)
