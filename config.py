# -*- coding: utf-8 -*-
"""
Loads all configuration from environment variables.
For security and flexibility, no hardcoded values are allowed.
"""
import os
import json
import base64
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

def get_env_var(key: str, required: bool = True, default=None):
    """
    Retrieves an environment variable.
    Raises a ValueError if a required variable is missing.
    """
    value = os.environ.get(key, default)
    if required and value is None:
        raise ValueError(f"Error: Required environment variable '{key}' is not set.")
    return value

# --- Telegram Bot Configuration ---
TELEGRAM_BOT_TOKEN = get_env_var("TELEGRAM_BOT_TOKEN")
BASE_URL = get_env_var("BASE_URL")
WEBHOOK_SECRET = get_env_var("WEBHOOK_SECRET")
ADMIN_CHAT_ID = get_env_var("ADMIN_CHAT_ID")

# --- External API Keys ---
OWM_API_KEY = get_env_var("OWM_API_KEY")
EXCHANGE_RATE_API_KEY = get_env_var("EXCHANGE_RATE_API_KEY")
HUGGINGFACE_API_KEY = get_env_var("HUGGINGFACE_API_KEY", required=False)

# --- Google Services Credentials ---
# The GOOGLE_CREDS should be a base64 encoded string of the service account JSON file
GOOGLE_CREDS_BASE64 = get_env_var("GOOGLE_CREDS")
try:
    GOOGLE_CREDS_JSON = base64.b64decode(GOOGLE_CREDS_BASE64)
    GOOGLE_CREDS = json.loads(GOOGLE_CREDS_JSON)
except (json.JSONDecodeError, TypeError, ValueError) as e:
    raise ValueError(f"Error decoding GOOGLE_CREDS. Make sure it's a valid base64 encoded JSON. Error: {e}")

GOOGLE_DRIVE_UPLOAD_FOLDER_ID = get_env_var("GOOGLE_DRIVE_UPLOAD_FOLDER_ID")
SHEET_ID = get_env_var("SHEET_ID")
SPREADSHEET_NAME = get_env_var("SPREADSHEET_NAME", default="PerugiaBotData")
QUESTIONS_SHEET_NAME = get_env_var("QUESTIONS_SHEET_NAME", default="questions")


# --- Redis Configuration ---
REDIS_URL = get_env_var("REDIS_URL")

# --- Application Settings ---
PORT = int(get_env_var("PORT", default="8000"))
LOG_LEVEL = get_env_var("LOG_LEVEL", default="INFO").upper()

# --- ISEE Calculation Constants ---
ISEE_THRESHOLD = 23000.0
ISEE_PROPERTY_COEFF = 500.0

# Family coefficients for ISEE calculation
ISEE_FAMILY_COEFFICIENTS = {
    1: 1.0,
    2: 1.57,
    3: 2.04,
    4: 2.46,
    5: 2.85,
}
ISEE_FAMILY_EXTRA_MEMBER_COEFF = 0.35

# --- Other Constants ---
GITHUB_DATA_URL = "https://raw.githubusercontent.com/your_username/your_repo/main/data/" # Placeholder
CACHE_TTL_SECONDS = 15 * 60  # 15 minutes
