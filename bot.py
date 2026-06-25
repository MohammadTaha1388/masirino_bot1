import random

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from db import add_user, get_user, update_streak, add_xp, get_stats
from plans import PLANS
from vip import is_vip
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


def generate_plan(goal, level, vip=False):
    base = random.choice(PLANS[goal])

    if vip:
        return f"""⭐ VIP PLAN:

{base}

🔥 تحلیل AI:
تو در مسیر حرفه‌ای رشد هستی، ادامه بده!
"""

    if level > 3:
        return f"""🚀 LEVEL UP PLAN:

{base}

💪 تو قوی‌تر شدی، چالش‌ها سخت‌تر شدن!
"""

    return base


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(config.WELCOME_TEXT, reply_markup=goals_keyboard)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # انتخاب هدف
    if text in PLANS:
        add_user(user_id, text)

        user = get_user(user_id)
        vip_status = is_vip(user_id)

        plan = generate_plan(text, user[4] if user else 1, vip_status)

        user_last_plan[user_id] = plan

        await update.message.reply_text(plan, reply_markup=action_keyboard)
        return

    # انجام شد
    if text == "🔥 انجام شد":
        vip_status = is_vip(user_id)

        update_streak(user_id, True)

        xp_gain = 40 if vip_status else 20
        add_xp(user_id, xp_gain)

        user = get_user(user_id)

        await update.message.reply_text(
            f"""🔥 عالی!

🔥 استریک: {user[2]}
⭐ XP: {user[3]}
🏆 Level: {user[4]}
💎 VIP: {'فعال' if vip_status else 'غیرفعال'}"""
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
        vip_status = is_vip(user_id)

        if not user:
            await update.message.reply_text("اول هدف انتخاب کن")
            return

        await update.message.reply_text(
            f"""👤 پروفایل:

🎯 هدف: {user[1]}
🔥 استریک: {user[2]}
⭐ XP: {user[3]}
🏆 Level: {user[4]}
💎 VIP: {'فعال' if vip_status else 'غیرفعال'}"""
        )
        return

    await update.message.reply_text("از دکمه‌ها استفاده کن 👇", reply_markup=goals_keyboard)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("MasirNo v1.5 running...")
    app.run_polling()


if __name__ == "__main__":
    main()
