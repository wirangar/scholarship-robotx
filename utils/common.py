# -*- coding: utf-8 -*-
"""
Common utility functions, validators, and helpers used across the application.
"""
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import ISEE_FAMILY_COEFFICIENTS, ISEE_FAMILY_EXTRA_MEMBER_COEFF

def sanitize_markdown(text: str) -> str:
    """
    Escapes characters that have special meaning in Telegram's MarkdownV2.
    """
    if not isinstance(text, str):
        return ""

    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def is_valid_email(email: str) -> bool:
    """
    Validates an email address using a simple regex.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_age(age_str: str) -> bool:
    """
    Validates that the age is an integer between 16 and 100.
    """
    try:
        age = int(age_str)
        return 16 <= age <= 100
    except (ValueError, TypeError):
        return False

def get_family_coeff(family_n: int) -> float:
    """
    Calculates the family coefficient for the ISEE calculation based on the number of members.
    """
    if family_n <= 0:
        return 1.0
    if family_n in ISEE_FAMILY_COEFFICIENTS:
        return ISEE_FAMILY_COEFFICIENTS[family_n]
    if family_n > 5:
        # For families larger than 5, add 0.35 for each additional member
        base_coeff = ISEE_FAMILY_COEFFICIENTS[5]
        extra_members = family_n - 5
        return base_coeff + (extra_members * ISEE_FAMILY_EXTRA_MEMBER_COEFF)
    return 1.0 # Fallback for any other case

def build_menu(buttons: list, n_cols: int, header_buttons=None, footer_buttons=None) -> InlineKeyboardMarkup:
    """
    Builds an InlineKeyboardMarkup from a list of InlineKeyboardButtons.

    Args:
        buttons: A list of InlineKeyboardButton objects.
        n_cols: The number of columns to arrange the buttons in.
        header_buttons: Optional list of buttons to add at the top.
        footer_buttons: Optional list of buttons to add at the bottom.
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return InlineKeyboardMarkup(menu)

# Example of creating a button
# from utils.i18n import get_text
# from telegram import InlineKeyboardButton
# lang = 'fa'
# my_button = InlineKeyboardButton(get_text('button_main_menu', lang), callback_data='main_menu')
