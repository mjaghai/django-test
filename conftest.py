import pytest
from django.contrib.auth.models import User
from posts.models import Post


@pytest.fixture
def user(db):
    """یوزر ساده برای تست‌ها"""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def post(db, user):
    """یه پست ساده برای تست‌ها"""
    return Post.objects.create(
        title="پست تستی",
        description="توضیحات کوتاه پست",
        content="متن کامل پست تستی",
        author=user,
        brand="پژو",
        model="206",
        year=1400,
        engine="1600cc",
        horsepower=110,
        transmission="manual",
        fuel_type="petrol",
        price=500_000_000,
    )


# ─── Override DB برای تست (SQLite به جای PostgreSQL) ───
@pytest.fixture(scope="session")
def django_settings_override():
    return {
        "DATABASES": {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        }
    }
