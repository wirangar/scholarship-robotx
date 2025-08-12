# -*- coding: utf-8 -*-
"""
Admin-only command handlers.
"""
import asyncio
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from utils.gates import require_admin
from utils.gsheets import get_sheet_data, update_row
from utils.i18n import get_text

@require_admin
async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Answers a pending question.
    Usage: /answer <question_id> <answer_text>
    """
    admin = update.effective_user
    lang = get_user_language(admin.id, context) # For admin-facing messages

    try:
        # The first arg is the question ID, the rest is the answer text
        question_id = context.args[0]
        answer_text = " ".join(context.args[1:])

        if not answer_text:
            await update.message.reply_text("Usage: /answer <ID> <text>")
            return

    except (ValueError, IndexError):
        await update.message.reply_text("Usage: /answer <ID> <text>")
        return

    # Find the question in the sheet
    questions_data = get_sheet_data('questions')
    row_index_to_update = -1
    question_row = None

    for i, row in enumerate(questions_data):
        # Assuming question ID is in the first column (index 0)
        if len(row) > 0 and str(row[0]) == str(question_id):
            row_index_to_update = i + 1 # GSheets are 1-indexed
            question_row = row
            break

    if not question_row or row_index_to_update == -1:
        await update.message.reply_text(f"Question with ID {question_id} not found.")
        return

    # Update the row with the answer and new status
    # Assumed format: ID, UserID, Question, Answer, Status, Timestamp
    original_user_id = question_row[1]
    question_text = question_row[2]

    updated_row = [
        question_row[0], # ID
        original_user_id,
        question_text,
        answer_text,
        "answered",
        question_row[5] # Timestamp
    ]

    update_row('questions', row_index_to_update, updated_row)

    await update.message.reply_text(f"✅ Answer for question {question_id} has been saved.")

    # Notify the original user
    try:
        user_lang = 'fa' # We don't have the user's context here, would need to fetch from their profile
        notification_text = get_text('qna_answer_notification', user_lang).format(
            question=question_text,
            answer=answer_text
        )
        await context.bot.send_message(
            chat_id=original_user_id,
            text=notification_text,
            parse_mode='MarkdownV2'
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Answer saved, but failed to notify user {original_user_id}. Error: {e}")


# Placeholder for other admin commands
@require_admin
async def approve_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Approves a pending success story.
    Usage: /approve_story <story_id>
    """
    try:
        story_id_to_approve = context.args[0]
    except IndexError:
        await update.message.reply_text("Usage: /approve_story <story_id>")
        return

    stories_data = get_sheet_data('success_stories')
    row_index_to_update = -1
    story_row = None

    for i, row in enumerate(stories_data):
        # Assuming story ID is in the first column (index 0)
        if len(row) > 0 and str(row[0]) == str(story_id_to_approve):
            row_index_to_update = i + 1
            story_row = row
            break

    if not story_row or row_index_to_update == -1:
        await update.message.reply_text(f"Story with ID {story_id_to_approve} not found.")
        return

    if story_row[5] == 'approved':
        await update.message.reply_text(f"Story {story_id_to_approve} is already approved.")
        return

    # Update status to 'approved'
    story_row[5] = 'approved'
    update_row('success_stories', row_index_to_update, story_row)

    await update.message.reply_text(f"✅ Success story {story_id_to_approve} has been approved.")

@require_admin
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends a message to all registered users.
    Usage: /broadcast <message_text>
    """
    message_text = " ".join(context.args)
    if not message_text:
        await update.message.reply_text("Usage: /broadcast <message>")
        return

    all_users = get_sheet_data('users')
    if not all_users:
        await update.message.reply_text("No users found to broadcast to.")
        return

    await update.message.reply_text(f"Starting broadcast to {len(all_users) - 1} users...")

    success_count = 0
    fail_count = 0

    # Start from index 1 to skip header row
    for user_row in all_users[1:]:
        user_id = user_row[0]
        try:
            await context.bot.send_message(chat_id=user_id, text=message_text)
            success_count += 1
        except Exception as e:
            print(f"Failed to send broadcast to {user_id}: {e}")
            fail_count += 1

        await asyncio.sleep(0.1) # 10 messages per second, well within limits

    await update.message.reply_text(
        f"Broadcast finished.\n"
        f"Successfully sent: {success_count}\n"
        f"Failed to send: {fail_count}"
    )


# Need to add get_user_language to gates.py if it's not there.
# It is there, but it requires context. A better way would be to fetch from GSheets.
# For now, this is a simplified implementation.
def get_user_language(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get('language', 'fa')
