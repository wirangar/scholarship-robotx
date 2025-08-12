# -*- coding: utf-8 -*-
"""
Google Sheets utility functions.
Acts as a simple database for structured data.
"""
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import GOOGLE_CREDS, SHEET_ID, SPREADSHEET_NAME
from utils.logger import get_logger

logger = get_logger(__name__)

# --- Authentication and Service Setup ---

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
if GOOGLE_CREDS:
    try:
        creds = service_account.Credentials.from_service_account_info(
            GOOGLE_CREDS, scopes=SCOPES
        )
    except Exception as e:
        logger.error(f"Failed to load Google credentials: {e}")

service = None
if creds:
    try:
        service = build('sheets', 'v4', credentials=creds)
    except Exception as e:
        logger.error(f"Failed to build Google Sheets service: {e}")

# --- Helper Functions ---

def _get_spreadsheet():
    """Helper to get the sheet service."""
    if not service:
        logger.error("Google Sheets service is not available.")
        return None
    return service.spreadsheets()

def get_sheet_data(sheet_name: str, range_name: str = 'A:Z') -> list[list[str]]:
    """
    Reads data from a specific sheet (tab) within the spreadsheet.
    Returns a list of lists representing the rows.
    """
    sheet_service = _get_spreadsheet()
    if not sheet_service:
        return []

    try:
        full_range = f"{sheet_name}!{range_name}"
        result = sheet_service.values().get(spreadsheetId=SHEET_ID, range=full_range).execute()
        values = result.get('values', [])
        return values
    except HttpError as err:
        logger.error(f"Error reading from sheet '{sheet_name}': {err}")
        # Handle specific errors like sheet not found if necessary
        if err.resp.status == 400:
             logger.error(f"Possible issue: Sheet '{sheet_name}' may not exist in spreadsheet '{SPREADSHEET_NAME}'.")
        return []

def append_row(sheet_name: str, row_data: list):
    """
    Appends a new row of data to the end of a specific sheet.
    `row_data` should be a list of values.
    """
    sheet_service = _get_spreadsheet()
    if not sheet_service:
        return None

    try:
        body = {
            'values': [row_data]
        }
        result = sheet_service.values().append(
            spreadsheetId=SHEET_ID,
            range=f"{sheet_name}!A1",
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        logger.info(f"Appended {result.get('updates').get('updatedCells')} cells to sheet '{sheet_name}'.")
        return result
    except HttpError as err:
        logger.error(f"Error appending to sheet '{sheet_name}': {err}")
        return None

def find_row_by_id(sheet_name: str, item_id, id_column_index: int = 0) -> list | None:
    """
    Finds a row in a sheet by a unique ID in a specified column.
    Assumes the first column (index 0) is the ID column by default.
    Returns the first matching row as a list, or None if not found.
    """
    data = get_sheet_data(sheet_name)
    if not data:
        return None

    # item_id might be int, sheet data is string.
    str_item_id = str(item_id)

    for row in data:
        if len(row) > id_column_index and row[id_column_index] == str_item_id:
            return row
    return None

def update_row(sheet_name: str, row_index: int, new_row_data: list):
    """
    Updates an entire row at a given index (1-based) in a sheet.
    """
    sheet_service = _get_spreadsheet()
    if not sheet_service:
        return None

    range_to_update = f"{sheet_name}!A{row_index}"
    try:
        body = {'values': [new_row_data]}
        result = sheet_service.values().update(
            spreadsheetId=SHEET_ID,
            range=range_to_update,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        logger.info(f"Updated {result.get('updatedCells')} cells in sheet '{sheet_name}' at row {row_index}.")
        return result
    except HttpError as err:
        logger.error(f"Error updating sheet '{sheet_name}': {err}")
        return None

# Example usage:
# from utils.gsheets import append_row, get_sheet_data, find_row_by_id
# append_row('users', [12345, 'Jules', 30, 'France', 'AI', 'jules@example.com'])
# user_data = find_row_by_id('users', 12345)
# all_users = get_sheet_data('users')
