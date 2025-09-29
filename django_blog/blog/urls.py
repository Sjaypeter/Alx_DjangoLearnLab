from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import ListView, UpdateView, CreateView, DeleteView, DetailView


urlpatterns = [
    path('login/',LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/',LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/',views.RegisterView.as_view(), name='register'),
    path('profile/',views.profile_view, name='profile'),
    path('post/new/',CreateView.as_view(), name='new-post' ),
    path('posts/list/', ListView.as_view(), name='post-list'),
    path('posts/<int:pk>/delete/', DeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/detail/',DetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/update/', DetailView.as_view(), name='post-update'),
]
