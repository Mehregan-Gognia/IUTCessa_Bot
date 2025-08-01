from telegram import Update
from telegram.ext import ContextTypes
from .AntiSpam import is_spamming_globally
from .Tokens import SALATIN

async def IDCheck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in SALATIN:
        chat_id = update.effective_chat.id  
        await update.message.reply_text(chat_id)
    
async def github_repo_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if (await is_spamming_globally(update, user_id)) or update.effective_chat.type != "private":
        return
    repo_link = "https://github.com/Nec-ro/IUTCessa_Bot"
    await update.message.reply_text(
        f"🚀 <b>لینک مخزن گیت‌هاب ربات:</b>\n\n🔗 <a href='{repo_link}'>{repo_link}</a>",
        parse_mode="HTML",
        disable_web_page_preview=False
    )