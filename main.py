import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    # بررسی تگ شدن یا ریپلای شدن
    if (message.reply_to_message and message.reply_to_message.from_user.id == context.bot.id) or        (f"@{context.bot.username.lower()}" in message.text.lower()):

        prompt = message.text.replace(f"@{context.bot.username}", "").strip()

        # ارسال پیام به OpenRouter
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        import requests
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "openchat/openchat-7b:free",
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=10
        )
        data = response.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "پاسخی دریافت نشد.")

        await message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
