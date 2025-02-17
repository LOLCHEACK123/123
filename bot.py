import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

SHOP_URL = "https://lolcheack123.github.io/123/"

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Привет! Я бот магазина. Используй /shop, чтобы перейти в магазин."
    )

async def shop(update: Update, context: CallbackContext):
    await update.message.reply_text(f"🛒 Магазин: [Перейти в магазин]({SHOP_URL})", parse_mode="Markdown")

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    if text == "/shop":
        await shop(update, context)
    else:
        await update.message.reply_text("Я не понимаю этот запрос. Используйте /shop.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("shop", shop))  # Добавили обработчик команды /shop
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
