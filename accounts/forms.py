from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """UserCreationForm پیش‌فرض فیلد ایمیل نداره، ولی قالب register.html
    ازش استفاده کرده؛ برای همین این فیلد رو اضافه می‌کنیم."""
    email = forms.EmailField(required=True, label='ایمیل')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user