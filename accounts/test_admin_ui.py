"""تست‌های تمپلیت ادمین و حالت روشن/تاریک"""

import re

import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admintest", email="admin@test.com", password="TestPass123!"
    )


@pytest.mark.django_db
class TestAdminBranding:
    """برندینگ ادمین"""

    def test_admin_index_status_200(self, client, admin_user):
        client.force_login(admin_user)
        response = client.get(reverse("admin:index"))
        assert response.status_code == 200

    def test_admin_page_has_title(self, client, admin_user):
        client.force_login(admin_user)
        response = client.get(reverse("admin:index"))
        assert "خودرومگ" in response.content.decode()

    def test_admin_loads_custom_css(self, client, admin_user):
        client.force_login(admin_user)
        response = client.get(reverse("admin:index"))
        assert "admin.css" in response.content.decode()

    def test_admin_loads_custom_js(self, client, admin_user):
        client.force_login(admin_user)
        response = client.get(reverse("admin:index"))
        assert "admin-theme.js" in response.content.decode()


@pytest.mark.django_db
class TestThemeToggle:
    """دکمه تغییر حالت روشن/تاریک"""

    def test_toggle_button_present(self, client, admin_user):
        client.force_login(admin_user)
        content = client.get(reverse("admin:index")).content.decode()
        assert 'id="themeToggle"' in content

    def test_toggle_has_accessible_label(self, client, admin_user):
        client.force_login(admin_user)
        content = client.get(reverse("admin:index")).content.decode()
        # دکمه باید aria-label داشته باشه برای صفحه‌خوان‌ها
        assert re.search(r'id="themeToggle"[^>]*aria-label', content)

    def test_toggle_is_a_button_element(self, client, admin_user):
        client.force_login(admin_user)
        content = client.get(reverse("admin:index")).content.decode()
        assert "<button" in content and 'id="themeToggle"' in content

    def test_no_flash_script_present(self, client, admin_user):
        """اسکریپت ضد-flash باید قبل از رندر اجرا بشه"""
        client.force_login(admin_user)
        content = client.get(reverse("admin:index")).content.decode()
        # جلوگیری از پرش رنگ (FOUC) — قبل از </head>
        assert "themeFlash" in content or "no-flash" in content


@pytest.mark.django_db
class TestNoChineseInAdmin:
    """نباید کاراکتر چینی در ادمین باشه"""

    def test_post_changelist_has_no_chinese(self, client, admin_user):
        from posts.models import Post

        Post.objects.create(
            title="Test", description="d", content="c", author=admin_user
        )
        client.force_login(admin_user)
        content = client.get(reverse("admin:posts_post_changelist")).content.decode()
        # هیچ کاراکتر CJK نباید باشه
        assert not re.search(r"[\u4e00-\u9fff]", content)

    def test_post_add_page_has_no_chinese(self, client, admin_user):
        client.force_login(admin_user)
        content = client.get(reverse("admin:posts_post_add")).content.decode()
        assert not re.search(r"[\u4e00-\u9fff]", content)

    def test_fieldset_names_are_ascii(self):
        """اسم فیلدست‌ها باید انگلیسی باشه"""
        from posts.admin import PostAdmin

        names = [fs[0] for fs in PostAdmin.fieldsets]
        for name in names:
            assert not re.search(r"[\u4e00-\u9fff]", name)

    def test_new_spec_fields_in_admin(self):
        """فیلدهای جدید باید در ادمین قابل ویرایش باشن"""
        from posts.admin import PostAdmin

        spec_fields = PostAdmin.fieldsets[2][1]["fields"]
        assert "acceleration_0_100" in spec_fields
        assert "torque" in spec_fields


@pytest.mark.django_db
class TestThemeColorsInCss:
    """CSS باید متغیرهای هر دو حالت رو داشته باشه"""

    @pytest.fixture
    def css_content(self):
        from pathlib import Path

        # test file is at <root>/accounts/test_admin_ui.py
        base = Path(__file__).resolve().parent.parent
        css_file = base / "static" / "css" / "admin.css"
        return css_file.read_text(encoding="utf-8")

    def test_has_light_theme_block(self, css_content):
        assert "data-theme='light'" in css_content

    def test_has_dark_theme_block(self, css_content):
        assert "data-theme='dark'" in css_content

    def test_uses_prefers_color_scheme(self, css_content):
        """اگه سیستم‌عامل حالت روشن/تاریک داشته باشه، رعایت بشه"""
        assert "prefers-color-scheme" in css_content

    def test_amber_accent_defined(self, css_content):
        assert "--admin-amber" in css_content

    def test_has_transition_property(self, css_content):
        """تغییر حالت باید نرم باشه نه ناگهانی"""
        assert "transition" in css_content
