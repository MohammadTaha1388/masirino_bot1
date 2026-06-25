import random
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from db import add_user, get_user, update_streak, get_stats
from plans import PLANS
import config

TOKEN = "8342491323:AAFgmXGyHjNI086EucC1K5WDCKUHIMiuPG0"

user_last_plan = {}

goals_keyboard = ReplyKeyboardMarkup(
    [
        ["برنامه‌نویسی", "کنکور"],
        ["زبان انگلیسی", "تناسب اندام"],
        ["کسب درآمد"]
    ],
    resize_keyboard=True
)

action_keyboard = ReplyKeyboardMarkup(
    [
        ["🔥 انجام شد", "❌ انجام نشد"],
        ["📅 برنامه امروز", "📊 آمار"]
    ],
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(config.WELCOME_TEXT, reply_markup=goals_keyboard)


def get_random_plan(goal):
    return random.choice(PLANS[goal])


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # انتخاب هدف
    if text in PLANS:
        add_user(user_id, text)

        plan = get_random_plan(text)
        user_last_plan[user_id] = plan

        await update.message.reply_text(
            f"🎯 هدف: {text}\n\n📌 برنامه امروز:\n{plan}",
            reply_markup=action_keyboard
        )
        return

    # انجام شد
    if text == "🔥 انجام شد":
        update_streak(user_id, True)
        user = get_user(user_id)
        await update.message.reply_text(f"🔥 عالی! استریک تو: {user[2]} روز")
        return

    # انجام نشد
    if text == "❌ انجام نشد":
        update_streak(user_id, False)
        await update.message.reply_text(config.FAIL_TEXT)
        return

    # برنامه امروز
    if text == "📅 برنامه امروز":
        plan = user_last_plan.get(user_id, "ابتدا یک هدف انتخاب کن")
        await update.message.reply_text(f"📌 برنامه امروز:\n{plan}")
        return

    # آمار
    if text == "📊 آمار":
        total, avg = get_stats()
        await update.message.reply_text(
            f"📊 آمار مسیرنو:\n\n👥 کاربران: {total}\n🔥 میانگین استریک: {avg}"
        )
        return

    await update.message.reply_text("از دکمه‌ها استفاده کن 👇", reply_markup=goals_keyboard)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("MasirNo v1.2 running...")
    app.run_polling()


if __name__ == "__main__":
    main()
