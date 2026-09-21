document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.getElementById('mobileToggle');
    var nav = document.getElementById('mainNav');
    var search = document.querySelector('.search-form');
    var auth = document.getElementById('authLinks');

    if (toggle) {
        toggle.addEventListener('click', function () {
            nav.classList.toggle('open');
            if (search) search.classList.toggle('open');
            if (auth) auth.classList.toggle('open');
        });
    }
});
