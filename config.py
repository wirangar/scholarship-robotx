import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Admin Chat ID for notifications
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Google Sheets API credentials
# You'll need to set up a service account and get the JSON key file
# GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "path/to/your/credentials.json")

# Default language
DEFAULT_LANGUAGE = "fa"

# Supported languages
SUPPORTED_LANGUAGES = ["fa", "en", "it"]
