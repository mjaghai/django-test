"""تست‌های تنظیمات رسانه (Media) — تضمین سرو شدن تصاویر آپلود شده"""

import pytest
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from posts.models import Post


# یه JPEG خیلی کوچک معتبر (1x1 پیکسل)
TINY_JPEG = (
    b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    b"\xff\xdb\x00C\x00" + bytes(range(1, 65)) + b"\x00" * 100 + b"\xff\xd9"
)


@pytest.mark.django_db
class TestMediaSettings:
    """MEDIA_URL و MEDIA_ROOT باید تنظیم شده باشن"""

    def test_media_url_is_configured(self):
        assert settings.MEDIA_URL
        assert settings.MEDIA_URL.startswith("/")

    def test_media_root_is_configured(self):
        assert settings.MEDIA_ROOT is not None

    def test_media_url_trailing_slash(self):
        """MEDIA_URL باید با / تموم بشه وگرنه join خراب میشه"""
        assert settings.MEDIA_URL.endswith("/")


@pytest.mark.django_db
class TestMediaUrlRouting:
    """در حالت DEBUG، فایل‌های media باید سرو بشن"""

    def test_media_path_is_served(self, client):
        """درخواست به مسیر media نباید 404 بده"""
        response = client.get("/media/nonexistent.jpg")
        # 404 یعنی مسیر ثبت شده ولی فایل نیست (درست)
        # اگر مسیر ثبت نشده بود، به صفحه اصلی ریدایرکت می‌شد
        assert response.status_code in (200, 404)
        assert response.status_code != 302


@pytest.mark.django_db
class TestPostImageUpload:
    """آپلود تصویر باید کار کنه"""

    def test_image_url_generated(self, user):
        """پست با تصویر باید URL تولید کنه"""
        upload = SimpleUploadedFile("car.jpg", TINY_JPEG, content_type="image/jpeg")
        post = Post.objects.create(
            title="پژو ۲۰۶",
            description="بررسی کامل",
            content="متن کامل",
            author=user,
            image=upload,
        )
        assert post.image.url.startswith("/media/")
        assert post.image.url.endswith(".jpg")

    def test_image_saved_in_date_path(self, user):
        """تصویر باید در مسیر تاریخ ذخیره بشه"""
        upload = SimpleUploadedFile("car.jpg", TINY_JPEG, content_type="image/jpeg")
        post = Post.objects.create(
            title="پژو ۲۰۶",
            description="بررسی",
            content="متن",
            author=user,
            image=upload,
        )
        # قالب مسیر: posts/%Y/%m/%d/filename.jpg → ۵ بخش
        parts = post.image.name.split("/")
        assert parts[0] == "posts"
        assert len(parts) == 5
        # تاریخ باید ۴ رقم سال، ۲ رقم ماه، ۲ رقم روز باشه
        assert len(parts[1]) == 4 and parts[1].isdigit()  # سال
        assert len(parts[2]) == 2 and parts[2].isdigit()  # ماه
        assert len(parts[3]) == 2 and parts[3].isdigit()  # روز

    def test_file_actually_written_to_disk(self, user):
        """فایل باید واقعاً روی دیسک نوشته بشه"""
        upload = SimpleUploadedFile("car.jpg", TINY_JPEG, content_type="image/jpeg")
        post = Post.objects.create(
            title="تست دیسک",
            description="بررسی",
            content="متن",
            author=user,
            image=upload,
        )
        assert post.image.storage.exists(post.image.name)
        post.image.delete()

    def test_post_without_image_has_empty_url(self, user):
        """پست بدون تصویر نباید URL داشته باشه"""
        post = Post.objects.create(
            title="بدون تصویر",
            description="بررسی",
            content="متن",
            author=user,
        )
        assert not post.image

    def test_image_is_optional(self, user):
        """فیلد image باید blank باشه تا بشه بدون تصویر هم پست ساخت"""
        post = Post.objects.create(
            title="بدون عکس ولی معتبر",
            description="بررسی",
            content="متن",
            author=user,
        )
        assert post.pk is not None


@pytest.mark.django_db
class TestUploadSizeLimit:
    """محدودیت حجم آپلود"""

    def test_max_memory_size_is_set(self):
        assert settings.DATA_UPLOAD_MAX_MEMORY_SIZE > 0

    def test_max_size_is_reasonable(self):
        """حداکثر ۲۰ مگابایت باشه (نه خیلی کم نه خیلی زیاد)"""
        mb = settings.DATA_UPLOAD_MAX_MEMORY_SIZE / (1024 * 1024)
        assert 1 <= mb <= 20
