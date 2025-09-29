from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import PostCreateView, PostDeleteView,PostDetailView,PostListView,PostUpdateView


urlpatterns = [
    path('login/',LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/',LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/',views.RegisterView.as_view(), name='register'),
    path('profile/',views.profile_view, name='profile'),
    path('post/new/',PostCreateView.as_view(), name='new-post' ),
    path('posts/list/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/detail/',PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/update/', PostDetailView.as_view(), name='post-update'),
]
