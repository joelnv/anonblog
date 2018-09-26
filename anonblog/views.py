from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def home(request):
    return render(request,'homepage.html')

class SignUp(View):
    def get(self, request):
        form = UserCreationForm()
        return  render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:create')
        return render(request, 'signup.html', {'form': form})

class LogIn(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('posts:create')
        return render(request, 'login.html', {'form': form})

class LogOut(View):

    def postx(self, request):
        logout(request)
        return redirect('posts:create')


