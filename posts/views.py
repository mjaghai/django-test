from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    """لیست پست‌ها با صفحه‌بندی"""
    posts = Post.objects.filter(is_published=True)
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "posts/posts.html", {"page_obj": page_obj})


def post_detail(request, slug):
    """جزئیات پست"""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, "posts/post.html", {"post": post})


def news(request):
    """صفحه اخبار — پست‌های دسته‌بندی «اخبار»"""
    posts = Post.objects.filter(is_published=True, category="اخبار")
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "posts/news.html", {"page_obj": page_obj})


def comparison(request):
    """صفحه مقایسه — پست‌های دسته‌بندی «مقایسه» به شکل جدول"""
    posts = Post.objects.filter(
        is_published=True, category="مقایسه"
    ).select_related("author")
    return render(request, "posts/comparison.html", {"posts": posts})


def review(request):
    """صفحه بررسی فنی — پست‌های دسته‌بندی «بررسی»"""
    posts = Post.objects.filter(is_published=True, category="بررسی")
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "posts/review.html", {"page_obj": page_obj})


def search(request):
    """جستجو در پست‌ها"""
    query = request.GET.get("q", "").strip()
    posts = Post.objects.none()

    if query:
        posts = (
            Post.objects.filter(is_published=True)
            .filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(content__icontains=query)
                | Q(brand__icontains=query)
                | Q(model__icontains=query)
            )
            .select_related("author")
        )

    return render(
        request,
        "posts/search.html",
        {"posts": posts, "query": query},
    )
