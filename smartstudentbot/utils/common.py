from fastapi import HTTPException
import re
import json
from config import JSON_VERSION
from typing import Any, Dict

def sanitize_markdown(text: str) -> str:
    """
    Removes or escapes characters that have special meaning in Telegram's MarkdownV2.
    """
    # Characters to be escaped: _ * [ ] ( ) ~ ` > # + - = | { } . !
    escape_chars = r'([_*\[\]()~`>#\+\-=|{}.!])'
    return re.sub(escape_chars, r'\\\1', text)

def validate_file(file_size: int, file_type: str) -> bool:
    """
    Validates file size and type against predefined limits.
    """
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES = ["pdf", "jpg", "png", "mp3", "mp4", "jpeg"]

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE / (1024*1024)}MB")

    # Extract extension from mimetype if needed, e.g., 'image/jpeg' -> 'jpeg'
    normalized_file_type = file_type.split('/')[-1]

    if normalized_file_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid file format. Allowed formats: {', '.join(ALLOWED_FILE_TYPES)}")

    return True

import os
from functools import lru_cache

# Define the base directory of the project (smartstudentbot)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG_DIR = os.path.join(BASE_DIR, "lang")

@lru_cache(maxsize=10) # Cache up to 10 language files
def load_language_data(lang: str = "en") -> dict:
    """
    Loads a language JSON file from the lang directory.
    Falls back to English if the specified language is not found.
    Caches the result to avoid repeated file I/O.
    """
    file_path = os.path.join(LANG_DIR, f"{lang}.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to English and avoid trying to load a non-existent file again
        with open(os.path.join(LANG_DIR, "en.json"), "r", encoding="utf-8") as f:
            return json.load(f)

def check_json_version(file_path: str, expected_version: str = JSON_VERSION) -> Dict[str, Any]:
    """
    Loads a JSON file and checks if its version matches the expected version.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if data.get("version") != expected_version:
            raise ValueError(f"Unsupported JSON version in {file_path}. Expected {expected_version}, got {data.get('version')}")

        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found at path: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Could not decode JSON from file: {file_path}")
