from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import RegisterForm


def login_view(request):
    """صفحه‌ی ورود"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if not request.POST.get('remember'):
                request.session.set_expiry(0)  # با بسته شدن مرورگر، سشن پاک بشه
            messages.success(request, 'با موفقیت وارد شدید.')
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """صفحه‌ی ثبت‌نام"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'حساب کاربری شما با موفقیت ساخته شد.')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@require_POST
def logout_view(request):
    """خروج — فقط POST قبول می‌کنه، چون فرم داخل هدر هم با POST می‌فرسته"""
    auth_logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('home')
