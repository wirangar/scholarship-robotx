# -*- coding: utf-8 -*-
"""
Handler for the /live_chat feature.
Connects a user with an admin for real-time conversation.
"""
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from utils.gates import require_registration
from config import ADMIN_CHAT_ID

# --- Conversation States ---
CHATTING = 0

# A simple in-memory mapping to find the user a chat belongs to.
# In a multi-worker environment, this should be stored in Redis.
admin_to_user_chat_map = {}

@require_registration
async def start_live_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the live chat session."""
    await update.message.reply_text(
        "You are now connected to an admin. Any messages you send will be forwarded.\n"
        "Type /end_chat to finish the conversation."
    )
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"🔔 User {update.effective_user.id} ({update.effective_user.full_name}) has started a live chat."
    )
    return CHATTING

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Forwards a user's message to the admin."""
    user = update.effective_user
    # Forward the message. This preserves the original message content (text, photo, etc.)
    # and also provides a way for the admin to reply to it.
    forwarded_message = await update.message.forward(chat_id=ADMIN_CHAT_ID)

    # Map the forwarded message ID in the admin chat to the user's chat ID
    # so we know who to reply to.
    admin_to_user_chat_map[forwarded_message.message_id] = user.id

    return CHATTING

async def forward_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles a reply from an admin in the admin chat and forwards it to the correct user.
    """
    # This handler only works in the admin chat
    if str(update.effective_chat.id) != str(ADMIN_CHAT_ID):
        return

    replied_to_message = update.message.reply_to_message
    if not replied_to_message:
        return

    # Find the user's chat ID from our map
    user_chat_id = admin_to_user_chat_map.get(replied_to_message.message_id)

    if user_chat_id:
        # Send a copy of the admin's message to the user
        await context.bot.send_message(
            chat_id=user_chat_id,
            text=f"💬 *Admin says:*\n{update.message.text}",
            parse_mode='MarkdownV2'
        )

async def end_live_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ends the live chat session."""
    user = update.effective_user
    await update.message.reply_text("You have disconnected from the live chat.")

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"User {user.id} has ended the live chat."
    )

    # Clean up any mappings related to this user
    keys_to_delete = [k for k, v in admin_to_user_chat_map.items() if v == user.id]
    for key in keys_to_delete:
        del admin_to_user_chat_map[key]

    return ConversationHandler.END

# --- Conversation Handler for the user side ---
live_chat_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('live_chat', start_live_chat)],
    states={
        CHATTING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin),
            CommandHandler('end_chat', end_live_chat)
        ],
    },
    fallbacks=[CommandHandler('end_chat', end_live_chat)],
)

# --- A separate handler for admin replies ---
# This handler should be added to the application in main.py
admin_reply_handler = MessageHandler(
    filters.Chat(chat_id=int(ADMIN_CHAT_ID)) & filters.REPLY,
    forward_to_user
)
