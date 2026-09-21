# ربات تلگرام ادمین — خودرومگ

## Problem Statement
چطور بتونیم از داخل تلگرام، بدون نیاز به مرورگر، پست‌های خودرومگ رو مدیریت کنیم؟

## Recommended Direction
ربات تلگرامی با **ConversationHandler** و **Inline Keyboard** که یه فرم سوال-جوابی برای ایجاد پست جدید ارائه بده. ادمین با دستور `/new_post` شروع می‌کنه و مرحله به مرحله فیلدها رو پر می‌کنه.

### Flow اصلی:
```
/new_post
  → 📝 عنوان: [input]
  → 📝 توضیح کوتاه: [input]
  → 📝 متن کامل: [input]
  → 📝 برند: [input] (اختیاری)
  → 📝 مدل: [input] (اختیاری)
  → 📝 سال: [input] (اختیاری)
  → 📝 موتور: [input] (اختیاری)
  → 📝 قدرت: [input] (اختیاری)
  → 📝 قیمت: [input] (اختیاری)
  → [ذخیره و انتشار] [ذخیره و پیش‌نویس] [لغو]
```

### دستورات:
| دستور | عملکرد |
|-------|--------|
| `/start` | خوش‌آمدگویی + راهنما |
| `/new_post` | شروع فرم ایجاد پست |
| `/list` | لیست ۵ پست آخر با دکمه ویرایش |
| `/cancel` | لغو عملیات جاری |

## Key Assumptions to Validate
- [ ] `python-telegram-bot` با Django ORM هماهنگه (تست: import و اجرای ساده)
- [ ] ادمین فقط یک نفره (Telegram user_id ثابت در settings)
- [ ] فیلد `image` در MVP رد بشه (از وب سایت آپلود بشه)
- [ ] اتصال به Telegram API از ایران بدون proxy کار می‌کنه

## MVP Scope

### ✅ In scope:
- ایجاد پست جدید از طریق تلگرام (ConversationHandler)
- فیلدهای اصلی: title, description, content
- فیلدهای اختیاری: brand, model, year, engine, horsepower, price
- دستور `/list` برای مشاهده پست‌ها
- ذخیره در دیتابیس با `is_published=False` (پیش‌نویس)
- انتشار با دکمه inline
- اعتبارسنجی ساده (عنوان الزامی)

### ❌ Out of scope (MVP):
- آپلود تصویر از تلگرام (نیاز به file handling پیچیده)
- ویرایش پست موجود
- حذف پست
- مدیریت چند ادمین
- ارسال خودکار به کانال
- سیستم نظرات

## Tech Stack
```
python-telegram-bot >= 21.0  (async, modern API)
Django 6.1 + PostgreSQL
ConversationHandler  (state machine)
InlineKeyboardMarkup  (دکمه‌ها)
```

## File Structure
```
telegram_bot/
├── __init__.py
├── bot.py              # Entry point, polling
├── handlers/
│   ├── __init__.py
│   ├── start.py        # /start, /help
│   ├── new_post.py     # /new_post conversation
│   └── list_posts.py   # /list
├── keyboards.py        # Inline keyboards
├── states.py           # Conversation states
└── permissions.py      # Admin user_id check
```

## Not Doing (and Why)
- **آپلود تصویر** — نیاز به file download + media group handling. MVP فقط عنوان و متن مهمه
- **ویرایش/حذف** — نیاز به inline query یا callback complex. بعداً اضافه بشه
- **چند ادمین** — فعلاً یه نفره. permission system اضافه کاریه
- **Webhook** — نیاز به سرور عمومی. polling برای MVP کافیه
- **Proxy** — فعلاً مستقیم. اگه وصل نشد proxy اضافه می‌کنیم

## Implementation Steps
1. نصب `python-telegram-bot`
2. ساخت `telegram_bot/` app با ساختار بالا
3. پیاده‌سازی `start` handler
4. پیاده‌سازی `new_post` ConversationHandler
5. پیاده‌سازی `list` handler
6. تست محلی با polling
7. اضافه کردن به `manage.py` یا اسکریپت جداگانه

## Open Questions
- آیا `image` فیلد الزامیه؟ (فعلاً `blank=True` نیست — باید migrate کنیم یا در bot رد کنیم)
- آیا django-settings برای `TELEGRAM_BOTT_TOKEN` و `TELEGRAM_ADMIN_ID` کافیه؟
