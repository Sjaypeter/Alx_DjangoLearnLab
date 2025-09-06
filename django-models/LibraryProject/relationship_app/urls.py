from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path

urlpatterns = [
    path('login/',LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/',LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/',views.register_view, name='register'),
    path('admin/',views.admin_view, name='admin'),
    path('member/',views.member_view, name='member'),
    path('Librarian/',views.librarian_view, name= 'Librarian')
]

