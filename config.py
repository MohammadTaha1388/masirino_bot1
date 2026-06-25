# config.py

import os

# توکن ربات
BOT_TOKEN = os.getenv("BOT_TOKEN")

# حالت توسعه یا پروداکشن
DEBUG = True

# نام ربات
BOT_NAME = "MasirNo"

# پیام‌های ثابت
WELCOME_TEXT = "👋 به مسیرنو خوش آمدی! هدف خودت را انتخاب کن:"

SELECT_GOAL_TEXT = "🎯 یکی از اهداف زیر را انتخاب کن:"

DONE_TEXT = "🔥 آفرین! امروز کارت انجام شد"

FAIL_TEXT = "⚠️ مشکلی نیست، فردا دوباره شروع کن"