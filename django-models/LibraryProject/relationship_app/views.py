from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Library
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth import logout
# Create your views here.

def book_list(request):
    #A basic function view that lists all books stored in the database
    books = Book.objects.all()
    context = {'list_books':books}
    return render(request, 'relationship_app/list_books.html',context)


class LibraryDetailView(DetailView):
    model = Library
    book = Library.objects.all()
    template_name = 'relationship_app/library_detail.html'
    
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'
    


    