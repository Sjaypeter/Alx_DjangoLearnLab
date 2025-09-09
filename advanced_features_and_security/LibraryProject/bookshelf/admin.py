from django.contrib import admin
from .models import Book,CustomUser,CustomUserManager
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    llist_filter = ('title','author','publication_year')
    search_fields = ('title','author')
    
class CustomUserAdmin(admin.ModelAdmin):
    pass
    

admin.site.register(Book,BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

