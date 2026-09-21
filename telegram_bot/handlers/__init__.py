"""هندلرهای شروع و راهنما"""

from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    await update.message.reply_text(
        "🚗 **خودرومگ — پنل مدیریت**\n\n"
        "دستورات:\n"
        "• `/new_post` — ایجاد پست جدید\n"
        "• `/list` — لیست پست‌ها\n"
        "• `/cancel` — لغو عملیات جاری\n",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /help"""
    await start(update, context)
