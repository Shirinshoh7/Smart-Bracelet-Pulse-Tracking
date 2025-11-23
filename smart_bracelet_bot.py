from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random
import asyncio

TOKEN = "7969338593:AAGTgNmx2l7zLujW4oBjQACQVh-wA45cnfk"

# Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    [["🚀 Старт", "💓 Текущий пульс"]],
    resize_keyboard=True
)

# Проверка пульса (имитация)
async def get_pulse():
    return random.randint(60, 150)  # случайное значение пульса

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот умного браслета.\nВыберите действие:",
        reply_markup=main_keyboard
    )

# Обработка кнопок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🚀 Старт":
        await update.message.reply_text("Бот запущен! Наблюдаю за пульсом 👀")

    elif text == "💓 Текущий пульс":
        pulse = await get_pulse()
        msg = f"Ваш текущий пульс: {pulse} уд/мин"
        await update.message.reply_text(msg)

        # Проверяем превышение нормы
        if pulse > 100:
            await send_alert(update, pulse)

    else:
        await update.message.reply_text("Выберите действие с помощью кнопок ⬇️")

# Функция авто-SMS
async def send_alert(update: Update, pulse):
    alert_msg = f"⚠️ Внимание! Высокий пульс: {pulse} уд/мин!"
    await update.message.reply_text(alert_msg)

    # Здесь можно добавить отправку SMS через API (например Twilio или SMSC.ru)
    # Пример (фиктивно):
    # send_sms("+77001234567", alert_msg)

# Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
