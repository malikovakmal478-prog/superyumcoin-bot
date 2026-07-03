from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import requests
from flask import Flask
from threading import Thread

TELEGRAM_TOKEN = "8321842423:AAHsI1cxehoKEKLKjE7ZmM0xOoLoqClq4wc"
GEMINI_API_KEY = "AQ.Ab8RN6Kdk7Gh2EvhEafRYGyq4ZU9ySTmwlcZn-aydgGwwtpoSg"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Bot ishlayapti"

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men aqlli yordamchiman. Menga xabar yozing.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        payload = {"contents": [{"parts": [{"text": f"Siz aqlli o'zbek tilidagi yordamchisiz. Foydalanuvchi savoli: {text}"}]}]}
        r = requests.post(GEMINI_URL, json=payload, timeout=30)
        data = r.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"] if "candidates" in data else f"API javobi: {data}"
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {e}")

Thread(target=run_flask).start()

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot ishga tushdi...")
app.run_polling()
