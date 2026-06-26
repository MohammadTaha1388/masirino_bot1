from openai import OpenAI
from groq import Groq

# OpenAI
openai_client = "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"

# Groq
groq_client = "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"


def build_prompt(goal, level, vip):
    return f"""
تو یک مربی حرفه‌ای هستی.

هدف: {goal}
سطح: {level}
VIP: {vip}

یک برنامه 3 بخشی بده:
1- کار اصلی
2- کار مکمل
3- چالش
"""


def ask_ai(goal, level, vip=False):

    prompt = build_prompt(goal, level, vip)

    # 🥇 OpenAI (اصلی)
    try:
        res = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "تو مربی انگیزشی هستی"},
                {"role": "user", "content": prompt}
            ]
        )
        return res.choices[0].message.content
    except:
        pass

    # 🥈 Groq (جایگزین سریع)
    try:
        res = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "تو یک مربی انگیزشی هستی"},
                {"role": "user", "content": prompt}
            ]
        )
        return res.choices[0].message.content
    except:
        pass

    # 🧱 fallback
    return """
📌 برنامه ساده:

1- کار اصلی: تمرین هدف
2- کار مکمل: مرور
3- چالش: یک قدم جلوتر
"""
