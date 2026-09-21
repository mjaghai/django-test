from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "first_name", "last_name", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "is_superuser"]
    search_fields = ["username", "email", "first_name", "last_name"]


# Unregister the default User admin and register with our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
