from telegram import Update
from telegram.ext import ContextTypes
from .AntiSpam import is_spamming_globally
from .Tokens import SALATIN
from .AI import ai_summarize, ai_opinion
import time
import re

def escape_usernames(text: str) -> str:
    return re.sub(
        r'@([A-Za-z0-9]+(?:_(?!\\)[A-Za-z0-9]+)*)',
        lambda m: '@' + m.group(1).replace('_', '\\_'),
        text
    )

ALLOWED_GROUPS = [
    -1001694787846,
    -1002678431127,
    -1002727773269,
    -1002594376990
]

async def IDCheck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in SALATIN:
        chat_id = update.effective_chat.id  
        await update.message.reply_text(chat_id)
    
async def github_repo_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await is_spamming_globally(update, user_id):
        return
    
    repo_link = "https://github.com/Nec-ro/IUTCessa_Bot"
    await update.message.reply_text(
        f"🚀 <b>لینک مخزن گیت‌هاب ربات:</b>\n\n🔗 <a href='{repo_link}'>{repo_link}</a>",
        parse_mode="HTML",
        disable_web_page_preview=False
    )

# ----------------------------------------------------

async def tldr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.effective_chat.type == "private":
        return
    if update.effective_chat.id not in ALLOWED_GROUPS:
        return
    if await is_spamming_globally(update, user_id):
        return
    
    if update.message.reply_to_message and update.message.reply_to_message.text:
        original_text = update.message.reply_to_message.text
        if len(original_text) <= 600:
            try:
                response = await update.message.reply_text("متن مشخص شده هم‌اکنون هم طولانی نیست!")
                await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.effective_message.id)
                time.sleep(5)
                await context.bot.delete_message(chat_id=update.message.chat_id, message_id=response.message_id)
            except:
                pass
            return
        summary = ai_summarize(original_text)
        await update.message.reply_text(summary)
    else:
        try:
            response = await update.message.reply_text("لطفا این دستور را روی یک پیام ریپلای بزنید.")
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.effective_message.id)
            time.sleep(5)
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=response.message_id)
        except:
            pass

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.effective_chat.type == "private":
        return
    if update.effective_chat.id not in ALLOWED_GROUPS:
        return
    if await is_spamming_globally(update, user_id):
        return
    
    if update.message.reply_to_message and update.message.reply_to_message.text:
        original_text = update.message.reply_to_message.text
        original_username = update.message.reply_to_message.from_user.username
        requester_username = update.effective_user.username
        bot_username = context.bot.username
        opinion = ai_opinion(original_text, original_username, requester_username, bot_username)
        try:
            opinionMK = escape_usernames(opinion)
            await update.message.reply_text(text=opinionMK, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(text=opinion)
    else:
        try:
            response = await update.message.reply_text("لطفا این دستور را روی یک پیام ریپلای بزنید.")
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.effective_message.id)
            time.sleep(5)
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=response.message_id)
        except:
            pass

async def qdc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.type == "private":
        return
    if not update.message.reply_to_message:
        try:
            response = await update.message.reply_text("لطفا این دستور را روی یک پیام ریپلای بزنید.")
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.effective_message.id)
            time.sleep(5)
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=response.message_id)
        except:
            pass
        return
    try:
        target = f"@{update.effective_user.username}" if update.effective_user.username else str(update.effective_user.id)    
        await context.bot.copy_message(
            chat_id=update.message.chat_id,                         # Destination chat (user who triggered the command)
            from_chat_id=-1002635821987,                            # Source private channel
            message_id=53,                                          # Message to forward
            disable_notification=True,                              # Optional: Send silently
            reply_to_message_id=update.message.reply_to_message.id, # Reply to what
            caption= f"Sent by {target}"                            # Say what
        )
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.effective_message.id)

    except Exception as e:
        await update.message.reply_text(f"Failed to forward or delete message: {e}")