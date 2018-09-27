from django.contrib import admin
from django.urls import path, include
from . import views
from .views import SignUp, LogIn, LogOut
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('', views.home),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LogIn.as_view() , name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
]


urlpatterns += staticfiles_urlpatterns()