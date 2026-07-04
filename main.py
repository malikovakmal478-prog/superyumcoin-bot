import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import google.generativeai as genai
from flask import Flask
from threading import Thread

TELEGRAM_TOKEN = "8321842423:AAG104h9Hz5V5N-4DysVGmrj4O0LMoVba00"
GEMINI_API_KEY = "AQ.Ab8RN6IHy4HWabNsntF4X55Kw3jqryQwSnyZntvv9617PJ8ULg"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-flash-latest")

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
        response = model.generate_content(f"Siz aqlli o'zbek tilidagi yordamchisiz. Foydalanuvchi savoli: {text}")
        await update.message.reply_text(response.text)
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
