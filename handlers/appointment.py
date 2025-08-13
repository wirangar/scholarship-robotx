# -*- coding: utf-8 -*-
"""
Handler for the /appointment command.
Allows users to book an appointment by fetching slots from Google Calendar.
"""
import datetime
from telegram import Update, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
)
from dateutil import parser

from utils.gates import require_registration, get_user_language
from utils.gsheets import append_row
from utils.i18n import get_text
from utils.gcalendar import get_free_slots, book_appointment_slot
from utils import redis_utils

# --- Conversation States ---
TIMESLOT, CONFIRMATION = range(2)

@require_registration
async def start_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the appointment booking by fetching available slots from GCal."""
    lang = get_user_language(update.effective_user.id, context)

    slots = get_free_slots()

    if not slots:
        await update.message.reply_text(get_text('error_appointments_unavailable', lang))
        return ConversationHandler.END

    # Store slots in context to avoid re-fetching
    context.user_data['appt_available_slots'] = slots

    buttons = []
    for slot in slots:
        # Format the datetime string into something more readable
        start_time = parser.isoparse(slot['start'])
        formatted_time = start_time.strftime('%A, %b %d @ %H:%M') # e.g., Monday, May 27 @ 10:00
        buttons.append(InlineKeyboardButton(formatted_time, callback_data=f"appt_slotid_{slot['id']}"))

    reply_markup = InlineKeyboardMarkup([buttons[i:i+1] for i in range(0, len(buttons))])
    await update.message.reply_text(get_text('appt_select_slot', lang), reply_markup=reply_markup)

    return TIMESLOT

async def confirm_booking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks the user to confirm their selected time slot."""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update.effective_user.id, context)
    event_id = query.data.split('_')[2]

    # Find the selected slot from the list stored in context
    selected_slot = next((s for s in context.user_data['appt_available_slots'] if s['id'] == event_id), None)
    if not selected_slot:
        await query.edit_message_text(get_text('error_general', lang))
        return ConversationHandler.END

    context.user_data['appt_event_id'] = event_id
    start_time = parser.isoparse(selected_slot['start']).strftime('%A, %b %d @ %H:%M')
    context.user_data['appt_slot_str'] = start_time

    buttons = [
        InlineKeyboardButton(get_text('button_confirm', lang), callback_data="appt_book_confirm"),
        InlineKeyboardButton(get_text('button_cancel', lang), callback_data="appt_book_cancel"),
    ]
    reply_markup = InlineKeyboardMarkup([buttons])
    await query.edit_message_text(text=get_text('appt_confirm_booking', lang).format(slot=start_time), reply_markup=reply_markup)
    return CONFIRMATION

async def save_booking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Books the slot on GCal and saves the booking to Google Sheets."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    lang = get_user_language(user.id, context)

    event_id = context.user_data['appt_event_id']
    slot_str = context.user_data['appt_slot_str']

    # Book the slot by updating the GCal event
    booked_event = book_appointment_slot(event_id, user.full_name, user.id)

    if not booked_event:
        await query.edit_message_text(get_text('error_appointments_unavailable', lang))
        return ConversationHandler.END

    # Schedule a reminder 24 hours before the appointment
    try:
        appointment_time_utc = parser.isoparse(booked_event['start']['dateTime'])
        reminder_time_utc = appointment_time_utc - datetime.timedelta(hours=24)
        reminder_timestamp = int(reminder_time_utc.timestamp())

        # Ensure we don't schedule reminders for past events
        if reminder_time_utc > datetime.datetime.now(datetime.timezone.utc):
            reminder_task = {
                "user_id": user.id,
                "message": get_text('appt_reminder_24h', lang).format(slot=slot_str)
            }
            redis_utils.schedule_task(reminder_timestamp, reminder_task)
    except Exception as e:
        print(f"Failed to schedule reminder for user {user.id}: {e}") # Log and continue

    # Log to Google Sheets
    try:
        booking_data = [
            datetime.datetime.utcnow().isoformat(),
            user.id,
            user.full_name,
            "General Advising", # Service is now generic since we fetch from one calendar
            slot_str,
            'booked',
            booked_event.get('htmlLink', '') # Link to the GCal event
        ]
        append_row('appointments', booking_data)
        await query.edit_message_text(get_text('appt_success', lang))
    except Exception as e:
        print(f"Failed to save appointment for user {user.id}: {e}")
        # TODO: Add logic to "un-book" the GCal event if sheet logging fails
        await query.edit_message_text(get_text('error_general', lang))

    # Cleanup
    for key in [k for k in context.user_data if k.startswith('appt_')]:
        del context.user_data[key]

    return ConversationHandler.END

async def cancel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the booking process."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(get_text('appt_canceled', lang))
    # Cleanup
    for key in [k for k in context.user_data if k.startswith('appt_')]:
        del context.user_data[key]
    return ConversationHandler.END

# --- Conversation Handler Setup ---
appointment_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('appointment', start_appointment)],
    states={
        TIMESLOT: [CallbackQueryHandler(confirm_booking, pattern='^appt_slotid_')],
        CONFIRMATION: [
            CallbackQueryHandler(save_booking, pattern='^appt_book_confirm$'),
            CallbackQueryHandler(cancel_booking, pattern='^appt_book_cancel$')
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel_booking)],
)
