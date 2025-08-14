from telegram import Update
from telegram.ext import ContextTypes
from .AntiSpam import is_spamming_globally
from .Tokens import SALATIN, GEMMA_API_KEY
from .AI import tldr_prompt
import time

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

from openai import OpenAI

client = OpenAI(
    api_key=GEMMA_API_KEY,
    base_url="https://api.avalai.ir/v1",
)

def ai_summarize(text: str) -> str:
    if len(text) <= 600:
        return "متن مشخص شده هم‌اکنون هم طولانی نیست!"

    prompt = tldr_prompt(text)

    response = client.chat.completions.create(
        model="gemma-3-27b-it",
        messages=[
            {"role": "user", "content": prompt}
        ],
        extra_body={"temperature": 0.75, "max_tokens": 250}
    )
    return response.choices[0].message.content.strip()

async def tldr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.effective_chat.type == "private":
        return
    if update.effective_chat.id not in [-1001694787846, -1002678431127]:
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
        # Forward the message
        username = update.effective_user.username
        if username:    
            await context.bot.copy_message(
                chat_id=update.message.chat_id,                         # Destination chat (user who triggered the command)
                from_chat_id=-1002635821987,                            # Source private channel
                message_id=53,                                          # Message to forward
                disable_notification=True,                              # Optional: Send silently
                reply_to_message_id=update.message.reply_to_message.id, # Reply to what
                caption= f"Sent by @{username}"                         # Say what
            )
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.effective_message.id)

    except Exception as e:
        await update.message.reply_text(f"Failed to forward or delete message: {e}")