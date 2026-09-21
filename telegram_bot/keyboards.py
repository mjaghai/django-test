"""Keyboard‌های inline ربات"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_keyboard():
    """دکمه‌های تایید/لغو"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ ذخیره و انتشار", callback_data="publish"),
                InlineKeyboardButton("📝 ذخیره پیش‌نویس", callback_data="draft"),
            ],
            [InlineKeyboardButton("❌ لغو", callback_data="cancel")],
        ]
    )


def skip_keyboard():
    """دکمه رد کردن فیلد اختیاری"""
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("⏭ رد کردن", callback_data="skip")]]
    )


def post_list_keyboard(posts):
    """لیست پست‌ها با دکمه مشاهده"""
    buttons = []
    for post in posts:
        buttons.append(
            [
                InlineKeyboardButton(
                    f"📄 {post.title[:30]}", url=post.get_absolute_url()
                )
            ]
        )
    return InlineKeyboardMarkup(buttons)
