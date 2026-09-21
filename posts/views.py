from django.shortcuts import render


def post_list(request):
    return render(request, "posts/posts.html")


def post_detail(request):

    return render(request, "posts/post.html")
