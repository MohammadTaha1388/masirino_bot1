from openai import OpenAI
import google.generativeai as genai
import config

openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

genai.configure(api_key=config.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


def ask_ai(prompt):

    system_prompt = """
تو یک مربی انگیزشی حرفه‌ای هستی.
کوتاه، ساده، کاربردی و قابل اجرا جواب بده.
"""

    # OpenAI
    try:
        res = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return res.choices[0].message.content
    except:
        pass

    # Gemini
    try:
        res = gemini_model.generate_content(prompt)
        return res.text
    except:
        pass

    return "⚠️ الان سیستم AI در دسترس نیست"
