# -*- coding: utf-8 -*-
"""
Centralized logging configuration.
"""
import logging
import sys
import json
from logging.handlers import TimedRotatingFileHandler
from config import LOG_LEVEL, ADMIN_CHAT_ID

# Using a basic bot instance placeholder for alerting.
# In the main application, this will be replaced with the actual bot instance.
_bot_instance = None

def setup_bot_instance_for_logging(bot):
    """
    Allows the main application to pass the bot instance to the logger
    so it can send alerts to the admin.
    """
    global _bot_instance
    _bot_instance = bot

class JsonFormatter(logging.Formatter):
    """
    Formats log records as a JSON string.
    """
    def format(self, record):
        log_object = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_object['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(log_object)

def get_logger(name: str):
    """
    Configures and returns a logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False # Avoid duplicate logs in parent loggers

    if not logger.handlers:
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        formatter = JsonFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Optional: File handler (e.g., for production)
        # file_handler = TimedRotatingFileHandler("logs/app.log", when="midnight", backupCount=30)
        # file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)

    return logger

# A throttled function to alert admin would be implemented here, likely using Redis
# For now, a simple function placeholder:
async def alert_admin(message: str):
    """
    Sends an alert message to the admin chat ID.
    TODO: Implement throttling (e.g., once every 5 minutes) using Redis.
    """
    logger = get_logger(__name__)
    if _bot_instance and ADMIN_CHAT_ID:
        try:
            await _bot_instance.send_message(chat_id=ADMIN_CHAT_ID, text=f"🚨 BOT ALERT 🚨\n\n{message}")
        except Exception as e:
            logger.error(f"Failed to send alert to admin: {e}")
    else:
        logger.warning("Admin alert requested, but bot instance or ADMIN_CHAT_ID not set.")

# Example usage:
# from utils.logger import get_logger, alert_admin
# logger = get_logger(__name__)
# logger.info("This is an info message.")
# await alert_admin("This is a critical alert.")
