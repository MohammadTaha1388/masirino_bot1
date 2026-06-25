import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8342491323:AAFgmXGyHjNI086EucC1K5WDCKUHIMiuPG0"

goals = [
    ["برنامه‌نویسی", "کنکور"],
    ["زبان انگلیسی", "تناسب اندام"],
    ["کسب درآمد"]
]

plans = {
    "برنامه‌نویسی": "امروز ۱ ساعت پایتون تمرین کن.",
    "کنکور": "امروز ۲ ساعت مطالعه متمرکز داشته باش.",
    "زبان انگلیسی": "۲۰ لغت جدید یاد بگیر.",
    "تناسب اندام": "۳۰ دقیقه ورزش کن.",
    "کسب درآمد": "یک ایده درآمدی جدید بررسی کن."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(goals, resize_keyboard=True)

    await update.message.reply_text(
        "👋 به مسیرنو خوش اومدی!\n\nهدفت رو انتخاب کن:",
        reply_markup=keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in plans:
        await update.message.reply_text(
            f"🎯 هدف: {text}\n\n📋 برنامه امروز:\n{plans[text]}"
        )
    else:
        await update.message.reply_text("لطفاً یکی از گزینه‌ها را انتخاب کن.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("MasirNo Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
