"""هندلر لیست پست‌ها"""

from telegram import Update
from telegram.ext import ContextTypes

from posts.models import Post

from ..keyboards import post_list_keyboard


async def list_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش ۵ پست آخر"""
    posts = Post.objects.all()[:5]

    if not posts:
        await update.message.reply_text("📭 هنوز پستی نداری.")
        return

    text = "📄 **آخرین پست‌ها:**\n\n"
    for i, post in enumerate(posts, 1):
        status = "✅" if post.is_published else "📝"
        text += f"{i}. {status} **{post.title}**\n"

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=post_list_keyboard(posts),
    )
