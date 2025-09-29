from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/',LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/',views.RegisterView.as_view(), name='register'),
]
