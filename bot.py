import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

# --- Переменные окружения ---
API_ID = int(os.environ.get("TELEGRAM_API_ID"))
API_HASH = os.environ.get("TELEGRAM_API_HASH")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# --- Flask для пробуждения Render ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, use_reloader=False)

# --- Pyrogram клиент ---
bot = Client(
    "smm_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Обработчик /start ---
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Загрузка...", reply_markup=ReplyKeyboardRemove())
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Telegram Stars", callback_data="stars"),
         InlineKeyboardButton("💎 Telegram Premium", callback_data="premium")],
        [InlineKeyboardButton("📈 Накрутка Telegram", callback_data="tg_boost"),
         InlineKeyboardButton("📸 Накрутка Instagram", callback_data="inst_boost")]
    ])
    
    await message.reply_text("Выберите нужный раздел:", reply_markup=keyboard)

# --- Запуск бота в отдельном потоке ---
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def main():
        await bot.start()
        print("Бот запущен!")
        await idle()

    loop.run_until_complete(main())

if __name__ == "__main__":
    # Запускаем бота в фоне
    threading.Thread(target=run_bot, daemon=True).start()
    # Flask работает в главном потоке
    run_flask()
