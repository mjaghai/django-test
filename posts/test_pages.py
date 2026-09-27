"""تست‌های صفحات جدید: اخبار، مقایسه، بررسی، جستجو"""

import pytest
from decimal import Decimal
from django.urls import reverse

from posts.models import Post


@pytest.fixture
def categorized_posts(db, user):
    """پست‌ها با دسته‌بندی‌های مختلف"""
    news = Post.objects.create(
        title="خبر رونمایی پژو",
        description="اخبار جدید",
        content="محتوای خبر",
        author=user,
        category="اخبار",
    )
    review = Post.objects.create(
        title="بررسی فولکس گلپ",
        description="بررسی کامل",
        content="محتوای بررسی",
        author=user,
        category="بررسی",
    )
    comp1 = Post.objects.create(
        title="پژو ۲۰۶ تیپ ۵",
        description="مشخصات",
        content="محتوا",
        author=user,
        category="مقایسه",
        brand="پژو",
        model="206",
        horsepower=110,
        acceleration_0_100=Decimal("9.5"),
        torque=150,
    )
    comp2 = Post.objects.create(
        title="پراید یورو ۴",
        description="مشخصات",
        content="محتوا",
        author=user,
        category="مقایسه",
        brand="سایپا",
        model="پراید",
        horsepower=65,
        acceleration_0_100=Decimal("14.2"),
        torque=113,
    )
    return {
        "news": news,
        "review": review,
        "comparison": [comp1, comp2],
    }


# ─── URL reversing ────────────────────────────────────────────────


class TestNewUrls:
    """مسیرها باید قابل reverse باشن"""

    def test_news_url(self):
        assert reverse("news") == "/posts/news/"

    def test_comparison_url(self):
        assert reverse("comparison") == "/posts/comparison/"

    def test_review_url(self):
        assert reverse("review") == "/posts/review/"

    def test_search_url(self):
        assert reverse("search") == "/posts/search/"


# ─── News page ───────────────────────────────────────────────────


@pytest.mark.django_db
class TestNewsPage:
    """صفحه اخبار"""

    def test_status_200(self, client, categorized_posts):
        response = client.get(reverse("news"))
        assert response.status_code == 200

    def test_uses_correct_template(self, client, categorized_posts):
        response = client.get(reverse("news"))
        assert "posts/news.html" in [t.name for t in response.templates]

    def test_shows_only_news_posts(self, client, categorized_posts):
        """فقط پست‌های دسته اخبار نمایش داده بشن"""
        response = client.get(reverse("news"))
        titles = [p.title for p in response.context["page_obj"]]
        assert "خبر رونمایی پژو" in titles
        assert "بررسی فولکس گلپ" not in titles

    def test_excludes_unpublished(self, client, user, categorized_posts):
        Post.objects.create(
            title="پیش‌نویس مخفی",
            description="دسکریپ",
            content="متن",
            author=user,
            category="اخبار",
            is_published=False,
        )
        response = client.get(reverse("news"))
        titles = [p.title for p in response.context["page_obj"]]
        assert "پیش‌نویس مخفی" not in titles

    def test_empty_state_shown(self, client):
        response = client.get(reverse("news"))
        assert response.status_code == 200
        assert b"\xd8\xa7\xd8\xae\xd8\xa8\xd8\xa7\xd8\xb1" in response.content


# ─── Review page ─────────────────────────────────────────────────


@pytest.mark.django_db
class TestReviewPage:
    """صفحه بررسی فنی"""

    def test_status_200(self, client, categorized_posts):
        assert client.get(reverse("review")).status_code == 200

    def test_uses_correct_template(self, client, categorized_posts):
        response = client.get(reverse("review"))
        assert "posts/review.html" in [t.name for t in response.templates]

    def test_shows_only_review_posts(self, client, categorized_posts):
        response = client.get(reverse("review"))
        titles = [p.title for p in response.context["page_obj"]]
        assert "بررسی فولکس گلپ" in titles
        assert "خبر رونمایی پژو" not in titles


# ─── Comparison page ─────────────────────────────────────────────


@pytest.mark.django_db
class TestComparisonPage:
    """صفحه مقایسه"""

    def test_status_200(self, client, categorized_posts):
        assert client.get(reverse("comparison")).status_code == 200

    def test_uses_correct_template(self, client, categorized_posts):
        response = client.get(reverse("comparison"))
        assert "posts/comparison.html" in [t.name for t in response.templates]

    def test_shows_only_comparison_posts(self, client, categorized_posts):
        response = client.get(reverse("comparison"))
        brands = {p.brand for p in response.context["posts"]}
        assert brands == {"پژو", "سایپا"}

    def test_renders_acceleration_column(self, client, categorized_posts):
        """ستون شتاب ۰-۱۰۰ باید رندر بشه"""
        response = client.get(reverse("comparison"))
        content = response.content.decode()
        assert "9.5" in content
        assert "14.2" in content

    def test_renders_torque_column(self, client, categorized_posts):
        """ستون گشتاور باید رندر بشه"""
        response = client.get(reverse("comparison"))
        content = response.content.decode()
        assert "150" in content
        assert "113" in content

    def test_empty_state_shown(self, client):
        response = client.get(reverse("comparison"))
        assert response.status_code == 200
        assert response.context["posts"].count() == 0


# ─── Search page ─────────────────────────────────────────────────


@pytest.mark.django_db
class TestSearchPage:
    """صفحه جستجو"""

    def test_status_200_without_query(self, client):
        assert client.get(reverse("search")).status_code == 200

    def test_uses_correct_template(self, client):
        response = client.get(reverse("search"))
        assert "posts/search.html" in [t.name for t in response.templates]

    def test_context_key_is_posts_not_results(self, client, categorized_posts):
        """کانتکست باید 'posts' باشه نه 'results' — باگ قبلی"""
        response = client.get(reverse("search"), {"q": "پژو"})
        assert "posts" in response.context
        assert "results" not in response.context

    def test_finds_by_title(self, client, categorized_posts):
        response = client.get(reverse("search"), {"q": "پژو"})
        titles = [p.title for p in response.context["posts"]]
        assert "خبر رونمایی پژو" in titles

    def test_finds_by_brand(self, client, categorized_posts):
        response = client.get(reverse("search"), {"q": "سایپا"})
        titles = [p.title for p in response.context["posts"]]
        assert "پراید یورو ۴" in titles

    def test_empty_query_returns_nothing(self, client, categorized_posts):
        response = client.get(reverse("search"), {"q": ""})
        assert response.context["posts"].count() == 0

    def test_no_match_returns_empty(self, client, categorized_posts):
        response = client.get(reverse("search"), {"q": "ماشین‌نیست"})
        assert response.context["posts"].count() == 0

    def test_query_reflected_in_context(self, client, categorized_posts):
        response = client.get(reverse("search"), {"q": "پژو"})
        assert response.context["query"] == "پژو"


# ─── Home page integration ───────────────────────────────────────


@pytest.mark.django_db
class TestHomeFeatureCardsLink:
    """کارت‌های صفحه اصلی باید لینک واقعی داشته باشن"""

    def test_news_link_present(self, client):
        response = client.get(reverse("home"))
        assert f'href="{reverse("news")}"' in response.content.decode()

    def test_comparison_link_present(self, client):
        response = client.get(reverse("home"))
        assert f'href="{reverse("comparison")}"' in response.content.decode()

    def test_review_link_present(self, client):
        response = client.get(reverse("home"))
        assert f'href="{reverse("review")}"' in response.content.decode()
