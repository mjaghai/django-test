from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("news/", views.news, name="news"),
    path("comparison/", views.comparison, name="comparison"),
    path("review/", views.review, name="review"),
    path("search/", views.search, name="search"),
    re_path(r"^post/(?P<slug>[\w-]+)/$", views.post_detail, name="post_detail"),
]
