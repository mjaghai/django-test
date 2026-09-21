"""Entry point برای ربات تلگرام ادمین"""

import os
import sys
from pathlib import Path

# اضافه کردن مسیر پروژه به sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# لود .env
from dotenv import load_dotenv

load_dotenv(BASE_DIR / ".env")

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rome.settings")
django.setup()

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
)

from handlers import start, help_command
from handlers.list_posts import list_posts
from handlers.new_post import get_new_post_handler


def main():
    """راه‌اندازی ربات"""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not token:
        print("❌ متغیر TELEGRAM_BOT_TOKEN تنظیم نشده!")
        print("   فایل .env رو بساز و TELEGRAM_BOT_TOKEN رو تنظیم کن.")
        return

    # ساخت application
    app = ApplicationBuilder().token(token).build()

    # ثبت هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("list", list_posts))
    app.add_handler(get_new_post_handler())

    # شروع polling
    print("🤖 ربات خودرومگ در حال اجراست... (Ctrl+C برای توقف)")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
