from django.shortcuts import render

from posts.models import Post


def home(request):
    """صفحه اصلی — آخرین ۶ پست منتشر شده"""
    latest_posts = Post.objects.filter(is_published=True)[:6]
    return render(request, "pages/home.html", {"latest_posts": latest_posts})


def about(request):
    return render(request, "pages/about.html")
