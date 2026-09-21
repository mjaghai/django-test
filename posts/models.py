from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class TransmissionType(models.TextChoices):
    MANUAL = "manual", "دنده‌ای"
    AUTOMATIC = "automatic", "اتوماتیک"


class FuelType(models.TextChoices):
    PETROL = "petrol", "بنزینی"
    DIESEL = "diesel", "دیزلی"
    HYBRID = "hybrid", "هیبریدی"
    ELECTRIC = "electric", "برقی"


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        allow_unicode=True,
        verbose_name="آدرس URL",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="نویسنده",
    )

    image = models.ImageField(upload_to="posts/%Y/%m/%d/", verbose_name="تصویر اصلی")
    description = models.CharField(
        max_length=300,
        verbose_name="توضیح کوتاه",
        help_text="برای نمایش در کارت‌ها و متا تگ‌ها استفاده می‌شه",
    )
    content = models.TextField(verbose_name="متن کامل")

    category = models.CharField(max_length=100, blank=True, verbose_name="دسته‌بندی")
    brand = models.CharField(max_length=100, blank=True, verbose_name="برند")
    model = models.CharField(max_length=100, blank=True, verbose_name="مدل")
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name="سال تولید")
    engine = models.CharField(max_length=100, blank=True, verbose_name="موتور")
    horsepower = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="قدرت (اسب‌بخار)"
    )
    transmission = models.CharField(
        max_length=20,
        choices=TransmissionType.choices,
        blank=True,
        verbose_name="گیربکس",
    )
    fuel_type = models.CharField(
        max_length=20, choices=FuelType.choices, blank=True, verbose_name="نوع سوخت"
    )
    price = models.PositiveBigIntegerField(
        null=True, blank=True, verbose_name="قیمت (تومان)"
    )

    is_published = models.BooleanField(default=True, verbose_name="منتشر شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        ordering = ["-created_at"]  # noqa: RUF012
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            # اگه اسلاگ تکراری باشه (دو پست هم‌عنوان)، یه شماره بهش اضافه می‌کنه
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
