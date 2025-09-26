from rest_framework import serializers
from .models import Book, Author
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["__all__"]
        
    def validate_public_year(self,data):
        current_year = datetime.now().year
        if data > current_year:
            raise serializers.ValidationError("Publication year cannot be in future")
        return data
    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']