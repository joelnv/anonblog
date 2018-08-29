from django.urls import path
from . import views
from posts.views import CreatePost

app_name='posts'


urlpatterns = [
    path('create/', CreatePost.as_view(), name='create'),
    path('<id>/', views.post, name='post'),
]
