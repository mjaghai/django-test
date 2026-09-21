"""هندلر ایجاد پست جدید — ConversationHandler"""

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from posts.models import Post

from ..keyboards import confirm_keyboard, skip_keyboard
from ..states import NewPostState


# ─── شروع مکالمه ────────────────────────────────────────────────


async def new_post_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع فرم ایجاد پست"""
    context.user_data["post_data"] = {}
    await update.message.reply_text(
        "📝 **پست جدید**\n\nعنوان پست رو وارد کن:",
        parse_mode="Markdown",
    )
    return NewPostState.TITLE


# ─── فیلدهای اصلی ───────────────────────────────────────────────


async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت عنوان"""
    context.user_data["post_data"]["title"] = update.message.text
    await update.message.reply_text(
        "توضیح کوتاه (حداکثر ۳۰۰ کاراکتر):", parse_mode="Markdown"
    )
    return NewPostState.DESCRIPTION


async def get_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت توضیح کوتاه"""
    text = update.message.text
    if len(text) > 300:
        await update.message.reply_text(
            f"⚠️ {len(text)} کاراکتر! حداکثر ۳۰۰ کاراکتر باشه.\nدوباره وارد کن:"
        )
        return NewPostState.DESCRIPTION

    context.user_data["post_data"]["description"] = text
    await update.message.reply_text(
        "متن کامل پست رو وارد کن:", parse_mode="Markdown"
    )
    return NewPostState.CONTENT


async def get_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت متن کامل"""
    context.user_data["post_data"]["content"] = update.message.text
    await update.message.reply_text(
        "🏷 **برند خودرو** (مثلاً پژو، تویوتا)\n"
        "یا دکمه رد کردن رو بزن:",
        parse_mode="Markdown",
        reply_markup=skip_keyboard(),
    )
    return NewPostState.BRAND


# ─── فیلدهای اختیاری ────────────────────────────────────────────


async def get_brand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت برند"""
    if update.callback_query:
        # رد کردن
        query = update.callback_query
        await query.answer()
        context.user_data["post_data"]["brand"] = ""
    else:
        context.user_data["post_data"]["brand"] = update.message.text

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🔢 **مدل خودرو** (مثلاً 206، کرولا)\nیا رد کردن:",
        parse_mode="Markdown",
        reply_markup=skip_keyboard(),
    )
    return NewPostState.MODEL


async def get_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت مدل"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        context.user_data["post_data"]["model"] = ""
    else:
        context.user_data["post_data"]["model"] = update.message.text

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="📅 **سال تولید** (مثلاً 1400)\nیا رد کردن:",
        parse_mode="Markdown",
        reply_markup=skip_keyboard(),
    )
    return NewPostState.YEAR


async def get_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت سال"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        context.user_data["post_data"]["year"] = None
    else:
        try:
            context.user_data["post_data"]["year"] = int(update.message.text)
        except ValueError:
            await update.message.reply_text("⚠️ فقط عدد وارد کن:")
            return NewPostState.YEAR

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🔧 **موتور** (مثلاً 1600cc)\nیا رد کردن:",
        parse_mode="Markdown",
        reply_markup=skip_keyboard(),
    )
    return NewPostState.ENGINE


async def get_engine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت موتور"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        context.user_data["post_data"]["engine"] = ""
    else:
        context.user_data["post_data"]["engine"] = update.message.text

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🐎 **قدرت (اسب‌بخار)** (مثلاً 110)\nیا رد کردن:",
        parse_mode="Markdown",
        reply_markup=skip_keyboard(),
    )
    return NewPostState.HORSEPOWER


async def get_horsepower(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت قدرت"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        context.user_data["post_data"]["horsepower"] = None
    else:
        try:
            context.user_data["post_data"]["horsepower"] = int(update.message.text)
        except ValueError:
            await update.message.reply_text("⚠️ فقط عدد وارد کن:")
            return NewPostState.HORSEPOWER

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="💰 **قیمت (تومان)** (مثلاً 500000000)\nیا رد کردن:",
        parse_mode="Markdown",
        reply_markup=skip_keyboard(),
    )
    return NewPostState.PRICE


async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت قیمت"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        context.user_data["post_data"]["price"] = None
    else:
        try:
            context.user_data["post_data"]["price"] = int(
                update.message.text.replace(",", "").replace("،", "")
            )
        except ValueError:
            await update.message.reply_text("⚠️ فقط عدد وارد کن:")
            return NewPostState.PRICE

    # ─── نمایش خلاصه و درخواست تایید ───
    data = context.user_data["post_data"]
    summary = (
        "📋 **خلاصه پست:**\n\n"
        f"**عنوان:** {data['title']}\n"
        f"**توضیح:** {data['description'][:50]}...\n"
        f"**برند:** {data.get('brand', '') or '—'}\n"
        f"**مدل:** {data.get('model', '') or '—'}\n"
        f"**سال:** {data.get('year') or '—'}\n"
        f"**موتور:** {data.get('engine', '') or '—'}\n"
        f"**قدرت:** {data.get('horsepower') or '—'} HP\n"
        f"**قیمت:** {data.get('price') or '—'} تومان\n\n"
        "ذخیره بشه؟"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=summary,
        parse_mode="Markdown",
        reply_markup=confirm_keyboard(),
    )
    return NewPostState.CONFIRM


# ─── تایید و ذخیره ──────────────────────────────────────────────


async def confirm_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ذخیره پست"""
    query = update.callback_query
    await query.answer()

    data = context.user_data["post_data"]

    if query.data == "cancel":
        await query.edit_message_text("❌ لغو شد.")
        context.user_data.clear()
        return ConversationHandler.END

    # ایجاد پست
    post = Post.objects.create(
        title=data["title"],
        description=data["description"],
        content=data["content"],
        brand=data.get("brand", ""),
        model=data.get("model", ""),
        year=data.get("year"),
        engine=data.get("engine", ""),
        horsepower=data.get("horsepower"),
        price=data.get("price"),
        is_published=(query.data == "publish"),
    )

    status = "منتشر شده ✅" if post.is_published else "پیش‌نویس 📝"
    await query.edit_message_text(
        f"✅ **پست ذخیره شد!**\n\n"
        f"**{post.title}**\n"
        f"وضعیت: {status}\n"
        f"اسلگ: `{post.slug}`\n"
        f"لینک: {post.get_absolute_url()}",
        parse_mode="Markdown",
    )

    context.user_data.clear()
    return ConversationHandler.END


# ─── لغو ────────────────────────────────────────────────────────


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لغو عملیات"""
    context.user_data.clear()
    await update.message.reply_text("❌ عملیات لغو شد.")
    return ConversationHandler.END


# ─── ConversationHandler ─────────────────────────────────────────


def get_new_post_handler():
    """برگرداندن ConversationHandler"""
    return ConversationHandler(
        entry_points=[
            CommandHandler("new_post", new_post_start),
        ],
        states={
            NewPostState.TITLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_title),
            ],
            NewPostState.DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_description),
            ],
            NewPostState.CONTENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_content),
            ],
            NewPostState.BRAND: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_brand),
                CallbackQueryHandler(get_brand, pattern="^skip$"),
            ],
            NewPostState.MODEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_model),
                CallbackQueryHandler(get_model, pattern="^skip$"),
            ],
            NewPostState.YEAR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_year),
                CallbackQueryHandler(get_year, pattern="^skip$"),
            ],
            NewPostState.ENGINE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_engine),
                CallbackQueryHandler(get_engine, pattern="^skip$"),
            ],
            NewPostState.HORSEPOWER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_horsepower),
                CallbackQueryHandler(get_horsepower, pattern="^skip$"),
            ],
            NewPostState.PRICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_price),
                CallbackQueryHandler(get_price, pattern="^skip$"),
            ],
            NewPostState.CONFIRM: [
                CallbackQueryHandler(confirm_save, pattern="^(publish|draft|cancel)$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
