import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import requests
from flask import Flask
from threading import Thread

TELEGRAM_TOKEN = "8321842423:AAG104h9Hz5V5N-4DysVGmrj4O0LMoVba00"
GEMINI_API_KEY = "AQ.Ab8RN6JNmviGc4BgJ1MsYTNWAuvvBmrYG7cmRwgRPeJ5o9tf-g"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

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
        headers = {"X-goog-api-key": GEMINI_API_KEY, "Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": f"Siz aqlli o'zbek tilidagi yordamchisiz. Foydalanuvchi savoli: {text}"}]}]}
        r = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=30)
        data = r.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"] if "candidates" in data else f"API javobi: {data}"
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
