# -*- coding: utf-8 -*-
"""
Google Calendar utility functions.
Handles fetching available slots and booking appointments.
"""
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.gsheets import creds # Re-use credentials
from config import GOOGLE_CALENDAR_ID
from utils.logger import get_logger

logger = get_logger(__name__)

# --- Service Setup ---
service = None
if creds and GOOGLE_CALENDAR_ID:
    try:
        service = build('calendar', 'v3', credentials=creds)
        logger.info("Successfully connected to Google Calendar API.")
    except Exception as e:
        logger.error(f"Failed to build Google Calendar service: {e}")

def get_free_slots() -> list[dict]:
    """
    Fetches available appointment slots from the Google Calendar.

    This is a simplified implementation that looks for events in the next 7 days
    with the summary "Available Slot".

    Returns:
        A list of dictionaries, each with 'summary', 'start', 'end', and 'id'.
    """
    if not service:
        logger.warning("Google Calendar service not available. Cannot fetch slots.")
        return []

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC
    time_max = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'

    try:
        events_result = service.events().list(
            calendarId=GOOGLE_CALENDAR_ID,
            timeMin=now,
            timeMax=time_max,
            q="Available Slot", # Search for events with this summary
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        slots = [
            {
                "summary": event['summary'],
                "start": event['start'].get('dateTime', event['start'].get('date')),
                "end": event['end'].get('dateTime', event['end'].get('date')),
                "id": event['id']
            } for event in events
        ]
        return slots

    except HttpError as err:
        logger.error(f"An error occurred fetching calendar events: {err}")
        return []

def book_appointment_slot(event_id: str, user_name: str, user_id: int) -> dict | None:
    """
    Books an appointment by updating an existing "Available Slot" event.
    It changes the summary to "Booked by [User]" and adds the user as an attendee.
    """
    if not service:
        return None

    try:
        # First, get the existing event to preserve its times
        event = service.events().get(calendarId=GOOGLE_CALENDAR_ID, eventId=event_id).execute()

        # Update the event summary and add attendee
        event['summary'] = f"Booked by {user_name} (User ID: {user_id})"
        # A real implementation might add the user's email if collected
        # event['attendees'] = [{'email': user_email}]

        updated_event = service.events().update(
            calendarId=GOOGLE_CALENDAR_ID,
            eventId=event['id'],
            body=event
        ).execute()

        return updated_event

    except HttpError as err:
        logger.error(f"An error occurred booking the appointment: {err}")
        return None
