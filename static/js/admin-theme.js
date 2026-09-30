/* مدیریت حالت روشن/تاریک پنل ادمین */
(function () {
    'use strict';

    var STORAGE_KEY = 'khodromag-admin-theme';
    var toggle = document.getElementById('themeToggle');

    function currentTheme() {
        return document.documentElement.getAttribute('data-theme') || 'dark';
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        if (toggle) {
            var label =
                theme === 'dark'
                    ? 'Switch to light theme'
                    : 'Switch to dark theme';
            toggle.setAttribute('aria-label', label);
        }
    }

    if (toggle) {
        // همگام‌سازی برچسب با تم فعال هنگام بارگذاری
        applyTheme(currentTheme());

        toggle.addEventListener('click', function () {
            var next = currentTheme() === 'dark' ? 'light' : 'dark';
            applyTheme(next);
            try {
                localStorage.setItem(STORAGE_KEY, next);
            } catch (e) {
                // اگر localStorage در دسترس نبود (مثلاً حالت خصوصی)
                // تم فقط برای همین صفحه اعمال می‌مونه
            }
        });
    }

    // اگه کاربر تم سیستم‌عامل رو عوض کنه و خودش چیزی انتخاب نکرده باشه، هماهنگ می‌شیم
    var media = window.matchMedia('(prefers-color-scheme: light)');
    var onChange = function (e) {
        var stored = null;
        try {
            stored = localStorage.getItem(STORAGE_KEY);
        } catch (err) {
            stored = null;
        }
        if (!stored) {
            applyTheme(e.matches ? 'light' : 'dark');
        }
    };

    if (media.addEventListener) {
        media.addEventListener('change', onChange);
    } else if (media.addListener) {
        media.addListener(onChange);
    }
})();
