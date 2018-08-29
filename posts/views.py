from django.shortcuts import render, redirect , get_object_or_404
from .models import Post
from django.views import View
from . import forms
from django.utils.crypto import get_random_string
from django.contrib import messages

def post(request,id):
    post = get_object_or_404(Post , id= id)
    return render(request, 'posts/post.html', {'post': post})

class CreatePost(View):

    def get(self, request):
        form = forms.CreatePosts()
        return render(request, 'posts/create_post.html',{'form':form})

    def post(self, request):
        form = forms.CreatePosts(request.POST)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.skey =unique_id = get_random_string(length=9)
            instance.save()
            messages.success(request, 'Secret Key for editing your post is '+ instance.skey)
            return redirect('posts:post', id=instance.id)
        return render(request, 'posts/create_post.html', {'form': form})







