from django.urls import path
from . import views
from posts.views import CreatePost, EditPost, MyPosts, ClaimPost
from django.contrib.auth.decorators import login_required

app_name='posts'


urlpatterns = [
    path('mine/',  login_required(MyPosts.as_view()), name='myposts'),
    path('', CreatePost.as_view(), name='create'),
    path('<id>/', views.post, name='post'),
    path('<id>/edit/<skey>', EditPost.as_view(), name='anon_edit'),
    path('<id>/edit/', EditPost.as_view(), name='edit'),
    path('<id>/claim/<skey>', ClaimPost.as_view(), name='claim'),
]
