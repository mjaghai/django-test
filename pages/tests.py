import pytest
from django.test import Client
from django.urls import reverse


# ─── Page View Tests ──────────────────────────────────────────────


@pytest.mark.django_db
class TestHomePage:
    """صفحه اصلی باید 200 برگردونه"""

    def test_home_status_code(self, client):
        response = client.get(reverse("home"))
        assert response.status_code == 200

    def test_home_uses_correct_template(self, client):
        response = client.get(reverse("home"))
        assert "pages/home.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestAboutPage:
    """صفحه درباره ما باید 200 برگردونه"""

    def test_about_status_code(self, client):
        response = client.get(reverse("about"))
        assert response.status_code == 200

    def test_about_uses_correct_template(self, client):
        response = client.get(reverse("about"))
        assert "pages/about.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestPostListPage:
    """لیست پست‌ها باید 200 برگردونه"""

    def test_post_list_status_code(self, client):
        response = client.get(reverse("post_list"))
        assert response.status_code == 200

    def test_post_list_uses_correct_template(self, client):
        response = client.get(reverse("post_list"))
        assert "posts/posts.html" in [t.name for t in response.templates]
