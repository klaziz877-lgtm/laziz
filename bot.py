import os
import asyncio
from flask import Flask
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import threading

# --- Переменные окружения ---
API_ID = int(os.environ.get("TELEGRAM_API_ID"))
API_HASH = os.environ.get("TELEGRAM_API_HASH")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# --- Flask для пробуждения (Render требует, чтобы порт был открыт) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    # Отключаем лишние логи Flask
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
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

# --- Запуск ---
async def main():
    # Запускаем бота в текущем цикле событий
    await bot.start()
    print("Бот запущен!")
    await idle()

if __name__ == "__main__":
    # 1. Запускаем Flask в отдельном потоке (для пробуждения Render)
    threading.Thread(target=run_flask, daemon=True).start()
    
    # 2. Создаём цикл событий ВРУЧНУЮ для главного потока
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # 3. Запускаем бота
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
