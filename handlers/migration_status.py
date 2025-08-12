# -*- coding: utf-8 -*-
"""
Handler for the /migration_status command.
Displays a static checklist for the immigration process.
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from utils.gates import require_registration
from utils.i18n import get_text
from utils.common import sanitize_markdown

# The checklist is hardcoded here for simplicity.
# It could also be moved to a JSON file in /data.
MIGRATION_CHECKLIST = {
    'fa': [
        ("✅", "دریافت پذیرش از دانشگاه"),
        ("✅", "دریافت ویزای تحصیلی ایتالیا"),
        ("⭕️", "ورود به ایتالیا و ثبت اظهارنامه حضور"),
        ("⭕️", "درخواست کارت اقامت (Permesso di Soggiorno)"),
        ("⭕️", "دریافت کد مالیاتی (Codice Fiscale)"),
        ("⭕️", "افتتاح حساب بانکی"),
        ("⭕️", "ثبت‌نام در سیستم بهداشت ملی (SSN)"),
    ],
    'en': [
        ("✅", "Receive university admission letter"),
        ("✅", "Obtain Italian study visa"),
        ("⭕️", "Enter Italy and declare presence"),
        ("⭕️", "Apply for Residence Permit (Permesso di Soggiorno)"),
        ("⭕️", "Get tax code (Codice Fiscale)"),
        ("⭕️", "Open a bank account"),
        ("⭕️", "Register with the National Health Service (SSN)"),
    ]
}

@require_registration
async def show_migration_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the migration checklist."""
    lang = get_user_language(update.effective_user.id, context)

    checklist = MIGRATION_CHECKLIST.get(lang, MIGRATION_CHECKLIST['en'])

    text = get_text('migration_checklist_title', lang)
    for status, item in checklist:
        text += f"\n{status} {sanitize_markdown(item)}"

    await update.message.reply_text(text, parse_mode='MarkdownV2')


# This is a helper function that should be in utils/gates.py, but is duplicated here for simplicity
def get_user_language(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get('language', 'fa')
