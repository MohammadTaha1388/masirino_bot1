import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from db import add_user, get_user, update_streak, get_stats

TOKEN = os.getenv("BOT_TOKEN")

goals = [
    ["برنامه‌نویسی", "کنکور"],
    ["زبان انگلیسی", "تناسب اندام"],
    ["کسب درآمد"]
]

plans = {
    "برنامه‌نویسی": "۱ ساعت تمرین پایتون + حل 3 تمرین",
    "کنکور": "۲ ساعت مطالعه + مرور تست",
    "زبان انگلیسی": "۲۰ لغت + ۱۰ دقیقه listening",
    "تناسب اندام": "۳۰ دقیقه ورزش",
    "کسب درآمد": "بررسی یک ایده جدید"
}

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(goals, resize_keyboard=True)
    await update.message.reply_text("👋 هدف خودت رو انتخاب کن:", reply_markup=keyboard)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if text in plans:
        add_user(user_id, text)
        user_state[user_id] = text

        keyboard = ReplyKeyboardMarkup([["امروز انجام شد ✅", "انجام نشد ❌"]], resize_keyboard=True)

        await update.message.reply_text(
            f"🎯 هدف: {text}\n\n📌 برنامه امروز:\n{plans[text]}",
            reply_markup=keyboard
        )
        return

    if text == "امروز انجام شد ✅":
        update_streak(user_id, True)
        user = get_user(user_id)
        await update.message.reply_text(f"🔥 آفرین! استریک تو: {user[2]} روز")
        return

    if text == "انجام نشد ❌":
        update_streak(user_id, False)
        await update.message.reply_text("⚠️ استریک ریست شد. فردا دوباره شروع کن!")
        return

    await update.message.reply_text("لطفاً از دکمه‌ها استفاده کن.")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total, avg = get_stats()
    await update.message.reply_text(
        f"📊 آمار مسیرنو:\n\n👥 کاربران: {total}\n🔥 میانگین استریک: {avg}"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Masirno v1.1 is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
