# -*- coding: utf-8 -*-
"""
Google Drive utility functions.
Handles file uploads and management.
"""
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
import io

from utils.gsheets import creds # Re-use credentials from gsheets
from config import GOOGLE_DRIVE_UPLOAD_FOLDER_ID
from utils.logger import get_logger

logger = get_logger(__name__)

# --- Service Setup ---

service = None
if creds:
    try:
        service = build('drive', 'v3', credentials=creds)
    except Exception as e:
        logger.error(f"Failed to build Google Drive service: {e}")

# --- Helper Functions ---

def upload_file_to_drive(file_content: bytes, filename: str, mimetype: str) -> str | None:
    """
    Uploads a file to the specified Google Drive folder.

    Args:
        file_content: The binary content of the file.
        filename: The desired name for the file in Google Drive.
        mimetype: The MIME type of the file (e.g., 'application/pdf').

    Returns:
        The file ID of the uploaded file, or None if the upload fails.
    """
    if not service:
        logger.error("Google Drive service is not available.")
        return None

    try:
        file_metadata = {
            'name': filename,
            'parents': [GOOGLE_DRIVE_UPLOAD_FOLDER_ID]
        }

        media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype=mimetype, resumable=True)

        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        file_id = file.get('id')
        logger.info(f"Successfully uploaded file '{filename}' with ID: {file_id}")
        return file_id

    except HttpError as err:
        logger.error(f"An error occurred during file upload to Google Drive: {err}")
        return None
    except Exception as e:
        logger.error(f"A non-HTTP error occurred during file upload: {e}")
        return None

# Example usage:
# from utils.gdrive import upload_file_to_drive
# with open('my_resume.pdf', 'rb') as f:
#     content = f.read()
#     file_id = upload_file_to_drive(content, 'user_123_resume.pdf', 'application/pdf')
#     if file_id:
#         print(f"File uploaded. ID: {file_id}")
