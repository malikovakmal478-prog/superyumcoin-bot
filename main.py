import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import requests
from flask import Flask
from threading import Thread

TELEGRAM_TOKEN = "8321842423:AAG104h9Hz5V5N-4DysVGmrj4O0LMoVba00"
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Bot ishlayapti"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men aqlli yordamchiman. Menga xabar yozing.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/llama-3.1-8b-instruct",
            "messages": [
                {"role": "system", "content": "Siz aqlli o'zbek tilidagi yordamchisiz."},
                {"role": "user", "content": text}
            ]
        }
        r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        data = r.json()
        reply = data["choices"][0]["message"]["content"] if "choices" in data else f"API javobi: {data}"
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {e}")

def main():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    Thread(target=run_flask, daemon=True).start()

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()
