from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from .models import Post

def post_list(request):
    return render(request,'posts/posts.html')

def post_detail(request):


    
    return render(request,'posts/post.html')
