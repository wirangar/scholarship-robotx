import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Telegram ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# --- Web Server & Webhook ---
BASE_URL = os.getenv("BASE_URL")
PORT = int(os.getenv("PORT", "8080"))

# --- Database ---
DATABASE_URL = os.getenv("DATABASE_URL")

# --- Google Sheets ---
SHEET_ID = os.getenv("SHEET_ID")
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME")
QUESTIONS_SHEET_NAME = os.getenv("QUESTIONS_SHEET_NAME")
GOOGLE_CREDS_PATH = os.getenv("GOOGLE_CREDS", "/etc/secrets/credentials.json")

# --- AI ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Bot Settings ---
DEFAULT_LANGUAGE = "fa"
SUPPORTED_LANGUAGES = ["fa", "en", "it"]
