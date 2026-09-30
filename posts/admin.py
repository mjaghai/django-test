from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "brand",
        "model",
        "year",
        "author",
        "is_published",
        "created_at",
    ]
    list_filter = ["is_published", "category", "brand", "fuel_type", "transmission"]
    search_fields = ["title", "brand", "model", "description"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_published"]
    list_per_page = 20
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    fieldsets = [
        ("Basic Info", {"fields": ["title", "slug", "author", "image"]}),
        ("Content", {"fields": ["description", "content"]}),
        (
            "Vehicle Specs",
            {
                "fields": [
                    "category",
                    "brand",
                    "model",
                    "year",
                    "engine",
                    "horsepower",
                    "acceleration_0_100",
                    "torque",
                    "transmission",
                    "fuel_type",
                    "price",
                ],
                "classes": ["collapse"],
            },
        ),
        ("Publishing", {"fields": ["is_published", "created_at", "updated_at"]}),
    ]
