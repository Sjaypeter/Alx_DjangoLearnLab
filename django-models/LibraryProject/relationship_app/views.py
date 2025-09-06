from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
# Create your views here.

def book_list(request):
    #A basic function view that lists all books stored in the database
    books = Book.objects.all()
    context = {'list_books':books}
    return render(request, 'list_books.html',context)


class LibraryDetailView(DetailView):
    model = Library
    