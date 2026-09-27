"""تست‌های فیلدهای عملکردی خودرو — شتاب ۰-۱۰۰ و گشتاور"""

import pytest
from decimal import Decimal

from posts.models import Post


@pytest.mark.django_db
class TestAccelerationField:
    """فیلد شتاب ۰ تا ۱۰۰ کیلومتر"""

    def test_field_exists(self):
        assert hasattr(Post, "acceleration_0_100")

    def test_is_decimal_type(self):
        """باید اعشاری باشه چون زمان‌هایی مثل ۴.۷ ثانیه داریم"""
        from django.db import models

        field = Post._meta.get_field("acceleration_0_100")
        assert isinstance(field, models.DecimalField)

    def test_nullable_and_blank(self):
        """باید اختیاری باشه تا پست‌های قدیمی نشکنن"""
        field = Post._meta.get_field("acceleration_0_100")
        assert field.null is True
        assert field.blank is True

    def test_default_is_none(self, post):
        assert post.acceleration_0_100 is None

    def test_can_store_decimal(self, user):
        p = Post.objects.create(
            title="F40",
            description="تست",
            content="متن",
            author=user,
            acceleration_0_100=Decimal("3.4"),
        )
        p.refresh_from_db()
        assert p.acceleration_0_100 == Decimal("3.4")

    def test_preserves_decimal_precision(self, user):
        """عدد اعشاری نباید گرد بشه"""
        p = Post.objects.create(
            title="F40 دقت",
            description="تست",
            content="متن",
            author=user,
            acceleration_0_100=Decimal("4.7"),
        )
        p.refresh_from_db()
        assert p.acceleration_0_100 == Decimal("4.7")

    def test_str_representation(self, user):
        p = Post.objects.create(
            title="F40 نمایش",
            description="تست",
            content="متن",
            author=user,
            acceleration_0_100=Decimal("3.4"),
        )
        assert str(p.acceleration_0_100) == "3.4"


@pytest.mark.django_db
class TestTorqueField:
    """فیلد گشتاور موتور"""

    def test_field_exists(self):
        assert hasattr(Post, "torque")

    def test_is_integer_type(self, user):
        """گشتاور معمولاً عدد صحیحه (۲۰۰ Nm)"""
        from django.db import models

        field = Post._meta.get_field("torque")
        assert isinstance(field, models.IntegerField)

    def test_nullable_and_blank(self):
        field = Post._meta.get_field("torque")
        assert field.null is True
        assert field.blank is True

    def test_default_is_none(self, post):
        assert post.torque is None

    def test_can_store_integer(self, user):
        p = Post.objects.create(
            title="F40 گشتاور",
            description="تست",
            content="متن",
            author=user,
            torque=760,
        )
        p.refresh_from_db()
        assert p.torque == 760

    def test_rejects_negative(self, user):
        """گشتاور منفی معنی نداره"""
        from django.core.exceptions import ValidationError

        p = Post(
            title="منفی",
            description="تست",
            content="متن",
            author=user,
            torque=-100,
        )
        with pytest.raises(ValidationError):
            p.full_clean()


@pytest.mark.django_db
class TestSpecFieldsOrdering:
    """ترتیب فیلدها در مدل"""

    def test_acceleration_comes_after_horsepower(self):
        """فیلد شتاب باید بعد از قدرت باشه (ترتیب منطقی)"""
        names = [f.name for f in Post._meta.fields]
        assert names.index("acceleration_0_100") > names.index("horsepower")

    def test_torque_comes_after_acceleration(self):
        names = [f.name for f in Post._meta.fields]
        assert names.index("torque") > names.index("acceleration_0_100")
