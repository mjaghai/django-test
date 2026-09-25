from django.core.paginator import Paginator
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
