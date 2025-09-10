from django import forms
from .models import Book

class ExampleForm():
    q = forms.CharField(max_length=100, label='Search Books')
    