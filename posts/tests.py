import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from posts.models import FuelType, Post, TransmissionType


# ─── Post Model Unit Tests ───────────────────────────────────────


@pytest.mark.django_db
class TestPostStr:
    """__str__ باید عنوان پست رو برگردونه"""

    def test_returns_title(self, post):
        assert str(post) == "پست تستی"


@pytest.mark.django_db
class TestPostAutoSlug:
    """اسلاگ باید خودکار از عنوان ساخته بشه"""

    def test_slug_generated_from_title(self, post):
        assert post.slug == "پست-تستی"

    def test_slug_not_overwritten_when_explicit(self, db, user):
        post = Post.objects.create(
            title="عنوان دیگه",
            slug="slug-exist",
            description="desc",
            content="body",
            author=user,
        )
        assert post.slug == "slug-exist"

    def test_slug_unique_on_collision(self, db, user):
        """وقتی دو پست عنوان یکسان دارن، اسلاگ شماره می‌خوره"""
        Post.objects.create(
            title="مشترک",
            description="اول",
            content="متن اول",
            author=user,
        )
        post2 = Post.objects.create(
            title="مشترک",
            description="دوم",
            content="متن دوم",
            author=user,
        )
        assert post2.slug == "مشترک-2"

    def test_slug_third_collision(self, db, user):
        """سه پست با عنوان یکسان"""
        for i in range(3):
            Post.objects.create(
                title="مشترک",
                description=f"شماره {i}",
                content=f"متن {i}",
                author=user,
            )
        slugs = list(Post.objects.values_list("slug", flat=True))
        assert "مشترک" in slugs
        assert "مشترک-2" in slugs
        assert "مشترک-3" in slugs


@pytest.mark.django_db
class TestPostGetAbsoluteUrl:
    """get_absolute_url باید لینک درست رو برگردونه"""

    def test_returns_correct_url(self, post):
        expected = reverse("post_detail", kwargs={"slug": post.slug})
        assert post.get_absolute_url() == expected


@pytest.mark.django_db
class TestPostDefaultValues:
    """مقادیر پیش‌فرض باید درست باشن"""

    def test_is_published_default_true(self, post):
        assert post.is_published is True

    def test_created_at_auto_set(self, post):
        assert post.created_at is not None

    def test_updated_at_auto_set(self, post):
        assert post.updated_at is not None


@pytest.mark.django_db
class TestPostOrdering:
    """پست‌ها باید بر اساس تاریخ انتشار نزولی مرتب بشن"""

    def test_newest_first(self, db, user):
        p1 = Post.objects.create(
            title="اول",
            description="desc",
            content="body",
            author=user,
        )
        p2 = Post.objects.create(
            title="دوم",
            description="desc",
            content="body",
            author=user,
        )
        posts = list(Post.objects.all())
        assert posts[0].pk == p2.pk
        assert posts[1].pk == p1.pk


@pytest.mark.django_db
class TestPostChoices:
    """Choices باید درست تعریف شده باشن"""

    def test_transmission_choices(self):
        assert TransmissionType.MANUAL == "manual"
        assert TransmissionType.AUTOMATIC == "automatic"

    def test_fuel_type_choices(self):
        assert FuelType.PETROL == "petrol"
        assert FuelType.DIESEL == "diesel"
        assert FuelType.HYBRID == "hybrid"
        assert FuelType.ELECTRIC == "electric"


@pytest.mark.django_db
class TestPostOptionalFields:
    """فیلدهای اختیاری باید بدون مشکل ذخیره بشن"""

    def test_create_minimal_post(self, db, user):
        post = Post.objects.create(
            title="最小",
            description="desc",
            content="body",
            author=user,
        )
        assert post.brand == ""
        assert post.year is None
        assert post.price is None
        assert post.transmission == ""
        assert post.fuel_type == ""
