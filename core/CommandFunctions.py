from telegram import Update
from .Tokens import SALATIN

async def IDCheck(update: Update):
    user_id = update.effective_user.id
    if user_id in SALATIN:
        chat_id = update.effective_chat.id  
        await update.message.reply_text(chat_id)