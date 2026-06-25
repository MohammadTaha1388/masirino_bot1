import random

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from db import add_user, get_user, update_streak, add_xp, get_stats
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
        ["📅 برنامه امروز", "📊 آمار"],
        ["👤 پروفایل"]
    ],
    resize_keyboard=True
)


def make_plan(goal):
    p = PLANS[goal]
    return f"""📌 برنامه امروز:

1️⃣ کار اصلی:
{p['main']}

2️⃣ کار مکمل:
{p['support']}

3️⃣ چالش:
{p['challenge']}
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(config.WELCOME_TEXT, reply_markup=goals_keyboard)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # انتخاب هدف
    if text in PLANS:
        add_user(user_id, text)

        plan = make_plan(text)
        user_last_plan[user_id] = plan

        await update.message.reply_text(plan, reply_markup=action_keyboard)
        return

    # انجام شد
    if text == "🔥 انجام شد":
        update_streak(user_id, True)
        add_xp(user_id, 20)

        user = get_user(user_id)

        await update.message.reply_text(
            f"🔥 آفرین!\n\n🔥 استریک: {user[2]} روز\n⭐ XP: {user[3]}\n🏆 Level: {user[4]}"
        )
        return

    # انجام نشد
    if text == "❌ انجام نشد":
        update_streak(user_id, False)
        await update.message.reply_text("⚠️ استریک ریست شد")
        return

    # برنامه امروز
    if text == "📅 برنامه امروز":
        plan = user_last_plan.get(user_id, "اول هدف رو انتخاب کن")
        await update.message.reply_text(plan)
        return

    # آمار
    if text == "📊 آمار":
        total, avg = get_stats()
        await update.message.reply_text(
            f"📊 آمار:\n👥 کاربران: {total}\n🔥 میانگین استریک: {avg}"
        )
        return

    # پروفایل
    if text == "👤 پروفایل":
        user = get_user(user_id)

        if not user:
            await update.message.reply_text("اول هدف انتخاب کن")
            return

        await update.message.reply_text(
            f"""👤 پروفایل:

🎯 هدف: {user[1]}
🔥 استریک: {user[2]}
⭐ XP: {user[3]}
🏆 Level: {user[4]}
"""
        )
        return

    await update.message.reply_text("از دکمه‌ها استفاده کن 👇", reply_markup=goals_keyboard)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("MasirNo v1.4 running...")
    app.run_polling()


if __name__ == "__main__":
    main()
