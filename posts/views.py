from django.shortcuts import render, redirect , get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views import View
from . import forms
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import Http404

def post(request,id):
    post = get_object_or_404(Post , id= id)
    url_path = mark_safe(reverse('posts:edit', kwargs={'id': post.id}))
    return render(request, 'posts/post.html', {'post': post, 'url':url_path})

class CreatePost(View):

    def get(self, request):
        form = forms.CreatePosts()
        return render(request, 'posts/create_post.html',{'form':form})

    def post(self, request):
        form = forms.CreatePosts(request.POST)
        if form.is_valid():
            instance =form.save(commit=False)
            if request.user.is_authenticated:
                instance.creator= request.user
            instance.skey =get_random_string(length=9)
            instance.save()
            if not request.user.is_authenticated:
                url_path = reverse('posts:anon_edit', kwargs={'id': instance.id , 'skey' : instance.skey})
                messages.success(request, mark_safe("<a href='{url_path}'>{url_path}</a>".format(url_path=url_path)))
            return redirect('posts:post', id=instance.id)
        return render(request, 'posts/create_post.html', {'form': form})

class EditPost(View):

    def dispatch(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Post, id=kwargs.get('id'))
        if not self.blog.creator:
            self.blog = get_object_or_404(Post, id=kwargs.get('id'),skey=kwargs.get('skey'))
        if kwargs.get('skey') and not self.blog.creator:
            if not self.blog.skey == kwargs.get('skey'):
                raise Http404
        elif not (request.user == self.blog.creator):
            raise Http404
        return super(EditPost,self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.blog
        form = forms.CreatePosts(instance = post)
        return render(request, 'posts/edit.html',{'form':form, 'post':post})

    def post(self, request, *args, **kwargs):
        post = self.blog
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

class ClaimPost(View):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.creator = request.user
        post.save()
        return redirect('posts:edit', id=post.id)

