import json
import os
from typing import Dict, Any

# Define the base directory of the project (smartstudentbot)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS_FILE_PATH = os.path.join(BASE_DIR, "news.json")

def save_news_item(news_item: Dict[str, Any]):
    """
    Saves a new news item to the news.json file.
    New items are inserted at the beginning of the list.
    """
    try:
        # Read existing data
        with open(NEWS_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid, start with a fresh structure
        data = {"version": "1.0", "data": []}

    # Add the new item and mark as published
    news_item["published"] = True
    data["data"].insert(0, news_item)

    # Write the updated data back to the file
    with open(NEWS_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
