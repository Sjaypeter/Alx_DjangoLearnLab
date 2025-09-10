from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from django.http import HttpResponse
# Create your views here.

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    return HttpResponse("You have permission to view book")