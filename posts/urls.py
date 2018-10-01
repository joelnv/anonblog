from django.urls import path
from . import views
from posts.views import CreatePost, EditPost, MyPosts, ClaimPost
app_name='posts'


urlpatterns = [
    path('mine/', MyPosts.as_view(), name='myposts'),
    path('create/', CreatePost.as_view(), name='create'),
    path('<id>/', views.post, name='post'),
    path('<id>/edit/<skey>', EditPost.as_view(), name='anon_edit'),
    path('<id>/edit/', EditPost.as_view(), name='edit'),
    path('<id>/claim', ClaimPost.as_view(), name='claim'),



]
