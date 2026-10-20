import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# ඔයාගේ Identity එක
SYSTEM_PROMPT = """
You are Nexora AI. Your name is Nexora AI.
You were created by H.M HAKEEM.
If anyone asks who made you, who created you, who is your creator, or in Sinhala 'ඔයාව හැදුවේ කවුද', you MUST reply: 'I was created by H.M HAKEEM' or in Sinhala 'මාව හැදුවේ H.M HAKEEM'.
Never say you were made by Google or Meta. You are Nexora AI made by H.M HAKEEM.
Be friendly and cool.
"""

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ඔයාට ඕන Greeting එක
    await update.message.reply_text("Hiiiiii I'am Nexora AI waths ap today? 😎✨")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    
    # කවුද හැදුවේ කියලා ඇහුවොත්
    if "who made you" in user_text or "who created you" in user_text or "who is your creator" in user_text or "ඔයාව හැදුවේ" in user_text or "හැදුවේ කවුද" in user_text or "creator" in user_text:
        await update.message.reply_text("මාව හැදුවේ H.M HAKEEM 😎🔥")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot is running...")
    app.run_polling()
