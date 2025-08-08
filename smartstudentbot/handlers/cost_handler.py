from aiogram import Router, types
from aiogram.filters import Command
import json
import os

from utils.logger import log_action

router = Router()

# Define the path to the data file
DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cost_of_living.json")

def load_cost_data() -> dict:
    """Loads the cost_of_living.json file."""
    try:
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

@router.message(Command("cost"))
async def cmd_cost(message: types.Message):
    """
    Handles the /cost command.
    Displays a formatted summary of the cost of living in Perugia.
    """
    log_action("cost_command", message.from_user.id)

    cost_data = load_cost_data().get("data", [])

    if not cost_data:
        await message.reply("Sorry, cost of living information is currently unavailable.")
        return

    response_text = "💰 **Estimated Cost of Living in Perugia** 💰\n\n"

    for category in cost_data:
        response_text += f"*{category.get('category')}*\n"
        for item in category.get("items", []):
            response_text += f"  - {item.get('name')}: *{item.get('cost')}*\n"
            if item.get('notes'):
                response_text += f"    _{item.get('notes')}_\n"
        response_text += "\n"

    response_text += "_Disclaimer: These are estimates and can vary based on your lifestyle._"

    await message.reply(response_text, parse_mode="Markdown")
