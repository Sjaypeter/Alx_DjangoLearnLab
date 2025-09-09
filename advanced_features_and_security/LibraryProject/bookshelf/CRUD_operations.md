CREATING BOOK INSTANCE
from bookshelf.models import Book

book = Book.objects.create(title = "1984", author = "George Orwell", publication_year = 1948) book
output:
<Book: 1984>


RETRIEVING BOOK INSTANCE
book = Book.objects.get(title = "1984")

book.title.book.author book.publication_year

output: '1984' 'George Orwell' 1949


UPDATE BOOK TITLE
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four" 
book.save()
book.title

output: 'Nineteen Eighty-Four'


DELETE BOOK INSTANCE
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete

Book.objects.all()

output: (1,{'bookshelf.Book': 1})<QuerySet []>