from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from ai import ask_ai

TOKEN = 8342491323:AAFgmXGyHjNI086EucC1K5WDCKUHIMiuPG0

keyboard = ReplyKeyboardMarkup(
    [
        ["💬 چت با AI"],
        ["📅 برنامه امروز", "📊 آمار"]
    ],
    resize_keyboard=True
)

user_mode = {}  # حالت چت


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 به مسیرنو AI خوش آمدی\n\n💬 برای صحبت با AI روی دکمه بزن",
        reply_markup=keyboard
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # 🤖 ورود به حالت چت
    if text == "💬 چت با AI":
        user_mode[user_id] = "chat"
        await update.message.reply_text("💬 حالا سوالت رو بپرس...")
        return

    # 💬 اگر در حالت چت هست
    if user_mode.get(user_id) == "chat":
        response = ask_ai(text)
        await update.message.reply_text(response)
        return

    # 📅 برنامه ساده
    if text == "📅 برنامه امروز":
        await update.message.reply_text("اول هدف رو انتخاب کن (نسخه کامل‌تر بعدی)")
        return

    # 📊 آمار ساده
    if text == "📊 آمار":
        await update.message.reply_text("📊 هنوز در نسخه 2.1 ساده هستیم")
        return

    await update.message.reply_text("از دکمه‌ها استفاده کن 👇")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("MasirNo Chat AI Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
