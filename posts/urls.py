from django.urls import path
from . import views

app_name='posts'


urlpatterns = [
    path('', views.post_list, name = 'list'),
    path('create/', views.create_post, name='create'),
    path('<id>/', views.post, name='post'),
]
