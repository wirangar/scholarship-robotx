import json
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def load_content():
    """Loads the content from the data/content.json file."""
    try:
        with open("data/content.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Could not load or parse content.json: {e}")
        return {}

def get_text(path: str, lang: str, default_lang: str = "en"):
    """
    Retrieves a text from the content dictionary using a dot-separated path.
    Example: get_text('scholarships.title', 'fa')

    If the final value is a dictionary, it tries to find the key corresponding
    to the language.
    """
    content = load_content()
    keys = path.split('.')
    current_level = content

    for key in keys:
        if isinstance(current_level, dict) and key in current_level:
            current_level = current_level[key]
        else:
            logger.warning(f"Path '{path}' not found in content.json")
            return f"_{path}_" # Return a placeholder for missing text

    if isinstance(current_level, dict):
        # If we have a dictionary of languages, get the correct one
        return current_level.get(lang, current_level.get(default_lang, f"_{path}.{lang}_"))
    elif isinstance(current_level, str):
        # If it's just a string (e.g., a deadline), return it directly
        return current_level
    else:
        # If it's something else (like a list), we might want to handle it differently
        # For now, we'll just return it as is.
        return current_level

if __name__ == '__main__':
    # Example usage for testing
    print("Testing content_manager...")
    print(f"Scholarships Title (FA): {get_text('scholarships.title', 'fa')}")
    print(f"Scholarships Title (EN): {get_text('scholarships.title', 'en')}")
    print(f"DSU Details (IT): {get_text('scholarships.options.dsu.details', 'it')}")
    print(f"PhD Deadline: {get_text('scholarships.options.university_of_perugia_phd.deadline', 'en')}")
    print(f"Missing Path: {get_text('non.existent.path', 'fa')}")
