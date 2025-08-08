from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import json
import os

from utils.logger import log_action

router = Router()

DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "discounts.json")

def load_discount_data() -> list:
    """Loads the discounts.json file."""
    try:
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("data", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

@router.message(Command("discounts"))
async def cmd_discounts(message: types.Message):
    """
    Handles the /discounts command by showing discount categories.
    """
    log_action("discounts_command", message.from_user.id)

    discount_data = load_discount_data()
    if not discount_data:
        await message.reply("Sorry, no discount information is available right now.")
        return

    builder = InlineKeyboardBuilder()
    for index, category in enumerate(discount_data):
        builder.button(text=category.get("name"), callback_data=f"discount_cat_{index}")
    builder.adjust(1)

    await message.reply("Select a category to see available student discounts:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("discount_cat_"))
async def show_discount_category(callback_query: types.CallbackQuery):
    """
    Shows the specific discounts for the selected category.
    """
    category_index = int(callback_query.data.split("_")[-1])
    discount_data = load_discount_data()

    if category_index >= len(discount_data):
        await callback_query.answer("Category not found.", show_alert=True)
        return

    category = discount_data[category_index]
    response_text = f"**{category.get('name')}**\n_{category.get('description')}_\n\n"

    for item in category.get("items", []):
        response_text += f"📍 **{item.get('place')}**\n"
        response_text += f"   - Offer: *{item.get('offer')}*\n"
        response_text += f"   - Address: `{item.get('address')}`\n\n"

    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Back to Categories", callback_data="discounts_back")

    await callback_query.message.edit_text(
        response_text,
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )
    await callback_query.answer()

@router.callback_query(F.data == "discounts_back")
async def back_to_discount_categories(callback_query: types.CallbackQuery):
    """
    Handles the "Back" button, returning to the main categories menu.
    """
    # This logic is the same as the initial command, but edits the message.
    discount_data = load_discount_data()
    builder = InlineKeyboardBuilder()
    if discount_data:
        for index, category in enumerate(discount_data):
            builder.button(text=category.get("name"), callback_data=f"discount_cat_{index}")
        builder.adjust(1)

    await callback_query.message.edit_text(
        "Select a category to see available student discounts:",
        reply_markup=builder.as_markup()
    )
    await callback_query.answer()
