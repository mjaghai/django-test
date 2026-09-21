import pytest
from django.contrib.auth.models import User

from accounts.forms import RegisterForm


# ─── RegisterForm Unit Tests ─────────────────────────────────────


@pytest.mark.django_db
class TestRegisterFormValid:
    """فرم ثبت‌نام با داده‌های معتبر باید کار کنه"""

    def test_valid_data_creates_user(self):
        form = RegisterForm(
            data={
                "username": "newuser",
                "email": "new@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )
        assert form.is_valid() is True
        user = form.save()
        assert user.username == "newuser"
        assert user.email == "new@example.com"

    def test_email_saved_correctly(self):
        form = RegisterForm(
            data={
                "username": "emailtest",
                "email": "saved@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )
        user = form.save()
        assert user.email == "saved@example.com"


@pytest.mark.django_db
class TestRegisterFormInvalid:
    """فرم با داده‌های نامعتبر باید reject بشه"""

    def test_missing_email(self):
        form = RegisterForm(
            data={
                "username": "noemail",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )
        assert form.is_valid() is False
        assert "email" in form.errors

    def test_password_mismatch(self):
        form = RegisterForm(
            data={
                "username": "mismatch",
                "email": "m@example.com",
                "password1": "StrongPass123!",
                "password2": "WrongPass456!",
            }
        )
        assert form.is_valid() is False
        assert "password2" in form.errors

    def test_missing_username(self):
        form = RegisterForm(
            data={
                "email": "noun@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )
        assert form.is_valid() is False
        assert "username" in form.errors


@pytest.mark.django_db
class TestRegisterFormDuplicateUsername:
    """یوزرنیم تکراری باید reject بشه"""

    def test_duplicate_username_rejected(self):
        User.objects.create_user(
            username="taken", email="old@example.com", password="pass123!"
        )
        form = RegisterForm(
            data={
                "username": "taken",
                "email": "new@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )
        assert form.is_valid() is False
        assert "username" in form.errors
