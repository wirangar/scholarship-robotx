import sys
from loguru import logger

# Remove default handler
logger.remove()

# Add a handler for writing to a log file
log_file_path = "logs/app.log"
logger.add(log_file_path, rotation="1 MB", level="DEBUG", encoding="utf-8")

# Add a handler for console output
logger.add(sys.stderr, level="INFO")

def log_action(action: str, user_id: int, details: str = ""):
    """
    Logs a specific user action.
    """
    logger.info(f"Action: {action}, User: {user_id}, Details: {details}")
