"""تست‌های ویوی احراز هویت"""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
class TestLogoutView:
    """خروج باید سشن رو پاک کنه"""

    def test_logout_url_exists(self):
        """مسیر logout باید در URL conf ثبت شده باشه"""
        assert reverse("logout") == "/accounts/logout"

    def test_logout_with_post_logs_user_out(self, client, user):
        """POST به logout باید کاربر رو از سشن خارج کنه"""
        client.force_login(user)
        assert client.session.get("_auth_user_id") == str(user.pk)

        response = client.post(reverse("logout"))

        assert response.status_code == 302
        assert "_auth_user_id" not in client.session

    def test_logout_rejects_get(self, client, user):
        """خروج نباید با GET کار کنه (فقط POST)"""
        client.force_login(user)
        response = client.get(reverse("logout"))
        assert response.status_code == 405
        assert client.session.get("_auth_user_id") == str(user.pk)

    def test_base_template_logout_form_points_to_url(self, client, user):
        """فرم خروج توی base.html باید به مسیر logout پست کنه"""
        client.force_login(user)
        response = client.get(reverse("home"))
        html = response.content.decode()

        assert f'action="{reverse("logout")}"' in html
        assert 'action=""' not in html


@pytest.mark.django_db
class TestLoginView:
    """ورود باید کار کنه"""

    def test_login_url_exists(self):
        assert reverse("login") == "/accounts/login"

    def test_login_redirects_authenticated_user(self, client, user):
        """کاربر لاگین‌این نباید صفحه ورود رو ببینه"""
        client.force_login(user)
        response = client.get(reverse("login"))
        assert response.status_code == 302
        assert response.url == reverse("home")

    def test_login_with_valid_credentials(self, client, user):
        """ورود با اطلاعات درست باید کار کنه"""
        response = client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
        )
        assert response.status_code == 302
        assert client.session.get("_auth_user_id") == str(user.pk)

    def test_login_with_wrong_password(self, client, user):
        """ورود با رمز اشتباه نباید کار کنه"""
        response = client.post(
            reverse("login"),
            {"username": "testuser", "password": "wrongpass"},
        )
        assert response.status_code == 200
        assert "_auth_user_id" not in client.session

    def test_login_without_remember_uses_browser_session(self, client, user):
        """بدون تیک مرا به خاطر بسپار، سشن باید با بستن مرورگر پاک بشه

        نکته: get_expiry_age() برای مقدار 0 (که falsy هست) cookie age
        پیش‌فرض رو برمی‌گردونه، پس باید _session_expiry رو چک کنیم.
        """
        client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
        )
        assert client.session.get("_session_expiry") == 0

    def test_login_with_remember_keeps_session(self, client, user):
        """با تیک مرا به خاطر بسپار، سشن باید دائمی بشه"""
        client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpass123",
                "remember": "on",
            },
        )
        assert client.session.get("_session_expiry") != 0
        assert client.session.get_expiry_age() > 0
