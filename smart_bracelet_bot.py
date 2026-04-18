import random
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7969338593:AAGTgNmx2l7zLujW4oBjQACQVh-wA45cnfk"
PULSE_THRESHOLD = 100

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

MENU_BUTTONS = [["🚀 Старт", "💓 Текущий пульс"]]
MAIN_KEYBOARD = ReplyKeyboardMarkup(MENU_BUTTONS, resize_keyboard=True)

MESSAGES = {
    "start": "Привет! Я бот умного браслета ⌚\nНажмите на кнопку ниже, чтобы проверить состояние:",
    "monitoring": "Бот запущен! Начинаю мониторинг показателей 👀",
    "pulse_info": "📊 Ваш текущий пульс: **{pulse}** уд/мин",
    "alert": "🚨 **ВНИМАНИЕ!**\nВысокий пульс: {pulse} уд/мин! Пожалуйста, отдохните.",
    "unknown": "Пожалуйста, используйте кнопки меню ⬇️"
}

async def get_pulse_value() -> int:
    return random.randint(60, 150)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MESSAGES["start"], reply_markup=MAIN_KEYBOARD)

async def handle_user_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if user_text == "🚀 Старт":
        await update.message.reply_text(MESSAGES["monitoring"])

    elif user_text == "💓 Текущий пульс":
        pulse = await get_pulse_value()
        await update.message.reply_text(
            MESSAGES["pulse_info"].format(pulse=pulse), 
            parse_mode="Markdown"
        )

        if pulse > PULSE_THRESHOLD:
            await send_emergency_alert(update, pulse)
    else:
        await update.message.reply_text(MESSAGES["unknown"])

async def send_emergency_alert(update: Update, pulse: int):
    alert_text = MESSAGES["alert"].format(pulse=pulse)
    await update.message.reply_text(alert_text, parse_mode="Markdown")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_actions))

    logging.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()
