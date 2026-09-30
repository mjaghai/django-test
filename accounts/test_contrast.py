"""بررسی کنتراست رنگ‌ها در هر دو تم (WCAG AA)"""


def srgb_to_linear(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color):
    """روشنایی نسبی طبق WCAG"""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return (
        0.2126 * srgb_to_linear(r)
        + 0.7152 * srgb_to_linear(g)
        + 0.0722 * srgb_to_linear(b)
    )


def contrast_ratio(fg, bg):
    """نسبت کنتراست بین دو رنگ (۱ تا ۲۱)"""
    l1, l2 = luminance(fg), luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ─── پالت‌ها ─────────────────────────────────────────────────────

DARK = {
    "bg": "#121215",
    "surface": "#19191d",
    "surface2": "#232328",
    "text": "#f2f1ec",
    "muted": "#a5a4ad",
    "dim": "#6f6e78",
    "amber": "#ff8c1a",
    "red": "#f4707c",
    "green": "#4ade80",
}

LIGHT = {
    "bg": "#f7f7f5",
    "surface": "#ffffff",
    "surface2": "#f1f1ee",
    "text": "#1a1a1c",
    "muted": "#5a5a62",
    "dim": "#8a8a92",
    "amber": "#b35900",
    "red": "#c6202c",
    "green": "#157f3d",
}


class TestDarkThemeContrast:
    """کنتراست تم تاریک"""

    def test_body_text_on_background(self):
        r = contrast_ratio(DARK["text"], DARK["bg"])
        assert r >= 4.5, f"body text contrast {r:.2f}:1"

    def test_body_text_on_surface(self):
        r = contrast_ratio(DARK["text"], DARK["surface"])
        assert r >= 4.5, f"text on surface {r:.2f}:1"

    def test_body_text_on_surface2(self):
        r = contrast_ratio(DARK["text"], DARK["surface2"])
        assert r >= 4.5, f"text on surface2 {r:.2f}:1"

    def test_muted_text_on_surface(self):
        r = contrast_ratio(DARK["muted"], DARK["surface"])
        assert r >= 4.5, f"muted text {r:.2f}:1"

    def test_amber_on_surface(self):
        r = contrast_ratio(DARK["amber"], DARK["surface"])
        assert r >= 4.5, f"amber accent {r:.2f}:1"

    def test_amber_contrast_color_on_amber(self):
        """متن روی دکمه نارنجی"""
        r = contrast_ratio("#16110a", DARK["amber"])
        assert r >= 4.5, f"text on amber button {r:.2f}:1"

    def test_error_red_on_surface(self):
        r = contrast_ratio(DARK["red"], DARK["surface"])
        assert r >= 4.5, f"error text {r:.2f}:1"

    def test_success_green_on_surface(self):
        r = contrast_ratio(DARK["green"], DARK["surface"])
        assert r >= 4.5, f"success text {r:.2f}:1"

    def test_dim_text_is_large_text_only(self):
        """متن dim فقط برای متن‌های بزرگ/کم‌اهمیت"""
        r = contrast_ratio(DARK["dim"], DARK["surface"])
        assert r >= 3.0, f"dim text {r:.2f}:1 (large text minimum)"


class TestLightThemeContrast:
    """کنتراست تم روشن"""

    def test_body_text_on_background(self):
        r = contrast_ratio(LIGHT["text"], LIGHT["bg"])
        assert r >= 4.5, f"body text contrast {r:.2f}:1"

    def test_body_text_on_surface(self):
        r = contrast_ratio(LIGHT["text"], LIGHT["surface"])
        assert r >= 4.5, f"text on surface {r:.2f}:1"

    def test_body_text_on_surface2(self):
        r = contrast_ratio(LIGHT["text"], LIGHT["surface2"])
        assert r >= 4.5, f"text on surface2 {r:.2f}:1"

    def test_muted_text_on_surface(self):
        r = contrast_ratio(LIGHT["muted"], LIGHT["surface"])
        assert r >= 4.5, f"muted text {r:.2f}:1"

    def test_amber_on_surface(self):
        """نارنجی تیره‌تر برای زمینه سفید"""
        r = contrast_ratio(LIGHT["amber"], LIGHT["surface"])
        assert r >= 4.5, f"amber accent {r:.2f}:1"

    def test_white_on_amber_button(self):
        """متن سفید روی دکمه نارنجی تیره"""
        r = contrast_ratio("#ffffff", LIGHT["amber"])
        assert r >= 4.5, f"text on amber button {r:.2f}:1"

    def test_error_red_on_surface(self):
        r = contrast_ratio(LIGHT["red"], LIGHT["surface"])
        assert r >= 4.5, f"error text {r:.2f}:1"

    def test_success_green_on_surface(self):
        r = contrast_ratio(LIGHT["green"], LIGHT["surface"])
        assert r >= 4.5, f"success text {r:.2f}:1"

    def test_dim_text_is_large_text_only(self):
        r = contrast_ratio(LIGHT["dim"], LIGHT["surface"])
        assert r >= 3.0, f"dim text {r:.2f}:1 (large text minimum)"


class TestBothThemesParity:
    """هر دو تم باید کیفیت یکسان داشته باشن"""

    def test_text_contrast_similar_across_themes(self):
        """اختلاف کنتراست متن اصلی نباید خیلی زیاد باشه"""
        dark = contrast_ratio(DARK["text"], DARK["surface"])
        light = contrast_ratio(LIGHT["text"], LIGHT["surface"])
        assert abs(dark - light) < 5, f"dark={dark:.2f} light={light:.2f}"

    def test_amber_readable_in_both(self):
        for name, palette in (("dark", DARK), ("light", LIGHT)):
            r = contrast_ratio(palette["amber"], palette["surface"])
            assert r >= 4.5, f"{name} amber {r:.2f}:1"

    def test_dark_theme_is_actually_dark(self):
        assert luminance(DARK["bg"]) < 0.02

    def test_light_theme_is_actually_light(self):
        assert luminance(LIGHT["bg"]) > 0.8
