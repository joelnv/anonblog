from django.shortcuts import render, redirect
from .models import Post
from . import forms
from django.utils.crypto import get_random_string

def post_list(request):
    posts = Post.objects.all()
    return render(request,'posts/posts_list.html',{'posts':posts})

def post(request,id):
    post = Post.objects.get(id=id)
    return render(request, 'posts/post.html', {'post': post})

def create_post(request):
    if request.method == 'POST':
        form = forms.CreatePost(request.POST,request.FILES)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.skey =unique_id = get_random_string(length=9)
            instance.save()
            return redirect('posts:post', id=instance.id)
    else:
        form = forms.CreatePost()
    return render(request, 'posts/create_post.html',{'form':form})




