from django.shortcuts import render, redirect , get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views import View
from . import forms
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe

def post(request,id):
    post = get_object_or_404(Post , id= id)
    return render(request, 'posts/post.html', {'post': post})

class CreatePost(View):

    def get(self, request):
        form = forms.CreatePosts()
        return render(request, 'posts/create_post.html',{'form':form})

    def post(self, request):
        form = forms.CreatePosts(request.POST)
        user = request.user
        if form.is_valid():
            instance =form.save(commit=False)
            instance.creator = user
            instance.skey =get_random_string(length=9)
            instance.save()
            url_path = reverse('posts:edit', kwargs={'id': instance.id , 'skey' : instance.skey})
            messages.success(request, mark_safe("<a href='{url_path}'>{url_path}</a>".format(url_path=url_path)))
            return redirect('posts:post', id=instance.id)
        return render(request, 'posts/create_post.html', {'form': form})

class EditPost(View):

    def get(self, request ,id , skey):
        post = get_object_or_404(Post, id= id, skey= skey)
        form = forms.CreatePosts(instance = post)
        return render(request, 'posts/edit.html',{'form':form, 'post':post})

    def post(self, request , id , skey):
        post = get_object_or_404(Post, id=id, skey=skey)
        form = forms.CreatePosts(request.POST , instance=  post)

        if form.is_valid():
            instance = form.save()
            instance.save()
            return redirect('posts:post', id=instance.id)
        return render(request, 'posts/edit.html', {'form': form, 'post':post})

class MyPosts(View):

    def get(self, request):
        myposts = Post.objects.filter(creator_id=request.user.id).order_by('-id')
        return render(request, 'posts/my_posts.html', {'posts': myposts})

    def post(self, request):
        return render(request, 'posts/my_posts.html')